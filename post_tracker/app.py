from contextlib import AbstractAsyncContextManager
from typing import Self

import httpx
from user_agent import generate_user_agent

from post_tracker.custom_types import TrackingResult
from post_tracker.logger import get_logger
from post_tracker.utils import get_viewstate, parse_tracking_result

logger = get_logger(name=__name__)


class PostTracker(AbstractAsyncContextManager):
    """
    PostTracker is the main class that will be used get tracking info.
    """

    def __init__(self) -> None:
        """initializing the PostTracker application."""

        timeout_config = httpx.Timeout(
            timeout=20.0,   # مجموع زمان کل درخواست
            connect=5.0,    # زمان اتصال
            read=15.0,      # زمان دریافت پاسخ
            write=10.0,     # زمان ارسال اطلاعات
            pool=5.0        # زمان انتظار برای آزاد شدن کانکشن از pool
        )

        self._httpx_client = httpx.AsyncClient(timeout=timeout_config)

        logger.debug("PostTracker app Initialized !")

    async def __aenter__(self) -> Self:
        logger.debug("async client opened.")
        return self

    async def __aexit__(self, __exc_type, __exc_value, __traceback) -> None:
        await self.close()

    async def close(self) -> None:
        if not self._httpx_client.is_closed:
            await self._httpx_client.aclose()
        logger.debug("PostTracker application closed.")

    async def get_tracking_post(self, tracking_code: str) -> TrackingResult:
        url = f"https://tracking.post.ir/search.aspx?id={tracking_code}"

        viewstate, event_validation = await get_viewstate(
            client=self._httpx_client, tracking_code=tracking_code
        )
        user_agent = generate_user_agent()

        payload = {
            "scripmanager1": "pnlMain|btnSearch",
            "__LASTFOCUS": "",
            "txtbSearch": tracking_code,
            "txtVoteReason": "",
            "txtVoteTel": "",
            "__EVENTTARGET": "btnSearch",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": viewstate,
            "__VIEWSTATEGENERATOR": "BBBC20B8",
            "__VIEWSTATEENCRYPTED": "",
            "__EVENTVALIDATION": event_validation,
            "__ASYNCPOST": "true",
            "": "",
        }

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Host": "tracking.post.ir",
            "Origin": "https://tracking.post.ir",
            "Referer": f"https://tracking.post.ir/search.aspx?id={tracking_code}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": user_agent,
            "X-MicrosoftAjax": "Delta=true",
            "X-Requested-With": "XMLHttpRequest",
        }

        response = await self._httpx_client.post(
            url,
            data=payload,
            headers=headers,
            follow_redirects=True
        )

        content = response.text
        data = parse_tracking_result(content=content)
        return data
