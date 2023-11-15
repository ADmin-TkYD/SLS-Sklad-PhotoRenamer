import os
import re


async def find_files(handlers: dict, path: str, patterns: dict, dictionary: dict[dict[dict]] = None) -> dict:
    if dictionary is None:
        # dictionary = {'dirs': {}, 'dictionary': {}}
        dictionary = {}

    if not os.path.exists(path):
        print(f'Directory: "{path}" not found!')
        return {}

    pattern = patterns['find_files']

    # Создаем словарь для новой (данной) папки.
    dictionary.update({path: {}})

    # print(f'Path: {file_path}')

    # Перебираем все элементы в текущей директории.
    for sub_item in os.listdir(path):
        abs_path = os.path.join(path, sub_item)

        if os.path.isdir(abs_path):
            # Если полученный элемент - директория, вызываем рекурсивно функцию, передав в нее путь к директории.
            await find_files(handlers=handlers, path=abs_path, patterns=patterns, dictionary=dictionary)

        elif re.fullmatch(pattern, sub_item, flags=re.IGNORECASE):
            # Добавляем файлы подпавшие под паттерн в словарь.
            # dictionary[file_path].update({sub_item: {'file_path': file_path, 'file': sub_item}})
            # dictionary[file_path].update({sub_item: {})

            photo_data, photo_group = await handlers['find'](
                barcode_reader=handlers['read'], path=path, file=sub_item, patterns=patterns)
            dictionary[path].update({sub_item: photo_data})
            print(f'photo_group: {photo_group}')

            # dictionary[file_path].update(
            #     {sub_item: await handlers['find'](
            #         barcode_reader=handlers['read'], file_path=file_path, file=sub_item, patterns=patterns
            #     )}
            # )
            # default values:
            photo_group = {}
            letter = 'a'

    # Если словарь для данной папки пуст - удаляем словарь.
    if not (dictionary[path]):
        del dictionary[path]

    return dictionary
