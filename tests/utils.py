import requests_mock

import typing as t

from khulnasoft import KhulnasoftApiClient


def get_test_client(
    *,
    tenant_id: t.Optional[int] = None,
    authenticated: bool = True,
) -> KhulnasoftApiClient:
    client = KhulnasoftApiClient(
        api_key="test-api-key",
        tenant_id=tenant_id,
    )

    if authenticated:
        with requests_mock.Mocker() as mocker:
            mocker.register_uri(
                "POST",
                "https://api.khulnasoft.com/tokens/generate",
                json={
                    "token": "test-token-hello",
                },
                status_code=200,
            )
            client.generate_token()

    return client
