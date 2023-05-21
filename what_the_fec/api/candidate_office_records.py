from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection, text


def get_all_candidate_office_records_func(conn: Connection, request: Request, templates: Jinja2Templates):
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
                ON `candidate_office_records`.incumbent_challenger_statuses_id = `incumbent_challenger_statuses`.id;
    """

    office_types_query = "SELECT id, name FROM office_types;"

    candidates_query = "SELECT id, email FROM candidates;"

    party_types_query = "SELECT id, short_name FROM party_types;"

    incumbent_challenger_statuses_query = "SELECT id, name FROM incumbent_challenger_statuses;"

    # had to dig this one up. its been a bit and this is never intuitive.
    # Citation for the following code:
    # Date: 05/20/2023
    # Copied from /OR/ Adapted from /OR/ Based on:
    # https://stackoverflow.com/a/58660606
    candidate_office_records = conn.execute(text(candidate_office_records_query)).mappings().all()
    office_types = conn.execute(text(office_types_query)).mappings().all()
    candidates = conn.execute(text(candidates_query)).mappings().all()
    party_types = conn.execute(text(party_types_query)).mappings().all()
    incumbent_challenger_statuses = conn.execute(text(incumbent_challenger_statuses_query)).mappings().all()

    
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
            "dropdown_keys": ["office_type", "candidate_email", "party_type", "incumbent_challenger_status"],
            "dropdown_items_for_add": dropdown_items_for_add,
        }
    )