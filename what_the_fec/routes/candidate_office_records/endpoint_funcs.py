import structlog
from fastapi import HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection, text
from what_the_fec.routes.common.tables_information import TABLES_INFORMATION

from what_the_fec.routes.helpers import (
    get_columns_information_dict,
    get_columns_information_query,
)

logger: structlog.types.FilteringBoundLogger = structlog.get_logger(__name__)
TABLE_NAME = "candidate_office_records"


def get_all_func(conn: Connection, request: Request, templates: Jinja2Templates):
    candidate_office_records_query = f"""
        SELECT
            `{TABLE_NAME}`.id,
            fec_cand_id,
            `{TABLE_NAME}`.name,
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
        FROM `{TABLE_NAME}`
            INNER JOIN `office_types` 
                ON `{TABLE_NAME}`.office_types_id = `office_types`.id
            LEFT OUTER JOIN `candidates` 
                ON `{TABLE_NAME}`.candidates_id = `candidates`.id
            INNER JOIN `party_types` 
                ON `{TABLE_NAME}`.party_types_id = `party_types`.id
            INNER JOIN `incumbent_challenger_statuses` 
                ON `{TABLE_NAME}`.incumbent_challenger_statuses_id = `incumbent_challenger_statuses`.id
    """

    office_types_query = "SELECT id, name FROM office_types"

    candidates_query = "SELECT id, email FROM candidates"

    party_types_query = "SELECT id, short_name FROM party_types"

    incumbent_challenger_statuses_query = (
        "SELECT id, name FROM incumbent_challenger_statuses"
    )

    # had to dig this one up. its been a bit and this is never intuitive.
    # Citation for the following code:
    # Date: 05/20/2023
    # Copied from /OR/ Adapted from /OR/ Based on:
    # https://stackoverflow.com/a/58660606
    candidate_office_records = (
        conn.execute(text(candidate_office_records_query)).mappings().all()
    )
    office_types = conn.execute(text(office_types_query)).mappings().all()
    candidates = conn.execute(text(candidates_query)).mappings().all()
    party_types = conn.execute(text(party_types_query)).mappings().all()
    incumbent_challenger_statuses = (
        conn.execute(text(incumbent_challenger_statuses_query)).mappings().all()
    )
    columns_information_result = (
        conn.execute(text(get_columns_information_query(table_name=TABLE_NAME)))
        .mappings()
        .all()
    )
    columns_information = get_columns_information_dict(columns_information_result)

    dropdown_items_for_add = {
        "office_type": {
            "data": office_types,
            "relevant_column_name": "name",
        },
        "candidate_email": {
            "data": candidates,
            "relevant_column_name": "email",
        },
        "party_type": {
            "data": party_types,
            "relevant_column_name": "short_name",
        },
        "incumbent_challenger_status": {
            "data": incumbent_challenger_statuses,
            "relevant_column_name": "name",
        },
    }

    return templates.TemplateResponse(
        f"{TABLE_NAME}/read.j2",
        {
            "request": request,
            "items": candidate_office_records,
            "table_name": TABLE_NAME,
            "dropdown_keys": [
                "office_type",
                "candidate_email",
                "party_type",
                "incumbent_challenger_status",
            ],
            "dropdown_items_for_add": dropdown_items_for_add,
            "columns_information": columns_information,
            "table_information": TABLES_INFORMATION[TABLE_NAME]
        },
    )


