"""Check an installed distribution; run with python -I to exclude the checkout."""

import importlib
import importlib.metadata
import os
import pkgutil

import phenostore
import phenostore.gen
from phenostore import AsyncClient, Client
from phenostore.gen.models import FhirResource

expected = os.environ["RELEASE_VERSION"]
if importlib.metadata.version("phenostore-sdk-python") != expected:
    raise SystemExit("Installed distribution version does not match the release")
if phenostore.__version__ != expected:
    raise SystemExit("Installed module version does not match the release")

for module in pkgutil.walk_packages(phenostore.gen.__path__, phenostore.gen.__name__ + "."):
    importlib.import_module(module.name)

assert callable(Client) and callable(AsyncClient)
resource = {"resourceType": "Patient", "extension": [{"url": "https://example.test/custom"}]}
assert FhirResource.from_dict(resource).to_dict() == resource
print(f"Installed distribution {expected}: SDK imports, generated modules, and models passed")
