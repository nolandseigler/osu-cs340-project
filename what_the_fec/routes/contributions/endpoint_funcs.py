from fastapi import Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection, text

from what_the_fec.routes.helpers import (
    get_columns_information_dict,
    get_columns_information_query,
)


def get_all(conn: Connection, request: Request, templates: Jinja2Templates):
    contributions_query = """
        SELECT 
            `contributions`.id,
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
        FROM `contributions`
            INNER JOIN `committees` 
                ON `contributions`.committees_id = `committees`.id
            INNER JOIN `report_types` 
                ON `contributions`.report_types_id = `report_types`.id
            INNER JOIN `transaction_types` 
                ON `contributions`.transaction_types_id = `transaction_types`.id
            INNER JOIN `amendment_indicators` 
                ON `contributions`.amendment_indicators_id = `amendment_indicators`.id
            INNER JOIN `contributor_types` 
                ON `contributions`.contributor_types_id = `contributor_types`.id;
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
    contributions = (
        conn.execute(text(contributions_query)).mappings().all()
    )
    committees = conn.execute(text(committees_query)).mappings().all()
    report_types = conn.execute(text(report_types_query)).mappings().all()
    transaction_types = conn.execute(text(transaction_types_query)).mappings().all()
    amendment_indicators = (
        conn.execute(text(amendment_indicators_query)).mappings().all()
    )
    contributor_types = (
        conn.execute(text(contributor_types_query)).mappings().all()
    )
    columns_information_result = (
        conn.execute(text(get_columns_information_query("contributions")))
        .mappings()
        .all()
    )
    columns_information = get_columns_information_dict(columns_information_result)

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

    return templates.TemplateResponse(
        "contributions/read.j2",
        {
            "request": request,
            "items": contributions,
            "table_name": "contributions",
            "dropdown_keys": [
                "committee",
                "report_type",
                "transaction_type",
                "amendment_indicator",
                "contributor_type",
            ],
            "dropdown_items_for_add": dropdown_items_for_add,
            "columns_information": columns_information,
        },
    )