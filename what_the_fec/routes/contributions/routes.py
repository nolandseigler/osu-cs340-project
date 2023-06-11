from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from what_the_fec.routes.contributions.endpoint_funcs import (
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
DATE_FORM_FIELD = Annotated[date, Form()]
FLOAT_FORM_FIELD = Annotated[float, Form()]
INT_FORM_FIELD = Annotated[float, Form()]


# Citation for the following code:
# Date: 04/06/2023
# Copied from /OR/ Adapted from /OR/ Based on:
# FastAPI/SQLAlchemy documentation examples
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
    report_type: STR_FORM_FIELD,
    transaction_type: STR_FORM_FIELD,
    amendment_indicator: STR_FORM_FIELD,
    contributor_type: STR_FORM_FIELD,
    transaction_pgi: Optional[str] = Form(None),
    image_num: Optional[str] = Form(None),
    transaction_dt: Optional[date] = Form(None),
    transaction_amt: Optional[float] = Form(None),
    trans_id: Optional[str] = Form(None),
    file_num: Optional[int] = Form(None),
    memo_cd: Optional[str] = Form(None),
    memo_text: Optional[str] = Form(None),
    sub_id: Optional[int] = Form(None),
):
    return create_single_func(
        conn=next(request.db_conn),
        transaction_pgi=transaction_pgi,
        image_num=image_num,
        transaction_dt=transaction_dt,
        transaction_amt=transaction_amt,
        trans_id=trans_id,
        file_num=file_num,
        memo_cd=memo_cd,
        memo_text=memo_text,
        sub_id=sub_id,
        cmte_id=cmte_id,
        report_type=report_type,
        transaction_type=transaction_type,
        amendment_indicator=amendment_indicator,
        contributor_type=contributor_type,
    )
