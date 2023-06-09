from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection, text

from what_the_fec.routes.common.tables_information import TABLES_INFORMATION


# TODO: https://github.com/nolandseigler/osu-cs340-project/pull/7#discussion_r1206133030
def get_columns_information_query(table_name):
    return f"""
        SELECT 
            COLUMN_NAME, 
            DATA_TYPE, 
            CHARACTER_MAXIMUM_LENGTH, 
            COLUMN_DEFAULT, 
            IS_NULLABLE 
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE table_name = '{table_name}' AND COLUMN_NAME != "id"
        """


def get_columns_information_dict(columns_information_list):
    columns_information_dict = {}
    for entry in columns_information_list:
        columns_information_dict[entry["COLUMN_NAME"]] = {
            "DATA_TYPE": entry["DATA_TYPE"],
            "CHARACTER_MAXIMUM_LENGTH": entry["CHARACTER_MAXIMUM_LENGTH"],
            "COLUMN_DEFAULT": entry["COLUMN_DEFAULT"],
            "IS_NULLABLE": entry["IS_NULLABLE"],
        }

    return columns_information_dict


def generic_render_table(
    conn: Connection,
    query: str,
    request: Request,
    table_name: str,
    templates: Jinja2Templates,
    dropdown_keys=[],
    dropdown_items_for_add={},
):
    # had to dig this one up. its been a bit and this is never intuitive.
    # Citation for the following code:
    # Date: 05/20/2023
    # Copied from /OR/ Adapted from /OR/ Based on:
    # https://stackoverflow.com/a/58660606
    items = conn.execute(text(query)).mappings().all()
    columns_information_result = (
        conn.execute(text(get_columns_information_query(table_name=table_name)))
        .mappings()
        .all()
    )
    columns_information = get_columns_information_dict(columns_information_result)

    return templates.TemplateResponse(
        "tables.j2",
        {
            "request": request,
            "items": items,
            "table_name": table_name,
            "columns_information": columns_information,
            "dropdown_keys": dropdown_keys,
            "dropdown_items_for_add": dropdown_items_for_add,
            "table_information": TABLES_INFORMATION[table_name],
            "render_edit": False,
            "render_delete": False,
        },
    )


def intersection_render_table(
    conn: Connection,
    query: str,
    request: Request,
    table_name: str,
    templates: Jinja2Templates,
    entity_1_table_name,
    entity_1_query,
    entity_2_table_name,
    entity_2_query,
    dropdown_keys=None,
    dropdown_items_for_add=None,
):
    if not dropdown_keys:
        dropdown_keys = []
    if not dropdown_items_for_add:
        dropdown_items_for_add = {}
    # had to dig this one up. its been a bit and this is never intuitive.
    # Citation for the following code:
    # Date: 05/20/2023
    # Copied from /OR/ Adapted from /OR/ Based on:
    # https://stackoverflow.com/a/58660606
    items = conn.execute(text(query)).mappings().all()

    entity_1 = conn.execute(text(entity_1_query)).mappings().all()
    entity_2 = conn.execute(text(entity_2_query)).mappings().all()

    columns_information_result = (
        conn.execute(text(get_columns_information_query(table_name=table_name)))
        .mappings()
        .all()
    )
    columns_information = get_columns_information_dict(columns_information_result)

    # NOTE: yeah this is gross but this is essentially the last day of the project last minute :D
    if table_name == "candidate_office_records_committees":
        columns_information["left_id"] = {
            "DATA_TYPE": "int",
            "CHARACTER_MAXIMUM_LENGTH": None,
            "COLUMN_DEFAULT": None,
            "IS_NULLABLE": "NO",
        }
        columns_information["right_id"] = {
            "DATA_TYPE": "int",
            "CHARACTER_MAXIMUM_LENGTH": None,
            "COLUMN_DEFAULT": None,
            "IS_NULLABLE": "NO",
        }
        return templates.TemplateResponse(
            f"{table_name}/read.j2",
            {
                "request": request,
                "items": items,
                "table_name": table_name,
                "columns_information": columns_information,
                "dropdown_keys": dropdown_keys,
                "dropdown_items_for_add": dropdown_items_for_add,
                "entity_1_table_name": entity_1_table_name,
                "entity_1": entity_1,
                "entity_2_table_name": entity_2_table_name,
                "entity_2": entity_2,
                "table_information": TABLES_INFORMATION[table_name],
                "render_edit_intersection": True,
            },
        )

    return templates.TemplateResponse(
        "intersection_tables.j2",
        {
            "request": request,
            "items": items,
            "table_name": table_name,
            "columns_information": columns_information,
            "dropdown_keys": dropdown_keys,
            "dropdown_items_for_add": dropdown_items_for_add,
            "entity_1_table_name": entity_1_table_name,
            "entity_1": entity_1,
            "entity_2_table_name": entity_2_table_name,
            "entity_2": entity_2,
            "table_information": TABLES_INFORMATION[table_name],
        },
    )


def intersection_render_table_row(
    conn: Connection,
    intersection_items: list[dict],
    request: Request,
    table_name: str,
    templates: Jinja2Templates,
    entity_1_table_name,
    entity_1_items: list[dict],
    entity_2_table_name,
    entity_2_items: list[dict],
    left_id,
    right_id,
    dropdown_keys=None,
    dropdown_items_for_add=None,
):
    if not dropdown_keys:
        dropdown_keys = []
    if not dropdown_items_for_add:
        dropdown_items_for_add = {}

    columns_information_result = (
        conn.execute(text(get_columns_information_query(table_name=table_name)))
        .mappings()
        .all()
    )
    columns_information = get_columns_information_dict(columns_information_result)

    return templates.TemplateResponse(
        f"{table_name}/update.j2",
        {
            "request": request,
            "items": intersection_items,
            "table_name": table_name,
            "columns_information": columns_information,
            "dropdown_keys": dropdown_keys,
            "dropdown_items_for_add": dropdown_items_for_add,
            "entity_1_table_name": entity_1_table_name,
            "entity_1": entity_1_items,
            "entity_2_table_name": entity_2_table_name,
            "entity_2": entity_2_items,
            "table_information": TABLES_INFORMATION[table_name],
            "left_id": left_id,
            "right_id": right_id,
        },
    )
