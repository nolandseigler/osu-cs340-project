from datetime import date
from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from what_the_fec.routes.contributions.endpoint_funcs import create_single_func
from what_the_fec.routes.contributions.endpoint_funcs import TABLE_NAME, get_all_func

router = APIRouter(
    prefix=f"/{TABLE_NAME}",
    tags=[f"{TABLE_NAME}"],
    responses={404: {"description": "Not found"}},
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
    transaction_pgi: STR_FORM_FIELD,
    image_num: STR_FORM_FIELD,
    transaction_dt: DATE_FORM_FIELD,
    transaction_amt: FLOAT_FORM_FIELD,
    trans_id: STR_FORM_FIELD,
    file_num: INT_FORM_FIELD,
    memo_cd: STR_FORM_FIELD,
    memo_text: STR_FORM_FIELD,
    sub_id: INT_FORM_FIELD,
    cmte_id: STR_FORM_FIELD,
    report_type: STR_FORM_FIELD,
    transaction_type: STR_FORM_FIELD,
    amendment_indicator: STR_FORM_FIELD,
    contributor_type: STR_FORM_FIELD,
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
