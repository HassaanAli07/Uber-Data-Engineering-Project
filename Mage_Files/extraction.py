import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    url = 'http://minio:9001/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL3ViZXItZGF0YS1idWNrZXQvdWJlcl9kYXRhLmNzdj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUdUUzVRM09OVEJCMkpQN0YxUkhJJTJGMjAyNTA1MDMlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwNTAzVDIyMTY1NVomWC1BbXotRXhwaXJlcz00MzIwMCZYLUFtei1TZWN1cml0eS1Ub2tlbj1leUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaFkyTmxjM05MWlhraU9pSkhWRk0xVVROUFRsUkNRakpLVURkR01WSklTU0lzSW1WNGNDSTZNVGMwTmpNMU16WXpPQ3dpY0dGeVpXNTBJam9pYldsdWFXOWhaRzFwYmlKOS43cmtOOVhncFZ2YUVMNmY0aGtkR2llYjRwbGxIRXJlZEhNWkxzZ3F6d3B2SkdzdTdpSFU5VFIwRy1VZURKaW9uc3FJWURNa0Zqc3E1MHhJWWR4M3p0dyZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmdmVyc2lvbklkPW51bGwmWC1BbXotU2lnbmF0dXJlPWRlY2VhMDA3ODVlYTA4ZDczNDBlODE5ZTNhZmJkOGEzMGFiMWJlYTY0OWJhM2E0NWFiMjRiODA2NTU2ODQ1YWI'
    response = requests.get(url)

    return pd.read_csv(io.StringIO(response.text), sep=',')


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
