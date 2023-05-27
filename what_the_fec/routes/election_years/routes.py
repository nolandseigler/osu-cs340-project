from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from what_the_fec.routes.election_years.endpoint_funcs import TABLE_NAME, get_all_func

router = APIRouter(
    prefix=f"/{TABLE_NAME}",
    tags=[f"{TABLE_NAME}"],
    responses={404: {"description": f"{TABLE_NAME} not found"}},
)


@router.get("/", response_class=HTMLResponse)
def get_all(request: Request):
    return get_all_func(
        conn=next(request.db_conn),
        request=request,
        templates=request.templates,
    )
