TABLES_INFORMATION = {
    "office_types": {
        "type": "category",
        "description": "Represents the office type the candidate ran for in the election or occupies during the cycle.",
    },
    "contributor_types": {
        "type": "category",
        "description": "Represents the specific type of contributor.",
    },
    "committee_types": {
        "type": "category",
        "description": "Represents the specific type of committee. Refer to: https://www.fec.gov/campaign-finance-data/committee-type-code-descriptions/",
    },
    "transaction_types": {
        "type": "category",
        "description": "Represents the transaction type used in data uploads to the system. Useful for linking documents uploaded as part of a single transaction.",
    },
    "report_types": {
        "type": "category",
        "description": "Represents the report code applicable to each committee or individual contribution.",
    },
    "party_types": {
        "type": "category",
        "description": "The political national political party associated with the candidate_office_records. not to be confused with Party Committees and PACs Note: for now in the name of simplicity we will parse this off of position 3 and 4 from here: https://www.fec.gov/campaign-finance-data/all-candidates-file-description/",
    },
    "incumbent_challenger_statuses": {
        "type": "category",
        "description": "Represents the report code applicable to each committee or individual contribution.",
    },
    "amendment_indicators": {
        "type": "category",
        "description": "Indicates the type of report (as part of a contribution transaction) being filed.",
    },
    "cycles": {
        "type": "category",
        "description": "The election cycle year. It is an even number with two year intervals. The cycle begins on the odd year and ends on the even year. Example: 2001-2002 -> year = 2002.",
    },
    "election_years": {
        "type": "category",
        "description": "The year that the election takes place in.",
    },
    "candidates": {
        "type": "entity",
        "description": "Represents the actual person that is the candidate. One record per person.",
    },
    "candidate_office_records": {
        "type": "entity",
        "description": "An FEC candidate record represents the elections and time spent in office(cycles) for a person for a specific office. A single person will have one candidate_office_record per office they ran for.",
        "attributes": {
            "fec_cand_id": "candidate identification",
            "name": "name on candidate office record",
            "ttl_receipts": "total receipts	",
            "trans_from_auth": "transfers from authorized committees",
            "ttl_disb": "total disbursements",
            "trans_to_auth": "transfers to authorized committees",
            "coh_bop": "beginning cash",
            "coh_cop": "ending cash",
            "cand_contrib": "contributions from candidate",
            "cand_loans": "loans from candidate",
            "other_loans": "other loans",
            "cand_loan_repay": "candidate loan repayments",
            "other_loan_repay": "other loan repayments",
            "debts_owed_by": "debts owed by",
            "ttl_indiv_contrib": "total individual contributions",
            "cand_office_st": "candidate state",
            "cand_office_district": "candidate district",
            "pol_pty_contrib": "contributions from party committees",
            "cvg_end_dt": "coverage end date",
            "indiv_refund": "refunds to individuals",
            "cmte_refund": "refunds to committees",
            "office_type": "the office type the candidate ran for in the election or occupies during the cycle",
            "candidate_email": "email associated with Candidate (entity)",
            "party_type": "associated party code",
            "incumbent_challenger_status": "incumbent challenger status",
        },
    },
    "committees": {
        "type": "entity",
        "description": "A committee is defined by the Federal Register as “any group of persons that receives more than $1,000 in contributions or makes more than $1,000 in expenditures during a calendar year. Refer to https://www.fec.gov/campaign-finance-data/contributions-individuals-file-description/ and https://www.fec.gov/campaign-finance-data/ contributions-committees-candidates-file-description/",
        "attributes": {
            "cmte_id": "A 9-character alpha-numeric code assigned to a committee by the Federal Election Commission. Committee IDs are unique and an ID for a specific committee always remains the same.",
            "committee_type": "Represents the specific type of committee",
        },
    },
    "contributions": {
        "type": "entity",
        "description": "Contributions from individuals or committees. includes independent expenditures.",
        "attributes": {
            "transaction_pgi": "primary-general indicator",
            "image_num": "image number",
            "transaction_dt": "transaction date",
            "transaction_amt": "transaction amount",
            "trans_id": "transaction ID",
            "file_num": "file number / report ID",
            "memo_cd": "memo code",
            "memo_text": "memo text",
            "sub_id": "FEC record number",
            "cmte_id": "filer identification number",
            "report_type": "represents the report code applicable to each committee or individual contribution",
            "transaction_type": "represents the transaction type used in data uploads to the system",
            "amendment_indicator": "indicates the type of report (as part of a contribution transaction) being filed",
            "contributor_type": "represents the specific type of contributor",
        },
    },
    "candidate_office_records_committees": {
        "type": "intersection",
        "description": "Intersection of candidate_office_records and committees.",
    },
    "candidate_office_records_contributions": {
        "type": "intersection",
        "description": "Intersection of candidate_office_records and contributions.",
    },
    "election_years_contributions": {
        "type": "intersection",
        "description": "Intersection of election_years and contributions.",
    },
    "election_years_candidate_office_records": {
        "type": "intersection",
        "description": "Intersection of election_years and candidate office_records.",
    },
    "cycles_contributions": {
        "type": "intersection",
        "description": "Intersection of cycles and contributions.",
    },
    "cycles_candidate_office_records": {
        "type": "intersection",
        "description": "Intersection of cycles and candidate office records.",
    },
}
