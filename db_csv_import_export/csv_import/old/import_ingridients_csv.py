import csv, sqlite3


units = ['name', 'банка', 'батон', 'бутылка', 'веточка', 'г', 'горсть',
         'долька', 'звездочка', 'зубчик', 'капля', 'кг', 'кусок', 'л',
         'лист', 'мл', 'пакет', 'пакетик', 'пачка', 'пласт', 'по вкусу',
         'пучок', 'ст. л.', 'стакан', 'стебель', 'стручок', 'тушка',
         'упаковка', 'ч. л.', 'шт.', 'щепотка']

def import_csv_to_db(from_file_path, to_db_name, to_table_name):
    connect = sqlite3.connect(to_db_name)
    cursor = connect.cursor()

    start_pos = 1

    with open(from_file_path, 'r', encoding='utf8') as file:
        dr = csv.DictReader(file, delimiter=',') # csv.DictReader по умолчанию использует первую строку под заголовки столбцов
        csv_headers = tuple(dr.fieldnames)
        to_db = []
        for string in dr:
            to_db.append([])
            for i, value in enumerate(string.values()):
                if i == 1:
                    to_db[-1].append(str(units.index(value)))
                else:
                    to_db[-1].append(value)
            to_db[-1].append(str(start_pos))
            start_pos += 1

    get_model_headers = connect.execute(f'SELECT * FROM {to_table_name}')
    model_headers = tuple(str[0] for str in get_model_headers.description)

    import_headers = list(csv_headers)
    for header in model_headers:
        if header not in import_headers:
            import_headers.append(header)

    import_values = '('
    i = 0
    
    for header in import_headers:
        if header in csv_headers:
            import_values += '?'
        else:
            import_values += "?"
        i += 1

        if i < len(import_headers):
            import_values += ', '
        else:
            import_values += ')'

    cursor.executemany(f"INSERT INTO {to_table_name} {tuple(import_headers)} VALUES {import_values};", to_db)
    connect.commit()
    connect.close()


def import_all(csv_to_table_dict, from_files_path, to_db_name):
    for key in csv_to_table_dict:
        from_path = from_files_path + csv_to_table_dict[key] + '.csv'
        to_table_name = key
        import_csv_to_db(from_path, to_db_name, to_table_name)


table_dict = {
    'app_recipes_ingredient': 'ingredients',
}

import_all(table_dict, '../ingredients_csv/', 'db.sqlite3')
