import os
import shutil


async def save_photo(src_path: str, dst_path: str, data: dict, action_move: bool = False):
    # распечатать все файлы и папки рекурсивно
    for dir_path, dir_names, filenames in os.walk(src_path):
        for filename in filenames:
            # print(f'\ndata[dir_path][filename]: {os.src_path.join(dir_path, filename)}\n{data[dir_path][filename]}')
            # print(f"Файл: {filename}\t| Путь: {dir_path}\t| Полный путь: {os.src_path.join(dir_path, filename)}")

            # or data[dir_path][filename]['status'] == 'BarCode'  # нет поля new_name
            if dir_path in data and filename in data[dir_path] and 'status' in data[dir_path][filename]:
                if (data[dir_path][filename]['status'] == 'OK'
                        or data[dir_path][filename]['status'] == 'attention'
                        or data[dir_path][filename]['status'] == 'BarCode'):

                    new_filename = data[dir_path][filename]['new_name']
                    barcode = data[dir_path][filename]['barcode']

                    src_file_path = os.path.join(dir_path, filename)

                    dst_dir_path = dir_path.replace(src_path, dst_path)
                    dst_file_path = os.path.join(dst_dir_path, new_filename)

                    dst_dir_path_barcode = os.path.join(dst_path, barcode[0:8])
                    dst_file_path_barcode = os.path.join(dst_dir_path_barcode, new_filename)

                    # TODO: проверить корректность работы с полными и относительными путями с учетом ОС Windows
                    if not os.path.exists(dst_dir_path):
                        print(f'Directory: "{dst_dir_path}" not found! Create directory.')
                        os.makedirs(dst_dir_path)

                    if not os.path.exists(dst_dir_path_barcode):
                        print(f'Directory: "{dst_dir_path_barcode}" not found! Create directory.')
                        os.makedirs(dst_dir_path_barcode)

                    try:
                        shutil.copy2(src_file_path, dst_file_path)

                        if action_move:
                            os.replace(src_file_path, dst_file_path_barcode)
                        else:
                            shutil.copy2(src_file_path, dst_file_path_barcode)

                    except FileNotFoundError:
                        print(f'File: "{src_file_path}" not found!')

    # переименовать text.txt на renamed-text.txt
    # os.rename("text.txt", "renamed-text.txt")

    # заменить (переместить) этот файл в другой каталог
    # os.replace("renamed-text.txt", "folder/renamed-text.txt")
