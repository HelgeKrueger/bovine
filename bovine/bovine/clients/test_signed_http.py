from unittest.mock import AsyncMock, MagicMock

import aiohttp

from bovine.utils.signature_checker import SignatureChecker
from bovine.utils.test import get_user_keys

from .signed_http import signed_get


async def test_signed_get():
    url = "https://test_domain/test_path"
    public_key_url = "public_key_url"
    public_key, private_key = get_user_keys()
    session = AsyncMock(aiohttp.ClientSession)
    session.get = AsyncMock()
    session.get.return_value = "value"

    key_retriever = AsyncMock()
    key_retriever.return_value = public_key
    signature_checker = SignatureChecker(key_retriever)

    response = await signed_get(session, public_key_url, private_key, url)

    session.get.assert_awaited_once()

    assert response == "value"

    args = session.get.await_args

    assert args[0] == (url,)
    assert "headers" in args[1]
    headers = args[1]["headers"]

    request = MagicMock()
    request.headers = headers
    request.method = "get"
    request.url = url

    assert await signature_checker.validate_signature(request)

    key_retriever.assert_awaited_once()
    assert key_retriever.await_args[0] == (public_key_url,)
