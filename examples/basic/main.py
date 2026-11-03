"""Read a patient and search observations using environment-provided credentials."""

import os

from phenostore import Client, OperationOutcomeError, is_not_found


def main() -> None:
    with Client(
        os.environ["PHENOSTORE_BASE_URL"],
        os.environ["PHENOSTORE_CLIENT_ID"],
        os.environ["PHENOSTORE_CLIENT_SECRET"],
        os.environ["PHENOSTORE_TENANT"],
        os.environ["PHENOSTORE_STORE"],
    ) as client:
        patient_id = os.environ["PHENOSTORE_PATIENT_ID"]
        try:
            print(client.read_resource("Patient", patient_id))
        except OperationOutcomeError as error:
            if not is_not_found(error):
                raise
            print("Patient not found")
        print(client.search_resources("Observation", {"subject": f"Patient/{patient_id}"}))


if __name__ == "__main__":
    main()
