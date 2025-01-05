# python-khulnasoft

`khulnasoft` is a light [Khulnasoft API](https://api.docs.khulnasoft.com/) SDK that wraps [requests](https://requests.readthedocs.io/) and automatically manages authentication.

Usage examples and use cases are documented in the [Khulnasoft API documentation](https://api.docs.khulnasoft.com/sdk/python).

## Installing

`khulnasoft` is [available on PyPI](https://pypi.org/project/khulnasoft/).

The library can be installed via `pip install khulnasoft`.

## Basic Usage

```python
import os

from khulnasoft import KhulnasoftApiClient


client = KhulnasoftApiClient(
    api_key=os.environ["KHULNASOFT_API_KEY"],
    tenant_id=None,  # Use my default tenant.
)

resp = client.get("/tokens/test")

print(resp.json())
```

## Contributing

- `make test` will run tests
- `make format` format will format the code
- `make lint` will run typechecking + linting
