from fastapi import Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection, text

from what_the_fec.routes.helpers import intersection_render_table

TABLE_NAME = "election_years_contributions"


def get_all_func(conn: Connection, request: Request, templates: Jinja2Templates):
    query = f"""
        SELECT * FROM {TABLE_NAME}
    """

    election_years_query = f"""
        SELECT * from election_years
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

    election_years_dropdown_selections_query = "SELECT * FROM `election_years`"
    contributions_dropdown_selections_query = "SELECT id FROM `contributions`"

    election_years_dropdown_selections = (
        conn.execute(text(election_years_dropdown_selections_query)).mappings().all()
    )
    contributions_dropdown_selections = (
        conn.execute(text(contributions_dropdown_selections_query)).mappings().all()
    )

    dropdown_items_for_add = {
        "election_years_year": {
            "data": election_years_dropdown_selections,
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
        entity_1_table_name="election_years",
        entity_1_query=election_years_query,
        entity_2_table_name="contributions",
        entity_2_query=contributions_query,
        dropdown_keys=dropdown_items_for_add.keys(),
        dropdown_items_for_add=dropdown_items_for_add,
    )


def create_single_func(
    conn: Connection,
    election_years_year,
    contributions_id,
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
                    WHERE id = :contributions_id
                )
            );
    """

    bind_params = [
        dict(
            election_years_year=election_years_year,
            contributions_id=contributions_id,
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
