
import json
import jsonschema
import os
from loguru import logger

logger.add('errors.log', encoding='UTF-8', format="\n{time} {level} {message}", level="ERROR")

EVENT_FOLD = os.path.join(os.getcwd(), 'event')
SCHEMA_FOLD = os.path.join(os.getcwd(), 'schema')


def read_json(path_file):
    with open(path_file, "r", encoding='UTF-8') as file:
        data = json.load(file)
    return data


def read_schema(path_file):
    with open(path_file, 'r') as f:
        schema_ = f.read()
        schema_data = json.loads(schema_)
    return schema_data


def validation(event, schema):
    name_schema = os.path.basename(schema)
    for path, dirs, files in os.walk(event):
        for file in files:
            path_f = os.path.join(path, file)
            validate_schema = jsonschema.Draft7Validator(read_schema(schema))
            errors = validate_schema.iter_errors(read_json(path_f))
            for err_ in errors:
                if err_.validator == 'required':
                    logger.error(f'\nОшибка по схеме <<{name_schema}>> в файле <<{file}>>\n<<{err_.message}>> --> '
                                 f'Свойство отсутвует или расположено не по структуре json.schema.')
                elif err_.validator == 'type':
                    if 'None' in err_.message:
                        logger.error(f'\nОшибка по схеме <<{name_schema}>> в файле <<{file}>>'
                                     f'\n<<{err_.message}>> --> JSON файл пустой. ')
                    else:
                        logger.error(f'\nОшибка по схеме <<{name_schema}>> в файле <<{file}>>'
                                     f'\n<<{err_.message}>> --> Неверный тип данных в ключах JSON файла.')


def main():
    for path, dirs, files in os.walk(SCHEMA_FOLD):
        for file in files:
            path_schema = os.path.join(path, file)
            validation(EVENT_FOLD, path_schema)


if __name__ == '__main__':
    main()
