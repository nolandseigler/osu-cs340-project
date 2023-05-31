from datetime import date
from typing import Annotated

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse


from what_the_fec.routes.contributions.endpoint_funcs import (
    get_all_func
)

router = APIRouter(
    prefix="/contributions",
    tags=["contributions"],
    responses={404: {"description": "Not found"}},
)


# Citation for the following code:
# Date: 04/06/2023
# Copied from /OR/ Adapted from /OR/ Based on:
# FastAPI/SQLAlchemy documentation examples
@router.get("/", response_class=HTMLResponse)
def get_all_contributions(request: Request):
    return get_all_func(
        conn=next(request.db_conn),
        request=request,
        templates=request.templates,
    )