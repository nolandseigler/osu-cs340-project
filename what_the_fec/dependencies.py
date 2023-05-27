from fastapi import Request
from fastapi.templating import Jinja2Templates

from what_the_fec.storage.mysql.db import get_db_conn as _get_db_conn


def get_db_conn(request: Request) -> None:
    request.db_conn = _get_db_conn()


_TEMPLATES = None


def templates_init(templates: Jinja2Templates):
    global _TEMPLATES
    _TEMPLATES = templates


def _get_templates():
    global _TEMPLATES
    if _TEMPLATES is None:
        raise ValueError("templates not set;")
    return _TEMPLATES


def get_templates(request: Request) -> None:
    request.templates = _get_templates()
