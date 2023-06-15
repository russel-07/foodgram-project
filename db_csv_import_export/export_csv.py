import csv, sqlite3


def export_db_to_csv(to_file_path, from_db_name, from_table_name):
    connect = sqlite3.connect(from_db_name)
    connect.text_factory = str
    cursor = connect.cursor()

    data = cursor.execute(f'SELECT * FROM {from_table_name}')
    with open(to_file_path, 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file)
        model_headers = (str[0] for str in data.description)
        writer.writerow(model_headers)
        writer.writerows(data)


def export_all(table_to_csv_dict, from_db_name, to_files_path):
    for key in table_to_csv_dict:
        to_path = to_files_path + table_to_csv_dict[key] + '.csv'
        from_table_name = key
        export_db_to_csv(to_path, from_db_name, from_table_name)


table_dict = {
    'auth_user': 'users',
    'app_recipes_unit': 'units',
    'app_recipes_ingredient': 'ingredients',
    'app_recipes_tag': 'tags',
}

export_all(table_dict, 'db.sqlite3', '../db_csv_import_export/csv_export/')
