from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection, text

from what_the_fec.routes.helpers import generic_render_table

TABLE_NAME = "contributions"

def get_all_func(conn: Connection, request: Request, templates: Jinja2Templates):
    contributions_query = f"""
        SELECT 
            `{TABLE_NAME}`.id,
            transaction_pgi,
            image_num,
            transaction_dt,
            transaction_amt,
            trans_id,
            file_num,
            memo_cd,
            memo_text,
            sub_id,
            `committees`.name as committee,
            `report_types`.name as report_type,
            `transaction_types`.name as transaction_type,
            `amendment_indicators`.name as amendment_indicator,
            `contributor_types`.name as contributor_type
        FROM `{TABLE_NAME}`
            INNER JOIN `committees` 
                ON `{TABLE_NAME}`.committees_id = `committees`.id
            INNER JOIN `report_types` 
                ON `{TABLE_NAME}`.report_types_id = `report_types`.id
            INNER JOIN `transaction_types` 
                ON `{TABLE_NAME}`.transaction_types_id = `transaction_types`.id
            INNER JOIN `amendment_indicators` 
                ON `{TABLE_NAME}`.amendment_indicators_id = `amendment_indicators`.id
            INNER JOIN `contributor_types` 
                ON `{TABLE_NAME}`.contributor_types_id = `contributor_types`.id;
    """

    committees_query = "SELECT id, name FROM committees"

    report_types_query = "SELECT id, name FROM report_types"

    transaction_types_query = "SELECT id, name FROM transaction_types"

    amendment_indicators_query = "SELECT id, name FROM amendment_indicators"

    contributor_types_query = "SELECT id, name FROM contributor_types"

    # had to dig this one up. its been a bit and this is never intuitive.
    # Citation for the following code:
    # Date: 05/20/2023
    # Copied from /OR/ Adapted from /OR/ Based on:
    # https://stackoverflow.com/a/58660606
    committees = conn.execute(text(committees_query)).mappings().all()
    report_types = conn.execute(text(report_types_query)).mappings().all()
    transaction_types = conn.execute(text(transaction_types_query)).mappings().all()
    amendment_indicators = (
        conn.execute(text(amendment_indicators_query)).mappings().all()
    )
    contributor_types = (
        conn.execute(text(contributor_types_query)).mappings().all()
    )


    dropdown_items_for_add = {
        "committee": {
            "data": committees,
            "relevant_column_name": "name",
        },
        "report_type": {
            "data": report_types,
            "relevant_column_name": "name",
        },
        "amendment_indicator": {
            "data": amendment_indicators,
            "relevant_column_name": "name",
        },
        "transaction_type": {
            "data": transaction_types,
            "relevant_column_name": "name",
        },
        "contributor_type": {
            "data": contributor_types,
            "relevant_column_name": "name",
        },
    }

    return generic_render_table(
        conn=conn,
        query=contributions_query,
        request=request,
        table_name=TABLE_NAME,
        templates=templates,
        dropdown_keys=[
            "committee",
            "report_type",
            "transaction_type",
            "amendment_indicator",
            "contributor_type",
        ],
        dropdown_items_for_add=dropdown_items_for_add,
    )