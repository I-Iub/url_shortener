import typing
from logging import config as logging_config

import uvicorn
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import ORJSONResponse
from starlette.responses import StreamingResponse

from src.api.v1 import base
from src.core import config
from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)
app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)
app.include_router(base.router, prefix='/api/v1')


@app.middleware('http')
async def blacklist_check(
        request: Request, call_next: typing.Callable
) -> typing.Union[Response, StreamingResponse]:
    if request.client.host in config.BLACK_LIST:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    response = await call_next(request)
    return response


if __name__ == '__main__':
    uvicorn.run(
        'src.main:app',
        host=config.PROJECT_HOST,
        port=config.PROJECT_PORT,
    )
