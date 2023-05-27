from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection
from sqlalchemy.sql import text

from what_the_fec.dependencies import get_db_conn
from what_the_fec.routes.candidate_office_records.candidate_office_records import (
    delete_single_candidate_office_records_func,
    delete_single_candidate_office_records_page_func,
    get_all_candidate_office_records_func,
    post_single_candidate_office_records_func,
    update_single_candidate_office_records_func,
    update_single_candidate_office_records_page_func,
)

STR_FORM_FIELD = Annotated[str, Form()]
FLOAT_FORM_FIELD = Annotated[float, Form()]
DATE_FORM_FIELD = Annotated[date, Form()]

router = APIRouter(
    prefix="/candidate_office_records",
    tags=["candidate_office_records"],
    responses={404: {"description": "Not found"}},
)


# Citation for the following code:
# Date: 04/06/2023
# Copied from /OR/ Adapted from /OR/ Based on:
# FastAPI/SQLAlchemy documentation examples
@router.get("/", response_class=HTMLResponse)
def get_all_candidate_office_records(request: Request):
    return get_all_candidate_office_records_func(
        conn=next(request.db_conn),
        request=request,
        templates=request.templates,
    )


@router.post("/")
def post_single_candidate_office_records(
    request: Request,
    fec_cand_id: STR_FORM_FIELD,
    name: STR_FORM_FIELD,
    ttl_receipts: FLOAT_FORM_FIELD,
    trans_from_auth: FLOAT_FORM_FIELD,
    coh_bop: FLOAT_FORM_FIELD,
    coh_cop: FLOAT_FORM_FIELD,
    cand_contrib: FLOAT_FORM_FIELD,
    cand_loans: FLOAT_FORM_FIELD,
    other_loans: FLOAT_FORM_FIELD,
    cand_loan_repay: FLOAT_FORM_FIELD,
    other_loan_repay: FLOAT_FORM_FIELD,
    debts_owed_by: FLOAT_FORM_FIELD,
    ttl_indiv_contrib: FLOAT_FORM_FIELD,
    cand_office_st: STR_FORM_FIELD,
    cand_office_district: STR_FORM_FIELD,
    pol_pty_contrib: FLOAT_FORM_FIELD,
    cvg_end_dt: DATE_FORM_FIELD,
    indiv_refund: FLOAT_FORM_FIELD,
    cmte_refund: FLOAT_FORM_FIELD,
    office_type: STR_FORM_FIELD,
    candidate_email: STR_FORM_FIELD,
    party_type: STR_FORM_FIELD,
    incumbent_challenger_status: STR_FORM_FIELD,
):
    return post_single_candidate_office_records_func(
        conn=next(request.db_conn),
        fec_cand_id=fec_cand_id,
        name=name,
        ttl_receipts=ttl_receipts,
        trans_from_auth=trans_from_auth,
        coh_bop=coh_bop,
        coh_cop=coh_cop,
        cand_contrib=cand_contrib,
        cand_loans=cand_loans,
        other_loans=other_loans,
        cand_loan_repay=cand_loan_repay,
        other_loan_repay=other_loan_repay,
        debts_owed_by=debts_owed_by,
        ttl_indiv_contrib=ttl_indiv_contrib,
        cand_office_st=cand_office_st,
        cand_office_district=cand_office_district,
        pol_pty_contrib=pol_pty_contrib,
        cvg_end_dt=cvg_end_dt,
        indiv_refund=indiv_refund,
        cmte_refund=cmte_refund,
        office_type=office_type,
        candidate_email=candidate_email,
        party_type=party_type,
        incumbent_challenger_status=incumbent_challenger_status,
    )


@router.get("/update/{record_id}", response_class=HTMLResponse)
def update_single_candidate_office_records_page(
    request: Request,
    record_id,
):
    return update_single_candidate_office_records_page_func(
        conn=next(request.db_conn),
        request=request,
        templates=request.templates,
        record_id=record_id,
    )


@router.post("/update/{record_id}")
def update_single_candidate_office_records(
    request: Request,
    record_id,
    candidate_email: STR_FORM_FIELD,
):
    return update_single_candidate_office_records_func(
        conn=next(request.db_conn),
        record_id=record_id,
        candidate_email=candidate_email,
    )


@router.get("/delete/{record_id}", response_class=HTMLResponse)
def delete_single_candidate_office_records_page(
    request: Request,
    record_id,
):
    return delete_single_candidate_office_records_page_func(
        conn=next(request.db_conn),
        request=request,
        templates=request.templates,
        record_id=record_id,
    )


@router.post("/delete/{record_id}")
def delete_single_candidate_office_records(
    request: Request,
    record_id,
):
    return delete_single_candidate_office_records_func(
        conn=next(request.db_conn),
        record_id=record_id,
    )
