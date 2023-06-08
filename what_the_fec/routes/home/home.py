from fastapi import Request
from fastapi.templating import Jinja2Templates
from what_the_fec.routes.common.tables_information import TABLES_INFORMATION


def home_page_func(request: Request, templates: Jinja2Templates):
    return templates.TemplateResponse(
        "home/home.j2",
        {
            "request": request,
            "tables_information": TABLES_INFORMATION,
        },
    )
