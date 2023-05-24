from fastapi import Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection, text


def get_all_candidate_office_records_func(
    conn: Connection, request: Request, templates: Jinja2Templates
):
    candidate_office_records_query = """
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
        "candidate_office_records.j2",
        {
            "request": request,
            "items": candidate_office_records,
            "table_name": "candidate_office_records",
            "dropdown_keys": [
                "office_type",
                "candidate_email",
                "party_type",
                "incumbent_challenger_status",
            ],
            "dropdown_items_for_add": dropdown_items_for_add,
        },
    )


def edit_single_candidate_office_records_page_func(
    conn: Connection, request: Request, templates: Jinja2Templates, record_id
):
    candidate_office_records_query = """
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
        WHERE `candidate_office_records`.id = :candidate_office_records_id
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
        "edit_candidate_office_records.j2",
        {
            "request": request,
            "items": candidate_office_records,
            "table_name": "candidate_office_records",
            "dropdown_keys": [
                "office_type",
                "candidate_email",
                "party_type",
                "incumbent_challenger_status",
            ],
            "dropdown_items_for_add": dropdown_items_for_add,
        },
    )


def delete_single_candidate_office_records_page_func(
    conn: Connection, request: Request, templates: Jinja2Templates, record_id
):
    candidate_office_records_query = """
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
        WHERE `candidate_office_records`.id = :candidate_office_records_id
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
        "delete_candidate_office_records.j2",
        {
            "request": request,
            "items": candidate_office_records,
            "table_name": "candidate_office_records",
            "dropdown_keys": [
                "office_type",
                "candidate_email",
                "party_type",
                "incumbent_challenger_status",
            ],
        },
    )


def post_single_candidate_office_records_func(
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
        candidates_email_populator = "NULL"
    else:
        candidates_email_populator = (
            f"(SELECT id FROM `candidates` WHERE email = '{candidate_email}')"
        )

    insert_query = f"""
        INSERT INTO `candidate_office_records` (
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
            '{fec_cand_id}',
            '{name}',
            {ttl_receipts},
            {trans_from_auth},
            {coh_bop},
            {coh_cop},
            {cand_contrib},
            {cand_loans},
            {other_loans},
            {cand_loan_repay},
            {other_loan_repay},
            {debts_owed_by},
            {ttl_indiv_contrib},
            '{cand_office_st}',
            '{cand_office_district}',
            {pol_pty_contrib},
            '{cvg_end_dt}',
            {indiv_refund},
            {cmte_refund},
            (SELECT id FROM `office_types` WHERE name = '{office_type}'),
            {candidates_email_populator},
            (SELECT id FROM `party_types` WHERE short_name = '{party_type}'),
            (SELECT id FROM `incumbent_challenger_statuses` WHERE name = '{incumbent_challenger_status}')
        )
    """

    # TODO: Use bind params
    conn.execute(text(insert_query))
    # we are in a transaction already due to pep idk one of them
    conn.commit()

    # NOTE: Redirect Path
    # Citation for the following code:
    # Date: 05/21/2023
    # Copied from /OR/ Adapted from /OR/ Based on:
    # https://stackoverflow.com/a/73088816
    return RedirectResponse(
        "/candidate_office_records",
        status_code=status.HTTP_302_FOUND,
    )


def update_single_candidate_office_records_func(
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

    update_sql = """
        UPDATE `candidate_office_records`
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
        f"/edit_candidate_office_records/{record_id}",
        status_code=status.HTTP_302_FOUND,
    )


def delete_single_candidate_office_records_func(
    conn: Connection,
    record_id,
):
    delete_sql = """
        DELETE FROM `candidate_office_records`
        WHERE id = :candidate_office_records_id
    """

    bind_params = [
        {"candidate_office_records_id": record_id},
    ]

    conn.execute(text(delete_sql), *bind_params)
    # we are in a transaction already due to pep idk one of them
    conn.commit()

    return RedirectResponse(
        "/candidate_office_records",
        status_code=status.HTTP_302_FOUND,
    )
