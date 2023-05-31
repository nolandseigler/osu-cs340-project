from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection, text

from what_the_fec.routes.helpers import generic_render_table

TABLE_NAME = "committees"


def get_all_func(conn: Connection, request: Request, templates: Jinja2Templates):
    committees_query = f"""
        SELECT 
            `{TABLE_NAME}`.id,
            cmte_id,
            `{TABLE_NAME}`.name,
            city,
            state,
            zip_code,
            `committee_types`.name as committee_type
        FROM `{TABLE_NAME}`
            INNER JOIN `committee_types`
                ON `{TABLE_NAME}`.committee_types_id = `committee_types`.id
    """

    committee_types_query = "SELECT id, name FROM committee_types"

    committee_types = conn.execute(text(committee_types_query)).mappings().all()

    dropdown_items_for_add = {
        "committee_type": {
            "data": committee_types,
            "relevant_column_name": "name",
        },
    }

    return generic_render_table(
        conn=conn,
        query=committees_query,
        request=request,
        table_name=TABLE_NAME,
        templates=templates,
        dropdown_keys=[
            "committee_type",
        ],
        dropdown_items_for_add=dropdown_items_for_add,
    )
