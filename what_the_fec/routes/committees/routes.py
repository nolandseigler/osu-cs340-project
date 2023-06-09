from typing import Annotated, Optional

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from what_the_fec.routes.committees.endpoint_funcs import (
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
    cmte_id: STR_FORM_FIELD,
    name: STR_FORM_FIELD,
    committee_type: STR_FORM_FIELD,
    city: Optional[str] = Form(None),
    state: Optional[str] = Form(None),
    zip_code: Optional[str] = Form(None),

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