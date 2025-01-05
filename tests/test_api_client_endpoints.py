import pytest
import requests_mock

from .utils import get_test_client


def test_wrapped_methods() -> None:
    client = get_test_client(authenticated=False)
    assert client._api_token is None
    assert client._api_token_exp is None

    # POST: This one will generate since its the first one.
    with requests_mock.Mocker() as mocker:
        mocker.register_uri(
            "POST",
            "https://api.khulnasoft.com/tokens/generate",
            json={
                "token": "test-token-hello",
            },
            status_code=200,
        )
        mocker.register_uri(
            "POST",
            "https://api.khulnasoft.com/hello-post",
            status_code=200,
        )

        client.post("https://api.khulnasoft.com/hello-post", json={"foo": "bar"})
        assert mocker.last_request.url == "https://api.khulnasoft.com/hello-post"
        assert mocker.last_request.headers["Authorization"] == "Bearer test-token-hello"
        assert mocker.last_request.json() == {"foo": "bar"}

    # GET
    with requests_mock.Mocker() as mocker:
        mocker.register_uri(
            "GET",
            "https://api.khulnasoft.com/hello-get",
            json={"foo": "bar"},
            status_code=200,
        )

        client.get("https://api.khulnasoft.com/hello-get")
        assert mocker.last_request.url == "https://api.khulnasoft.com/hello-get"
        assert mocker.last_request.headers["Authorization"] == "Bearer test-token-hello"

    # PUT
    with requests_mock.Mocker() as mocker:
        mocker.register_uri(
            "PUT",
            "https://api.khulnasoft.com/hello-put",
            json={"foo": "bar"},
            status_code=200,
        )

        client.put("https://api.khulnasoft.com/hello-put")
        assert mocker.last_request.url == "https://api.khulnasoft.com/hello-put"
        assert mocker.last_request.headers["Authorization"] == "Bearer test-token-hello"

    # DELETE
    with requests_mock.Mocker() as mocker:
        mocker.register_uri(
            "DELETE",
            "https://api.khulnasoft.com/hello-delete",
            json={"foo": "bar"},
            status_code=200,
        )

        client.delete("https://api.khulnasoft.com/hello-delete")
        assert mocker.last_request.url == "https://api.khulnasoft.com/hello-delete"
        assert mocker.last_request.headers["Authorization"] == "Bearer test-token-hello"


def test_get_path_only() -> None:
    client = get_test_client()
    with requests_mock.Mocker() as mocker:
        mocker.register_uri(
            "GET",
            "https://api.khulnasoft.com/hello/test",
            status_code=200,
        )
        client.get("/hello/test")
        assert mocker.last_request.url == "https://api.khulnasoft.com/hello/test"


def test_get_user_agent() -> None:
    client = get_test_client()
    with requests_mock.Mocker() as mocker:
        mocker.register_uri(
            "GET",
            "https://api.khulnasoft.com/hello/test",
            status_code=200,
        )
        client.get("/hello/test")
        assert mocker.last_request.url == "https://api.khulnasoft.com/hello/test"
        user_agent = mocker.last_request.headers["User-Agent"]

    assert "python-khulnasoft/" in user_agent
    assert "requests/" in user_agent


def test_bad_domain() -> None:
    client = get_test_client()

    with pytest.raises(
        Exception,
        match="Client was used to access netloc='bad.com' at url='https://bad.com/hello-post'. Only the domain api.khulnasoft.com is supported.",
    ):
        client.post("https://bad.com/hello-post")
