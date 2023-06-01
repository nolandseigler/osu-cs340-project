from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from what_the_fec.routes.committees.endpoint_funcs import (
    TABLE_NAME,
    create_single_func,
    get_all_func,
)

router = APIRouter(
    prefix=f"/{TABLE_NAME}",
    tags=[f"{TABLE_NAME}"],
    responses={404: {"description": f"{TABLE_NAME} not found"}},
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
    cmte_id: STR_FORM_FIELD,
    name: STR_FORM_FIELD,
    city: STR_FORM_FIELD,
    state: STR_FORM_FIELD,
    zip_code: STR_FORM_FIELD,
    committee_type: STR_FORM_FIELD,
):
    return create_single_func(
        conn=next(request.db_conn),
        cmte_id=cmte_id,
        name=name,
        city=city,
        state=state,
        zip_code=zip_code,
        committee_types_name=committee_type,
    )
