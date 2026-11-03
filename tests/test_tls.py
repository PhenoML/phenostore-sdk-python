"""Real HTTPS requests, including token exchange and a custom trusted CA."""

from __future__ import annotations

import json
import ssl
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

import httpx
import pytest
import trustme

from phenostore import AsyncClient, Client, OperationOutcomeError

from .conftest import BUNDLE, PATIENT, call


@pytest.fixture
def tls_server():
    ca = trustme.CA()
    certificate = ca.issue_cert("127.0.0.1")
    tls = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    certificate.configure_cert(tls)
    trusted = ssl.create_default_context()
    ca.configure_trust(trusted)
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

        def do_POST(self):
            body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            requests.append((self.command, self.path, dict(self.headers), body))
            if self.path == "/prefix/oauth/token":
                self.send_json(
                    200, {"access_token": "tls-token", "token_type": "Bearer", "expires_in": 3600}
                )
            else:
                self.send_json(201, json.loads(body))

        def do_GET(self):
            requests.append((self.command, self.path, dict(self.headers), b""))
            if self.path.endswith("/Patient/missing"):
                self.send_json(
                    404,
                    {
                        "resourceType": "OperationOutcome",
                        "issue": [
                            {"severity": "error", "code": "not-found", "diagnostics": "missing"}
                        ],
                    },
                )
            elif self.path.endswith("/Patient/id"):
                self.send_json(200, PATIENT)
            else:
                self.send_json(200, BUNDLE)

        def send_json(self, status, data):
            body = json.dumps(data).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/fhir+json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Last-Modified", "Wed, 21 Oct 2015 07:28:00 GMT")
            self.end_headers()
            self.wfile.write(body)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.socket = tls.wrap_socket(server.socket, server_side=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"https://127.0.0.1:{server.server_port}/prefix/", trusted, requests
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


@pytest.mark.parametrize("cls", [Client, AsyncClient], ids=["sync", "async"])
async def test_real_tls_round_trip(tls_server, cls):
    base_url, trusted, requests = tls_server
    client = cls(base_url, "client", "secret+&", "t", "s", verify=trusted, timeout=httpx.Timeout(5))
    try:
        assert await call(client.read_resource, "Patient", "id") == PATIENT
        assert await call(client.create_resource, "Patient", PATIENT) == PATIENT
        assert await call(client.search_resources, "Patient", {"name": "Ana & Maria"}) == BUNDLE
        with pytest.raises(OperationOutcomeError, match="missing"):
            await call(client.read_resource, "Patient", "missing")
    finally:
        await call(client.close if cls is Client else client.aclose)
    assert len(requests) == 5  # One token exchange and four API calls.
    assert parse_qs(requests[0][3].decode())["client_secret"] == ["secret+&"]
    assert "Authorization" not in requests[0][2]
    assert all(r[2]["Authorization"] == "Bearer tls-token" for r in requests[1:])
    assert "name=Ana+%26+Maria" in requests[3][1]
