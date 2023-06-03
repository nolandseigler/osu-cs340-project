from fastapi import Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection, text

from what_the_fec.routes.helpers import generic_render_table

TABLE_NAME = "committees"


def get_all_func(conn: Connection, request: Request, templates: Jinja2Templates):
    query = f"""
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
        query=query,
        request=request,
        table_name=TABLE_NAME,
        templates=templates,
        dropdown_keys=[
            "committee_type",
        ],
        dropdown_items_for_add=dropdown_items_for_add,
    )


def create_single_func(
    conn: Connection,
    cmte_id,
    name,
    city,
    state,
    zip_code,
    committee_types_name,
):
    insert_query = f"""
        INSERT INTO `{TABLE_NAME}` (
            cmte_id,
            name,
            city,
            state,
            zip_code,
            committee_types_id
        ) VALUES
        (
            :cmte_id,
            :name,
            :city,
            :state,
            :zip_code,
            (SELECT id FROM `committee_types` WHERE name = :committee_types_name)
        )
    """

    bind_params = [
        dict(
            cmte_id=cmte_id,
            name=name,
            city=city,
            state=state,
            zip_code=zip_code,
            committee_types_name=committee_types_name,
        )
    ]
    conn.execute(
        text(insert_query),
        *bind_params,
    )
    # we are in a transaction already due to pep idk one of them
    conn.commit()

    # NOTE: Redirect Path
    # Citation for the following code:
    # Date: 05/21/2023
    # Copied from /OR/ Adapted from /OR/ Based on:
    # https://stackoverflow.com/a/73088816
    return RedirectResponse(
        f"/{TABLE_NAME}/",
        status_code=status.HTTP_302_FOUND,
    )
