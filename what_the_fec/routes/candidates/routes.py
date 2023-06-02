from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from what_the_fec.routes.candidates.endpoint_funcs import (
    TABLE_NAME,
    create_single_func,
    get_all_func,
)
from what_the_fec.routes.route import BaseRoute

router = APIRouter(
    prefix=f"/{TABLE_NAME}",
    tags=[f"{TABLE_NAME}"],
    route_class=BaseRoute,
)

STR_FORM_FIELD = Annotated[str, Form()]


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
    first_name: STR_FORM_FIELD,
    middle_name: STR_FORM_FIELD,
    last_name: STR_FORM_FIELD,
    email: STR_FORM_FIELD,
):
    return create_single_func(
        conn=next(request.db_conn),
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        email=email,
    )
