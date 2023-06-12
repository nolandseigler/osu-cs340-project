from fastapi import HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection, text

from what_the_fec.routes.helpers import (
    intersection_render_table,
    intersection_render_table_row,
)

TABLE_NAME = "candidate_office_records_committees"


def get_all_func(conn: Connection, request: Request, templates: Jinja2Templates):
    # UI tablename order is backwards. this fits that order except when we
    # construct ids like left_id,right_id where left is the first table.
    # left -> candidate_office_records
    entity_1_table_name = "committees"
    entity_1_attribute = "cmte_id"

    entity_2_table_name = "candidate_office_records"
    entity_2_attribute = "fec_cand_id"

    query = f"""
        SELECT 
            `{entity_1_table_name}`.{entity_1_attribute} as `{entity_1_attribute}`,
            `{entity_2_table_name}`.{entity_2_attribute} as `{entity_2_attribute}`,
            `{entity_2_table_name}`.id as left_id,
            `{entity_1_table_name}`.id as right_id
        FROM `{TABLE_NAME}`
            INNER JOIN `{entity_1_table_name}` 
                ON `{TABLE_NAME}`.{entity_1_table_name}_id = `{entity_1_table_name}`.id
            INNER JOIN `{entity_2_table_name}` 
                ON `{TABLE_NAME}`.{entity_2_table_name}_id = `{entity_2_table_name}`.id
    """

    entity_1_query = f"""
        SELECT 
            `committees`.id,
            cmte_id,
            `committees`.name,
            city,
            state,
            zip_code,
            `committee_types`.name as committee_type
        FROM `committees`
            INNER JOIN `committee_types`
                ON `committees`.committee_types_id = `committee_types`.id
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

    entity_1_dropdown_selections_query = (
        f"SELECT {entity_1_attribute} FROM `{entity_1_table_name}`"
    )
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
        entity_1_attribute: {
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
    cmte_id,
    fec_cand_id,
):
    insert_query = f"""
        INSERT INTO `{TABLE_NAME}`(
            candidate_office_records_id,
            committees_id
        ) VALUES
            (
                (
                    SELECT id FROM `candidate_office_records` 
                    WHERE fec_cand_id = :fec_cand_id
                ),
                (
                    SELECT id FROM `committees` 
                    WHERE cmte_id = :cmte_id
                )
            )
    """

    bind_params = [
        dict(
            cmte_id=cmte_id,
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


def update_single_page_func(
    conn: Connection,
    request: Request,
    templates: Jinja2Templates,
    candidate_office_records_id: int,
    committees_id: int,
):
    entity_1_table_name = "committees"
    entity_1_attribute = "cmte_id"

    entity_2_table_name = "candidate_office_records"
    entity_2_attribute = "fec_cand_id"

    query = f"""
        SELECT 
            `{entity_1_table_name}`.{entity_1_attribute} as `{entity_1_attribute}`,
            `{entity_2_table_name}`.{entity_2_attribute} as `{entity_2_attribute}`
        FROM `{TABLE_NAME}`
            INNER JOIN `{entity_1_table_name}` 
                ON `{TABLE_NAME}`.{entity_1_table_name}_id = `{entity_1_table_name}`.id
            INNER JOIN `{entity_2_table_name}` 
                ON `{TABLE_NAME}`.{entity_2_table_name}_id = `{entity_2_table_name}`.id
        WHERE
            `{entity_1_table_name}`.id = :committees_id
            AND `{entity_2_table_name}`.id = :candidate_office_records_id
    """
    intersection_items = (
        conn.execute(
            text(query),
            *[
                dict(
                    candidate_office_records_id=candidate_office_records_id,
                    committees_id=committees_id,
                )
            ],
        )
        .mappings()
        .all()
    )
    if not intersection_items:
        raise HTTPException(
            status_code=404,
            detail=f"no {TABLE_NAME} record for provided record id: {candidate_office_records_id}_{committees_id}",
        )

    entity_1_query = f"""
        SELECT 
            `{entity_1_table_name}`.id,
            cmte_id,
            `{entity_1_table_name}`.name,
            city,
            state,
            zip_code,
            `committee_types`.name as committee_type
        FROM `{entity_1_table_name}`
            INNER JOIN `committee_types`
                ON `{entity_1_table_name}`.committee_types_id = `committee_types`.id
        WHERE
            `{entity_1_table_name}`.id = :committees_id
    """
    entity_1_items = (
        conn.execute(text(entity_1_query), *[dict(committees_id=committees_id)])
        .mappings()
        .all()
    )

    entity_2_query = f"""
        SELECT
            `{entity_2_table_name}`.id,
            fec_cand_id,
            `{entity_2_table_name}`.name,
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
        FROM `{entity_2_table_name}`
            INNER JOIN `office_types` 
                ON `{entity_2_table_name}`.office_types_id = `office_types`.id
            LEFT OUTER JOIN `candidates` 
                ON `{entity_2_table_name}`.candidates_id = `candidates`.id
            INNER JOIN `party_types` 
                ON `{entity_2_table_name}`.party_types_id = `party_types`.id
            INNER JOIN `incumbent_challenger_statuses` 
                ON `{entity_2_table_name}`.incumbent_challenger_statuses_id = `incumbent_challenger_statuses`.id
        WHERE
            `{entity_2_table_name}`.id = :candidate_office_records_id
    """
    entity_2_items = (
        conn.execute(
            text(entity_2_query),
            *[dict(candidate_office_records_id=candidate_office_records_id)],
        )
        .mappings()
        .all()
    )

    entity_1_dropdown_selections_query = f"""
        SELECT {entity_1_attribute}
        FROM `{entity_1_table_name}`
    """
    entity_1_dropdown_selections = (
        conn.execute(
            text(entity_1_dropdown_selections_query),
        )
        .mappings()
        .all()
    )

    entity_2_dropdown_selections_query = f"""
        SELECT {entity_2_attribute}
        FROM `{entity_2_table_name}`
    """
    entity_2_dropdown_selections = (
        conn.execute(
            text(entity_2_dropdown_selections_query),
        )
        .mappings()
        .all()
    )

    dropdown_items_for_add = {
        entity_1_attribute: {
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

    return intersection_render_table_row(
        conn=conn,
        intersection_items=intersection_items,
        request=request,
        table_name=TABLE_NAME,
        templates=templates,
        entity_1_table_name=entity_1_table_name,
        entity_1_items=entity_1_items,
        entity_2_table_name=entity_2_table_name,
        entity_2_items=entity_2_items,
        dropdown_keys=dropdown_items_for_add.keys(),
        dropdown_items_for_add=dropdown_items_for_add,
        left_id=candidate_office_records_id,
        right_id=committees_id,
    )


def update_single_func(
    conn: Connection,
    candidate_office_records_id: int,
    committees_id: int,
    updated_fec_cand_id: str,
    updated_cmte_id: str,
):
    update_sql = f"""
        UPDATE `{TABLE_NAME}`
        SET
            candidate_office_records_id = (
                SELECT id FROM `candidate_office_records` 
                WHERE fec_cand_id = :updated_fec_cand_id
            ),
            committees_id = (
                SELECT id FROM `committees` 
                WHERE cmte_id = :updated_cmte_id
            )
        WHERE
            candidate_office_records_id = :candidate_office_records_id
            AND committees_id = :committees_id
    """

    bind_params = [
        {
            "updated_fec_cand_id": updated_fec_cand_id,
            "updated_cmte_id": updated_cmte_id,
            "candidate_office_records_id": candidate_office_records_id,
            "committees_id": committees_id,
        },
    ]

    conn.execute(text(update_sql), *bind_params)
    # we are in a transaction already due to pep idk one of them
    conn.commit()

    bind_params = [
        {
            "updated_fec_cand_id": updated_fec_cand_id,
            "updated_cmte_id": updated_cmte_id,
        },
    ]
    result = (
        conn.execute(
            text(
                f"""
                SELECT candidate_office_records_id, committees_id
                FROM `{TABLE_NAME}`
                WHERE 
                    candidate_office_records_id = (
                        SELECT id FROM `candidate_office_records` 
                        WHERE fec_cand_id = :updated_fec_cand_id
                    )
                    AND committees_id = (
                        SELECT id FROM `committees` 
                        WHERE cmte_id = :updated_cmte_id
                    )
            """
            ),
            *bind_params,
        )
        .mappings()
        .one()
    )

    return RedirectResponse(
        f"/{TABLE_NAME}/update/{result['candidate_office_records_id']}_{result['committees_id']}",
        status_code=status.HTTP_302_FOUND,
    )
