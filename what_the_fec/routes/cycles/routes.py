from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from what_the_fec.routes.cycles.endpoint_funcs import (
    TABLE_NAME,
    create_single_func,
    get_all_func,
)

router = APIRouter(
    prefix=f"/{TABLE_NAME}",
    tags=[f"{TABLE_NAME}"],
    responses={404: {"description": f"{TABLE_NAME} not found"}},
)

INT_FORM_FIELD = Annotated[int, Form()]


@router.get("/", response_class=HTMLResponse)
def get_all(request: Request):
    return get_all_func(
        conn=next(request.db_conn),
        request=request,
        templates=request.templates,
    )


@router.post("/")
def create_single(
    request: Request,
    year: INT_FORM_FIELD,
):
    return create_single_func(
        conn=next(request.db_conn),
        year=year,
    )
