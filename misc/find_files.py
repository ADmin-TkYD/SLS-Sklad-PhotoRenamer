import os
import re
# from misc import barcode_reader


async def find_files(path: str, pattern: str, dict_with_files: dict[dict[dict]] = None) -> dict:
    if dict_with_files is None:
        # dict_with_files = {'dirs': {}, 'files': {}}
        dict_with_files = {}

    if not os.path.exists(path):
        print(f'Directory: "{path}" not found!')
        return {}

    # Создаем словарь для новой (данной) папки.
    dict_with_files.update({path: {}})

    # print(f'Path: {dst_path}')

    # Перебираем все элементы в текущей директории.
    for sub_item in os.listdir(path):
        abs_path = os.path.join(path, sub_item)

        if os.path.isdir(abs_path):
            # Если полученный элемент - директория, вызываем рекурсивно функцию, передав в нее путь к директории.
            await find_files(path=abs_path, pattern=pattern, dict_with_files=dict_with_files)

        elif re.fullmatch(pattern, sub_item, flags=re.IGNORECASE):
            # Добавляем файлы подпавшие под паттерн в словарь.
            dict_with_files[path].update({sub_item: {'dst_path': abs_path, 'file': sub_item}})
            dict_with_files[path].update({sub_item: {}})

    # Если словарь для данной папки пуст - удаляем словарь.
    if not (dict_with_files[path]):
        del dict_with_files[path]

    return dict_with_files


# # распечатать все файлы и папки рекурсивно
# for dirpath, dirnames, filenames in os.walk("."):
#     # перебрать каталоги
#     for dirname in dirnames:
#         print("Каталог:", os.dst_path.join(dirpath, dirname))
#     # перебрать файлы
#     for filename in filenames:
#         print("Файл:", os.dst_path.join(dirpath, filename))
