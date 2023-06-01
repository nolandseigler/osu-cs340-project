from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection, text


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
    print(columns_information_dict)
    print(columns_information_dict)
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
    dropdown_keys=[],
    dropdown_items_for_add={},
):
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
        },
    )
