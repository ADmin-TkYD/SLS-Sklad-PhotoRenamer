import re
import os
from typing import Callable
# from misc.barcode_reader import barcode_reader


async def find_barcode(barcode_reader: Callable, dict_with_photo: dict, patterns: dict) -> dict:
    # if dict_with_photo.get('all') is None:
    if not dict_with_photo:
        print(f'File dictionary is empty.')
        return {}

    statuses = {
        'ok': 'OK',
        'barcode': 'BarCode',
        'renamed': 'Renamed',
        'attention': 'Attention',
        'incomprehensible': 'Incomprehensible',
    }

    for path, dict_files in dict_with_photo.items():
        # default values:
        photo_group = {}
        letter = 'a'

        for file in dict_files:
            # DEBUG:
            # matches = re.fullmatch(patterns['barcode_name_files'], file, flags=re.IGNORECASE)
            # print(f"Select file: {file}") if matches else ""
            # print(f"{patterns['barcode_name_files']} File: {file}")

            # Если файл уже был переименован ранее, переходим к следуюющему файлу.
            if re.fullmatch(patterns['barcode_name_files'], file, flags=re.IGNORECASE):
                dict_with_photo[path][file].update({
                    'status': statuses['renamed'], 'debug': f"The file '{file}' was previously renamed"})
                print(f'The file "{file}" was previously renamed. Continue...')

            # Если имя файла подпадает под шаблон имен файлов фотографий.
            elif re.fullmatch(patterns['photo_files'], file, flags=re.IGNORECASE):
                barcode_result = await barcode_reader(os.path.join(path, file))
                barcode_count = len(barcode_result)

                if barcode_count == 0:
                    photo_group.update({file: letter})

                    # Функция ord() использована для возврата кода начальной буквы алфавита («a»), к нему прибавляется
                    # текущее смещение, задаваемое итерируемой переменной i. А далее для полученных кодов функция chr()
                    # возвращает буквы.
                    letter = chr(ord(letter) + 1)

                if barcode_count > 0:
                    match = {'barcode': barcode for barcode in barcode_result if re.fullmatch(patterns['barcode'], barcode)}

                    if match is None:
                        dict_with_photo[path][file].update({
                            'status': statuses['incomprehensible'],
                            'debug': {'barcode_count': barcode_count, 'barcode_result': barcode_result, 'match': match,
                                      'file': os.path.join(path, file)}
                        })

                    dict_with_photo[path][file].update(match)

                    # if barcode is not None (if the barcode is read from this file)
                    if dict_with_photo[path][file]['barcode']:
                        dict_with_photo[path][file].update({'status': statuses['barcode']})

                        for file_name, file_letter in photo_group.items():
                            # Get extension from file
                            ext = re.fullmatch(patterns['extension'], file, flags=re.IGNORECASE)[1].lower()

                            dict_with_photo[path][file_name].update({
                                'barcode': dict_with_photo[path][file]['barcode'],
                                'new_name': f"{dict_with_photo[path][file]['barcode']}-{file_letter}.{ext}",
                                'status': statuses['ok']
                            })

                            # DEBUG
                            # print(
                            #     f'File: {file_name}\tLetter: {file_letter}\t'
                            #     f'Result: {dict_with_files["all"][path][file_name]}')

                        # reset values to default:
                        photo_group = {}
                        letter = 'a'

                    # DEBUG
                    if barcode_count > 1:
                        dict_with_photo[path][file].update({'status': statuses['attention']})
                        dict_with_photo[path][file].update({'debug': f'Double BarCode: {barcode_result}'})

                        print(
                            f"Attention!:\t"
                            f"\tbarcode_result: '{barcode_result}"
                            f"\t| Save barcode: {dict_with_photo[path][file]['barcode']}"
                            f"\t| Save path: {os.path.join(path, file)}"
                        )

            # Если имя файла не подпадает ни под один шаблон имен файлов.
            else:
                barcode_count = -1
                dict_with_photo[path][file].update({
                    'status': statuses['incomprehensible'],
                    'debug': {'filename': file, 'file': os.path.join(path, file)}
                })

    return dict_with_photo
