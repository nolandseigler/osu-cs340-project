from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from what_the_fec.routes.candidate_office_records_committees.endpoint_funcs import (
    TABLE_NAME,
    create_single_func,
    get_all_func,
    update_single_func,
    update_single_page_func,
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
    fec_cand_id: STR_FORM_FIELD,
):
    print("request=", request)
    return create_single_func(
        conn=next(request.db_conn),
        cmte_id=cmte_id,
        fec_cand_id=fec_cand_id,
    )

@router.get("/update/{record_id}", response_class=HTMLResponse)
def update_single_page(
    request: Request,
    record_id: str,
):
    candidate_office_records_id, committees_id = record_id.split("_")
    return update_single_page_func(
        conn=next(request.db_conn),
        request=request,
        templates=request.templates,
        candidate_office_records_id=int(candidate_office_records_id),
        committees_id=int(committees_id),
    )


@router.post("/update/{record_id}")
def update_single(
    request: Request,
    record_id: str,
    updated_fec_cand_id: STR_FORM_FIELD,
    updated_cmte_id: STR_FORM_FIELD,
):
    candidate_office_records_id, committees_id = record_id.split("_")
    return update_single_func(
        conn=next(request.db_conn),
        candidate_office_records_id=int(candidate_office_records_id),
        committees_id=int(committees_id),
        updated_fec_cand_id=updated_fec_cand_id,
        updated_cmte_id=updated_cmte_id,
    )
