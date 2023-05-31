from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection, text

from what_the_fec.routes.helpers import intersection_render_table

TABLE_NAME = "cycles_contributions"


def get_all_func(conn: Connection, request: Request, templates: Jinja2Templates):
    query = f"""
        SELECT * FROM {TABLE_NAME}
    """

    cycles_query = f"""
        SELECT * from cycles
    """

    contributions_query = f"""
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

    cycles_dropdown_selections_query = "SELECT * FROM `cycles`"
    contributions_dropdown_selections_query = "SELECT id FROM `contributions`"

    cycles_dropdown_selections = conn.execute(text(cycles_dropdown_selections_query)).mappings().all()
    contributions_dropdown_selections = conn.execute(text(contributions_dropdown_selections_query)).mappings().all()


    dropdown_items_for_add = {
        "cycles_year": {
            "data": cycles_dropdown_selections,
            "relevant_column_name": "year",
        },
        "contributions_id": {
            "data": contributions_dropdown_selections,
            "relevant_column_name": "id",
        },
    }

    return intersection_render_table(
        conn=conn,
        query=query,
        request=request,
        table_name=TABLE_NAME,
        templates=templates,
        entity_1_table_name="cycles",
        entity_1_query=cycles_query,
        entity_2_table_name="contributions",
        entity_2_query=contributions_query,
        dropdown_keys=dropdown_items_for_add.keys(),
        dropdown_items_for_add = dropdown_items_for_add

    )
