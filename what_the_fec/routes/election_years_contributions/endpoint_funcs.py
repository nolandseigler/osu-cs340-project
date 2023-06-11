from fastapi import Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection, text

from what_the_fec.routes.helpers import intersection_render_table

TABLE_NAME = "election_years_contributions"


def get_all_func(conn: Connection, request: Request, templates: Jinja2Templates):
    entity_1_table_name = "election_years"
    entity_1_attribute = "year"

    entity_2_table_name = "contributions"
    entity_2_attribute = "sub_id"

    query = f"""
        SELECT 
            `{entity_1_table_name}`.{entity_1_attribute} as `{entity_1_table_name}_{entity_1_attribute}`,
            `{entity_2_table_name}`.{entity_2_attribute} as `{entity_2_attribute}`
        FROM `{TABLE_NAME}`
            INNER JOIN `{entity_1_table_name}` 
                ON `{TABLE_NAME}`.{entity_1_table_name}_year = `{entity_1_table_name}`.year
            INNER JOIN `{entity_2_table_name}` 
                ON `{TABLE_NAME}`.{entity_2_table_name}_id = `{entity_2_table_name}`.id
    """

    entity_1_query = f"""
        SELECT * from election_years
    """

    entity_2_query = f"""
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

    entity_1_dropdown_selections_query = f"SELECT * FROM `{entity_1_table_name}`"
    entity_2_dropdown_selections_query = (
        f"SELECT {entity_2_attribute} FROM `{entity_2_table_name}`"
    )

    entity_1_dropdown_selections = (
        conn.execute(text(entity_1_dropdown_selections_query)).mappings().all()
    )
    entity_2_dropdown_selections = (
        conn.execute(text(entity_2_dropdown_selections_query)).mappings().all()
    )

    dropdown_items_for_add = {
        f"{entity_1_table_name}_{entity_1_attribute}": {
            "data": entity_1_dropdown_selections,
            "relevant_column_name": entity_1_attribute,
            "table_name": entity_1_table_name,
        },
        entity_2_attribute: {
            "data": entity_2_dropdown_selections,
            "relevant_column_name": entity_2_attribute,
            "table_name": entity_2_table_name,
        },
    }

    return intersection_render_table(
        conn=conn,
        query=query,
        request=request,
        table_name=TABLE_NAME,
        templates=templates,
        entity_1_table_name=entity_1_table_name,
        entity_1_query=entity_1_query,
        entity_2_table_name=entity_2_table_name,
        entity_2_query=entity_2_query,
        dropdown_keys=dropdown_items_for_add.keys(),
        dropdown_items_for_add=dropdown_items_for_add,
    )


def create_single_func(
    conn: Connection,
    election_years_year,
    sub_id,
):
    insert_query = f"""
        INSERT INTO `{TABLE_NAME}`(
            election_years_year,
            contributions_id
        ) VALUES
            (
                (
                    SELECT year FROM `election_years` 
                    WHERE year = :election_years_year
                ),
                (
                    SELECT id FROM `contributions` 
                    WHERE sub_id = :sub_id
                )
            );
    """

    bind_params = [
        dict(
            election_years_year=election_years_year,
            sub_id=sub_id,
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
