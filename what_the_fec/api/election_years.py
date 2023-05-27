from fastapi import Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection, text

from what_the_fec.api.columns_information import (
    get_columns_information_query,
    get_columns_information_dict
)


def get_all_election_years_func(
    conn: Connection, request: Request, templates: Jinja2Templates
):
    election_years_query = """
        SELECT * FROM election_years;
    """

    # had to dig this one up. its been a bit and this is never intuitive.
    # Citation for the following code:
    # Date: 05/20/2023
    # Copied from /OR/ Adapted from /OR/ Based on:
    # https://stackoverflow.com/a/58660606
    election_years = conn.execute(text(election_years_query)).mappings().all()
    columns_information_result = conn.execute(text(get_columns_information_query("election_years"))).mappings().all()
    columns_information=get_columns_information_dict(columns_information_result)

    return templates.TemplateResponse(
        "tables.j2",
        {
            "request": request,
            "items": election_years,
            "table_name": "election_years",
            "columns_information": columns_information,
        },
    )



