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
    update_single_candidate_office_records_page_func,
    get_all_candidate_office_records_func,
    post_single_candidate_office_records_func,
    update_single_candidate_office_records_func,
)



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
def get_all_candidate_office_records(
    request: Request
):
    return get_all_candidate_office_records_func(
        conn=next(request.db_conn),
        request=request,
        templates=request.templates,
    )


@router.get("/update/{record_id}", response_class=HTMLResponse)
def update_single_candidate_office_records_page(
    request: Request, record_id,
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
    candidate_email: Annotated[str, Form()],
):
    return update_single_candidate_office_records_func(
        conn=next(request.db_conn),
        record_id=record_id,
        candidate_email=candidate_email,
    )

# @router.get(
#     "/delete_candidate_office_records/{record_id}", response_class=HTMLResponse
# )
# def delete_single_candidate_office_records_page(
#     request: Request, record_id, conn: Connection = Depends(db.get_conn)
# ):
#     return delete_single_candidate_office_records_page_func(
#         conn=conn, request=request, templates=templates, record_id=record_id
#     )

# @router.post("/candidate_office_records/")
# def post_single_candidate_office_records(
#     fec_cand_id: Annotated[str, Form()],
#     name: Annotated[str, Form()],
#     ttl_receipts: Annotated[float, Form()],
#     trans_from_auth: Annotated[float, Form()],
#     coh_bop: Annotated[float, Form()],
#     coh_cop: Annotated[float, Form()],
#     cand_contrib: Annotated[float, Form()],
#     cand_loans: Annotated[float, Form()],
#     other_loans: Annotated[float, Form()],
#     cand_loan_repay: Annotated[float, Form()],
#     other_loan_repay: Annotated[float, Form()],
#     debts_owed_by: Annotated[float, Form()],
#     ttl_indiv_contrib: Annotated[float, Form()],
#     cand_office_st: Annotated[str, Form()],
#     cand_office_district: Annotated[str, Form()],
#     pol_pty_contrib: Annotated[float, Form()],
#     cvg_end_dt: Annotated[date, Form()],
#     indiv_refund: Annotated[float, Form()],
#     cmte_refund: Annotated[float, Form()],
#     office_type: Annotated[str, Form()],
#     candidate_email: Annotated[str, Form()],
#     party_type: Annotated[str, Form()],
#     incumbent_challenger_status: Annotated[str, Form()],
#     conn: Connection = Depends(db.get_conn),
# ):
#     return post_single_candidate_office_records_func(
#         conn=conn,
#         fec_cand_id=fec_cand_id,
#         name=name,
#         ttl_receipts=ttl_receipts,
#         trans_from_auth=trans_from_auth,
#         coh_bop=coh_bop,
#         coh_cop=coh_cop,
#         cand_contrib=cand_contrib,
#         cand_loans=cand_loans,
#         other_loans=other_loans,
#         cand_loan_repay=cand_loan_repay,
#         other_loan_repay=other_loan_repay,
#         debts_owed_by=debts_owed_by,
#         ttl_indiv_contrib=ttl_indiv_contrib,
#         cand_office_st=cand_office_st,
#         cand_office_district=cand_office_district,
#         pol_pty_contrib=pol_pty_contrib,
#         cvg_end_dt=cvg_end_dt,
#         indiv_refund=indiv_refund,
#         cmte_refund=cmte_refund,
#         office_type=office_type,
#         candidate_email=candidate_email,
#         party_type=party_type,
#         incumbent_challenger_status=incumbent_challenger_status,
#     )



# # This is gross.
# # We are using forms everywhere so we get to choose between GET and POST.
# # No other method options are available.
# @router.post("/candidate_office_records/delete/{record_id}")
# def delete_single_candidate_office_records(
#     record_id,
#     conn: Connection = Depends(db.get_conn),
# ):
#     return delete_single_candidate_office_records_func(
#         conn=conn,
#         record_id=record_id,
#     )

