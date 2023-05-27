from fastapi import Request
from fastapi.templating import Jinja2Templates

TABLES_INFORMATION = {
    "office_types": {
        "type": "category",
        "description": "represents the office type the candidate ran for in the election or occupies during the cycle",
    },
    "contributor_types": {
        "type": "category",
        "description": "represents the specific type of contributor",
    },
    "committee_types": {
        "type": "category",
        "description": "represents the specific type of committee. Refer to: https://www.fec.gov/campaign-finance-data/committee-type-code-descriptions/",
    },
    "transaction_types": {
        "type": "category",
        "description": "represents the transaction type used in data uploads to the system. useful for linking documents uploaded as part of a single transaction",
    },
    "report_types": {
        "type": "category",
        "description": "represents the report code applicable to each committee or individual contribution.",
    },
    "party_types": {
        "type": "category",
        "description": "the political national political party associated with the candidate_office_records. not to be confused with Party Committees and PACs Note: for now in the name of simplicity we will parse this off of position 3 and 4 from here: https://www.fec.gov/campaign-finance-data/all-candidates-file-description/",
    },
    "incumbent_challenger_statuses": {
        "type": "category",
        "description": "represents the report code applicable to each committee or individual contribution",
    },
    "amendment_indicators": {
        "type": "category",
        "description": "indicates if the type of report(as part of a contribution transaction) being filed",
    },
    "cycles": {
        "type": "category",
        "description": "the election cycle year. It is an even number with two year intervals. The cycle begins on the odd year and ends on the even year. Example 2001-2002 -> year = 2002",
    },
    "election_years": {
        "type": "category",
        "description": "the year that the election takes place in",
    },
    "candidates": {
        "type": "entity",
        "description": "represents the actual person that is the candidate. One record per person",
    },
    "candidate_office_records": {
        "type": "entity",
        "description": "a FEC candidate record represents the elections + time spent in office(cycles) for a person for a specific office. A single person will have one candidate_office_record per office they ran for",
    },
    "committees": {
        "type": "entity",
        "description": "a committee is defined by the Federal Register as “any group of persons that receives more than $1,000 in contributions or makes more than $1,000 in expenditures during a calendar year. Refer to https://www.fec.gov/campaign-finance-data/contributions-individuals-file-description/ and https://www.fec.gov/campaign-finance-data/ contributions-committees-candidates-file-description/",
    },
    "contributions": {
        "type": "entity",
        "description": "contributions from individuals or committees. includes independent expenditures",
    },
    "candidate_office_records_committees": {
        "type": "intersection",
        "description": "intersection of candidate_office_records and committees",
    },
    "candidate_office_records_contributions": {
        "type": "intersection",
        "description": "intersection of candidate_office_records and contributions",
    },
    "election_years_contributions": {
        "type": "intersection",
        "description": "intersection of election_years and contributions",
    },
    "election_years_candidate_office_records": {
        "type": "intersection",
        "description": "intersection of election_years and candidate office_records",
    },
    "cycles_contributions": {
        "type": "intersection",
        "description": "intersection of cycles and contributions",
    },
    "cycles_candidate_office_records": {
        "type": "intersection",
        "description": "intersection of cycles and candidate office records",
    },
}


def home_page_func(request: Request, templates: Jinja2Templates):
    return templates.TemplateResponse(
        "home.j2",
        {
            "request": request,
            "tables_information": TABLES_INFORMATION,
        },
    )
