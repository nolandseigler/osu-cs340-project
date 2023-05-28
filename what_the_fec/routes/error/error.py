from fastapi import Request
from fastapi.templating import Jinja2Templates

def error_page_func(request: Request, templates: Jinja2Templates):
    return templates.TemplateResponse(
        "error.j2",
        {
            "request": request,
        },
    )