def create_single_func(
    conn: Connection,
    fec_cand_id,
    name,
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
    office_type,
    candidate_email,
    party_type,
    incumbent_challenger_status,
):
    if candidate_email == "none":
        logger.debug("no candidate email provided")
        candidates_id = None
    else:
        logger.debug("candidate email provided")
        candidates_email_populator = (
            f"SELECT id FROM `candidates` WHERE email = :candidate_email"
        )
        bind_params = [dict(candidate_email=candidate_email)]
        # had to dig this one up. its been a bit and this is never intuitive.
        # Citation for the following code:
        # Date: 05/20/2023
        # Copied from /OR/ Adapted from /OR/ Based on:
        # https://stackoverflow.com/a/58660606
        result = (
            conn.execute(
                text(candidates_email_populator),
                *bind_params,
            )
            .mappings()
            .one_or_none()
        )
        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"no candidates record for provided candidate email; candidate email: {candidate_email}",
            )
        candidates_id = result["id"]

    insert_query = f"""
        INSERT INTO `{TABLE_NAME}` (
            fec_cand_id,
            name,
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
            office_types_id,
            candidates_id,
            party_types_id,
            incumbent_challenger_statuses_id
        ) VALUES (
            :fec_cand_id,
            :name,
            :ttl_receipts,
            :trans_from_auth,
            :coh_bop,
            :coh_cop,
            :cand_contrib,
            :cand_loans,
            :other_loans,
            :cand_loan_repay,
            :other_loan_repay,
            :debts_owed_by,
            :ttl_indiv_contrib,
            :cand_office_st,
            :cand_office_district,
            :pol_pty_contrib,
            :cvg_end_dt,
            :indiv_refund,
            :cmte_refund,
            (SELECT id FROM `office_types` WHERE name = :office_type),
            :candidates_id,
            (SELECT id FROM `party_types` WHERE short_name = :party_type),
            (SELECT id FROM `incumbent_challenger_statuses` WHERE name = :incumbent_challenger_status)
        )
    """

    bind_params = [
        dict(
            fec_cand_id=fec_cand_id,
            name=name,
            ttl_receipts=ttl_receipts,
            trans_from_auth=trans_from_auth,
            coh_bop=coh_bop,
            coh_cop=coh_cop,
            cand_contrib=cand_contrib,
            cand_loans=cand_loans,
            other_loans=other_loans,
            cand_loan_repay=cand_loan_repay,
            other_loan_repay=other_loan_repay,
            debts_owed_by=debts_owed_by,
            ttl_indiv_contrib=ttl_indiv_contrib,
            cand_office_st=cand_office_st,
            cand_office_district=cand_office_district,
            pol_pty_contrib=pol_pty_contrib,
            cvg_end_dt=cvg_end_dt,
            indiv_refund=indiv_refund,
            cmte_refund=cmte_refund,
            office_type=office_type,
            candidate_email=candidate_email,
            party_type=party_type,
            incumbent_challenger_status=incumbent_challenger_status,
            candidates_id=candidates_id,
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
    conn: Connection, request: Request, templates: Jinja2Templates, record_id
):
    candidate_office_records_query = f"""
        SELECT
            `{TABLE_NAME}`.id,
            fec_cand_id,
            `{TABLE_NAME}`.name,
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
        FROM `{TABLE_NAME}`
            INNER JOIN `office_types` 
                ON `{TABLE_NAME}`.office_types_id = `office_types`.id
            LEFT OUTER JOIN `candidates` 
                ON `{TABLE_NAME}`.candidates_id = `candidates`.id
            INNER JOIN `party_types` 
                ON `{TABLE_NAME}`.party_types_id = `party_types`.id
            INNER JOIN `incumbent_challenger_statuses` 
                ON `{TABLE_NAME}`.incumbent_challenger_statuses_id = `incumbent_challenger_statuses`.id
        WHERE `{TABLE_NAME}`.id = :candidate_office_records_id
    """

    bind_params = [dict(candidate_office_records_id=record_id)]
    # had to dig this one up. its been a bit and this is never intuitive.
    # Citation for the following code:
    # Date: 05/20/2023
    # Copied from /OR/ Adapted from /OR/ Based on:
    # https://stackoverflow.com/a/58660606
    candidate_office_records = (
        conn.execute(
            text(candidate_office_records_query),
            *bind_params,
        )
        .mappings()
        .all()
    )

    candidates_query = "SELECT id, email FROM candidates"
    candidates = conn.execute(text(candidates_query)).mappings().all()
    dropdown_items_for_add = {
        "candidate_email": {
            "data": candidates,
            "relevant_column_name": "email",
        },
    }

    return templates.TemplateResponse(
        f"{TABLE_NAME}/update.j2",
        {
            "request": request,
            "items": candidate_office_records,
            "table_name": TABLE_NAME,
            "dropdown_keys": [
                "office_type",
                "candidate_email",
                "party_type",
                "incumbent_challenger_status",
            ],
            "dropdown_items_for_add": dropdown_items_for_add,
        },
    )


def update_single_func(
    conn: Connection,
    record_id,
    candidate_email: str,
):
    if candidate_email.lower() == "null":
        candidates_id = None
    else:
        candidates_id_query = """
            SELECT id
            FROM `candidates`
            WHERE email = :candidate_email
        """
        candidates_id_result = (
            conn.execute(
                text(candidates_id_query), *[{"candidate_email": candidate_email}]
            )
            .mappings()
            .one_or_none()
        )
        if candidates_id_result is not None:
            candidates_id = candidates_id_result["id"]
        else:
            candidates_id = None

    update_sql = f"""
        UPDATE `{TABLE_NAME}`
            SET candidates_id = :candidates_id
        WHERE id = :candidate_office_records_id
    """

    bind_params = [
        {"candidates_id": candidates_id, "candidate_office_records_id": record_id},
    ]

    conn.execute(text(update_sql), *bind_params)
    # we are in a transaction already due to pep idk one of them
    conn.commit()

    return RedirectResponse(
        f"/{TABLE_NAME}/update/{record_id}/",
        status_code=status.HTTP_302_FOUND,
    )


def delete_single_page_func(
    conn: Connection, request: Request, templates: Jinja2Templates, record_id
):
    candidate_office_records_query = f"""
        SELECT
            `{TABLE_NAME}`.id,
            fec_cand_id,
            `{TABLE_NAME}`.name,
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
        FROM `{TABLE_NAME}`
            INNER JOIN `office_types` 
                ON `{TABLE_NAME}`.office_types_id = `office_types`.id
            LEFT OUTER JOIN `candidates` 
                ON `{TABLE_NAME}`.candidates_id = `candidates`.id
            INNER JOIN `party_types` 
                ON `{TABLE_NAME}`.party_types_id = `party_types`.id
            INNER JOIN `incumbent_challenger_statuses` 
                ON `{TABLE_NAME}`.incumbent_challenger_statuses_id = `incumbent_challenger_statuses`.id
        WHERE `{TABLE_NAME}`.id = :candidate_office_records_id
    """

    bind_params = [dict(candidate_office_records_id=record_id)]
    # had to dig this one up. its been a bit and this is never intuitive.
    # Citation for the following code:
    # Date: 05/20/2023
    # Copied from /OR/ Adapted from /OR/ Based on:
    # https://stackoverflow.com/a/58660606
    candidate_office_records = (
        conn.execute(
            text(candidate_office_records_query),
            *bind_params,
        )
        .mappings()
        .all()
    )

    return templates.TemplateResponse(
        f"{TABLE_NAME}/delete.j2",
        {
            "request": request,
            "items": candidate_office_records,
            "table_name": TABLE_NAME,
            "dropdown_keys": [
                "office_type",
                "candidate_email",
                "party_type",
                "incumbent_challenger_status",
            ],
        },
    )


def delete_single_func(
    conn: Connection,
    record_id,
):
    delete_sql = f"""
        DELETE FROM `{TABLE_NAME}`
        WHERE id = :candidate_office_records_id
    """

    bind_params = [
        {"candidate_office_records_id": record_id},
    ]

    conn.execute(text(delete_sql), *bind_params)
    # we are in a transaction already due to pep idk one of them
    conn.commit()

    return RedirectResponse(
        f"/{TABLE_NAME}/",
        status_code=status.HTTP_302_FOUND,
    )
