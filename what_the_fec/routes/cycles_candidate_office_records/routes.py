from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from what_the_fec.routes.cycles_candidate_office_records.endpoint_funcs import (
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
    cycles_year: INT_FORM_FIELD,
    candidate_office_records_id: INT_FORM_FIELD,
):
    return create_single_func(
        conn=next(request.db_conn),
        cycles_year=cycles_year,
        candidate_office_records_id=candidate_office_records_id,
    )
