import time
from typing import Callable

import structlog
from fastapi import HTTPException, Request, Response
from fastapi.routing import APIRoute

logger: structlog.types.FilteringBoundLogger = structlog.get_logger(__name__)
# Citation for the following code:
# Date: 05/21/2023
# Copied from /OR/ Adapted from /OR/ Based on:
# https://fastapi.tiangolo.com/advanced/custom-request-and-route/#custom-apiroute-class-in-a-router


# NOTE: This is just a very rough start so the errors will make it to the web browser.
# Since this is an "admin" db app we are going to send the exact error to the client.
class BaseRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                response: Response = await original_route_handler(request)
            except HTTPException as h:
                logger.aexception("an error occurred")
                return Response(str(h), status_code=h.status_code)
            # catch the bare exception if nothing else did.
            except Exception as e:
                logger.aexception("an error occurred")
                return Response(str(e), status_code=500)
            return response

        return custom_route_handler
