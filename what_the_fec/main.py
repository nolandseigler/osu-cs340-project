import os
from datetime import date
from typing import Annotated

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection
from sqlalchemy.sql import text

from what_the_fec.api.candidate_office_records import (
    delete_single_candidate_office_records_func,
    delete_single_candidate_office_records_page_func,
    edit_single_candidate_office_records_page_func,
    get_all_candidate_office_records_func,
    home_page_func,
    post_single_candidate_office_records_func,
    update_single_candidate_office_records_func,
)
from what_the_fec.storage.db import init as db_init
from what_the_fec.storage.mysql.config import MySQLConfig

# this doesnt feel great but works for today
from what_the_fec.storage.mysql.db import get_db

from what_the_fec.static.table_information import tables_information

def create_app() -> FastAPI:
    app = FastAPI()
    app.mount(
        "/static", StaticFiles(directory=os.environ["STATIC_DIR_PATH"]), name="static"
    )
    templates = Jinja2Templates(directory=os.environ["TEMPLATES_DIR_PATH"])

    db_init(
        config=MySQLConfig(
            db_user=os.environ["MARIA_DB_USER"],
            db_password=os.environ["MARIA_DB_PASSWORD"],
            db_hostname=os.environ["MARIA_DB_HOSTNAME"],
            db_port=os.environ["MARIA_DB_PORT"],
            db_name=os.environ["MARIA_DB_NAME"],
            pool_connections=2,
        )
    )
    db = get_db()

    @app.get("/", response_class=HTMLResponse)
    def home_page(request: Request):
        return home_page_func(request=request, templates=templates, tables_information=tables_information)

    # Citation for the following code:
    # Date: 04/06/2023
    # Copied from /OR/ Adapted from /OR/ Based on:
    # FastAPI/SQLAlchemy documentation examples
    @app.get("/candidate_office_records/", response_class=HTMLResponse)
    def get_all_candidate_office_records(
        request: Request, conn: Connection = Depends(db.get_conn)
    ):
        return get_all_candidate_office_records_func(
            conn=conn, request=request, templates=templates
        )

    @app.get("/edit_candidate_office_records/{record_id}", response_class=HTMLResponse)
    def edit_single_candidate_office_records_page(
        request: Request, record_id, conn: Connection = Depends(db.get_conn)
    ):
        return edit_single_candidate_office_records_page_func(
            conn=conn, request=request, templates=templates, record_id=record_id
        )

    @app.get(
        "/delete_candidate_office_records/{record_id}", response_class=HTMLResponse
    )
    def delete_single_candidate_office_records_page(
        request: Request, record_id, conn: Connection = Depends(db.get_conn)
    ):
        return delete_single_candidate_office_records_page_func(
            conn=conn, request=request, templates=templates, record_id=record_id
        )
    
    @app.post("/candidate_office_records/")
    def post_single_candidate_office_records(
        fec_cand_id: Annotated[str, Form()],
        name: Annotated[str, Form()],
        ttl_receipts: Annotated[float, Form()],
        trans_from_auth: Annotated[float, Form()],
        coh_bop: Annotated[float, Form()],
        coh_cop: Annotated[float, Form()],
        cand_contrib: Annotated[float, Form()],
        cand_loans: Annotated[float, Form()],
        other_loans: Annotated[float, Form()],
        cand_loan_repay: Annotated[float, Form()],
        other_loan_repay: Annotated[float, Form()],
        debts_owed_by: Annotated[float, Form()],
        ttl_indiv_contrib: Annotated[float, Form()],
        cand_office_st: Annotated[str, Form()],
        cand_office_district: Annotated[str, Form()],
        pol_pty_contrib: Annotated[float, Form()],
        cvg_end_dt: Annotated[
            date, Form()
        ],
        indiv_refund: Annotated[float, Form()],
        cmte_refund: Annotated[float, Form()],
        office_type: Annotated[str, Form()],
        candidate_email: Annotated[str, Form()],
        party_type: Annotated[str, Form()],
        incumbent_challenger_status: Annotated[str, Form()],
        conn: Connection = Depends(db.get_conn),
    ):
        return post_single_candidate_office_records_func(
            conn=conn,
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

    # This is gross.
    # We are using forms everywhere so we get to choose between GET and POST.
    # No other method options are available.
    @app.post("/candidate_office_records/update/{record_id}")
    def update_single_candidate_office_records(
        record_id,
        candidate_email: Annotated[str, Form()],
        conn: Connection = Depends(db.get_conn),
    ):
        return update_single_candidate_office_records_func(
            conn=conn,
            record_id=record_id,
            candidate_email=candidate_email,
        )

    # This is gross.
    # We are using forms everywhere so we get to choose between GET and POST.
    # No other method options are available.
    @app.post("/candidate_office_records/delete/{record_id}")
    def delete_single_candidate_office_records(
        record_id,
        conn: Connection = Depends(db.get_conn),
    ):
        return delete_single_candidate_office_records_func(
            conn=conn,
            record_id=record_id,
        )

    return app
