from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from what_the_fec.routes.home.home import home_page_func

router = APIRouter(
    tags=["home"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return home_page_func(
        request=request,
        templates=request.templates,
    )