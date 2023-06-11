from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from what_the_fec.routes.error.error import error_page_func

router = APIRouter(
    tags=["error"],
    responses={404: {"description": "Not found"}},
)


@router.get("/error", response_class=HTMLResponse)
def error_page(request: Request):
    return error_page_func(
        request=request,
        templates=request.templates,
    )
