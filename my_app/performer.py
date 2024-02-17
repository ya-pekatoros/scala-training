import asyncio
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from typing import Optional, Literal
from dataclasses import dataclass
from datetime import datetime, timedelta
import random

timeout_seconds = timedelta(seconds=15).total_seconds()


class Response(Enum):
    Success = 1
    RetryAfter = 2
    Failure = 3


class ApplicationStatusResponse(Enum):
    Success = 1
    Failure = 2


@dataclass
class ApplicationResponse:
    application_id: str
    status: ApplicationStatusResponse
    description: str
    last_request_time: datetime
    retriesCount: Optional[int]


async def get_random_result_from_application() -> Response:
    """Имитация поведения сервиса - возврат ответа или timeout или ошибка"""
    asnwer = random.choice(list(Response))
    status = random.choice(
        [
            "ok",
        ]
        * 15
        + ["error", "timeout"]
    )
    if status == "error":
        raise
    elif status == "timeout":
        await asyncio.sleep(int(timeout_seconds) + 1)
    return asnwer


def form_result(
    response: ApplicationStatusResponse,
    app_id: int,
    last_request_time: datetime,
    restries: int = 0,
) -> ApplicationResponse:
    app_response: ApplicationResponse = ApplicationResponse(
        application_id=str(app_id),
        status=response,
        description="Some desctiption",
        last_request_time=last_request_time,
        retriesCount=restries,
    )
    return app_response


class Application:
    app_id: int

    def __init__(self, app_id):
        self.app_id = app_id

    async def get_application_status(
        self, identifier: str
    ) -> ApplicationResponse | Literal["error"]:
        # Метод, возвращающий статус заявки
        retries_count = 0
        while True:
            try:
                response = await get_random_result_from_application()
                lat_request_time = datetime.now()
                if response == Response.RetryAfter:
                    await asyncio.sleep(1)
                    retries_count += 1
                else:
                    break
            except Exception:
                return "error"

        loop = asyncio.get_running_loop()

        with ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(
                pool,
                form_result,
                response,
                self.app_id,
                lat_request_time,
                retries_count,
            )
            return result


async def perform_operation(
    identifier: str,
) -> list[ApplicationResponse | Literal["error"]] | Literal["TIMEOUT"]:
    loop = asyncio.get_running_loop()

    app_1 = Application(app_id=1)
    app_2 = Application(app_id=2)

    task_1 = loop.create_task(app_1.get_application_status(identifier))
    task_2 = loop.create_task(app_2.get_application_status(identifier))
    await asyncio.sleep(0)

    for i in range(int(timeout_seconds)):
        if task_1.done() and task_2.done():
            response_1 = task_1.result()
            response_2 = task_2.result()

            return [response_1, response_2]
        await asyncio.sleep(1)

    return "TIMEOUT"
