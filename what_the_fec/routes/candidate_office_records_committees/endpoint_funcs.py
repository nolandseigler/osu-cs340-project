from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection

from what_the_fec.routes.helpers import generic_render_table

TABLE_NAME = "candidate_office_records_committees"


def get_all_func(conn: Connection, request: Request, templates: Jinja2Templates):
    query = f"""
        SELECT * FROM {TABLE_NAME}
    """
    return generic_render_table(
        conn=conn,
        query=query,
        request=request,
        table_name=TABLE_NAME,
        templates=templates,
    )
