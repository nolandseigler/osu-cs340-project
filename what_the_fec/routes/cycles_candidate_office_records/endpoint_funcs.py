from fastapi import Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection, text

from what_the_fec.routes.helpers import intersection_render_table

TABLE_NAME = "cycles_candidate_office_records"


def get_all_func(conn: Connection, request: Request, templates: Jinja2Templates):
    entity_1_table_name = "cycles"
    entity_1_attribute = "year"
    
    entity_2_table_name = "candidate_office_records"
    entity_2_attribute = "fec_cand_id"

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
        SELECT * from cycles
    """

    entity_2_query = """
        SELECT
            `candidate_office_records`.id,
            fec_cand_id,
            `candidate_office_records`.name,
            ttl_receipts,
            trans_from_auth,
            coh_bop,
            coh_cop,
            cand_contrib,
            cand_loans,
            other_loans,
            cand_loan_repay,
            other_loan_repay,
            debts_owed_by,
            ttl_indiv_contrib,
            cand_office_st,
            cand_office_district,
            pol_pty_contrib,
            cvg_end_dt,
            indiv_refund,
            cmte_refund,
            `office_types`.name as office_type,
            `candidates`.email as candidate_email,
            `party_types`.short_name as party_type,
            `incumbent_challenger_statuses`.name as incumbent_challenger_status
        FROM `candidate_office_records`
            INNER JOIN `office_types` 
                ON `candidate_office_records`.office_types_id = `office_types`.id
            LEFT OUTER JOIN `candidates` 
                ON `candidate_office_records`.candidates_id = `candidates`.id
            INNER JOIN `party_types` 
                ON `candidate_office_records`.party_types_id = `party_types`.id
            INNER JOIN `incumbent_challenger_statuses` 
                ON `candidate_office_records`.incumbent_challenger_statuses_id = `incumbent_challenger_statuses`.id
    """

    entity_1_dropdown_selections_query = f"SELECT * FROM `{entity_1_table_name}`"
    entity_2_dropdown_selections_query = f"SELECT {entity_2_attribute} FROM `{entity_2_table_name}`"

    entity_1_dropdown_selections = conn.execute(text(entity_1_dropdown_selections_query)).mappings().all()
    entity_2_dropdown_selections = conn.execute(text(entity_2_dropdown_selections_query)).mappings().all()

    dropdown_items_for_add = {
        f"{entity_1_table_name}_{entity_1_attribute}": {
            "data": entity_1_dropdown_selections,
            "relevant_column_name": entity_1_attribute,
            "table_name": entity_1_table_name
        },
        entity_2_attribute: {
            "data": entity_2_dropdown_selections,
            "relevant_column_name": entity_2_attribute,
            "table_name": entity_2_table_name
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
        dropdown_items_for_add = dropdown_items_for_add
    )


def create_single_func(
    conn: Connection,
    cycles_year,
    fec_cand_id,
):
    insert_query = f"""
        INSERT INTO `{TABLE_NAME}`(
            cycles_year,
            candidate_office_records_id
        ) VALUES
            (
                :cycles_year,
                (
                    SELECT id FROM `candidate_office_records` 
                    WHERE fec_cand_id = :fec_cand_id
                )
            );
    """

    bind_params = [
        dict(
            cycles_year=cycles_year,
            fec_cand_id=fec_cand_id,
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
