import sqlite3
import csv


def get_name_tables(from_db_name):
    connect = sqlite3.connect(from_db_name)
    cursor = connect.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in cursor.fetchall():
        print(table)


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
    'app_users_user': 'users',
    'app_recipes_unit': 'units',
    'app_recipes_ingredient': 'ingredients',
    'app_recipes_tag': 'tags',
    'app_recipes_recipe': 'recipes',
    'app_recipes_recipe_tags': 'recipe_tags',
    'app_recipes_recipeingredient': 'recipe_ingredients',
    'django_flatpage_sites': 'flatpage_sites',
    'django_flatpage': 'flatpages',
}


get_name_tables('db.sqlite3')
export_all(table_dict, 'db.sqlite3', '../db_csv_import_export/csv_export/')
