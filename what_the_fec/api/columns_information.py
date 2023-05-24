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
            "IS_NULLABLE": entry["IS_NULLABLE"] 
        }
    return columns_information_dict
