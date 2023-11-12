import re
import os
from typing import Callable
# from misc.barcode_reader import barcode_reader


async def find_barcode(barcode_reader: Callable, dict_with_photo: dict, patterns: dict) -> dict:
    # if dict_with_photo.get('all') is None:
    if not dict_with_photo:
        print(f'File dictionary is empty.')
        return {}

    enable_debug = True

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
        print(f'Open Dir: {path}')
        if enable_debug:
            print(f'Set default values:\tphoto_group: {photo_group}\tletter: "{letter}"')

        for file in dict_files:
            print()
            # DEBUG:
            # matches = re.fullmatch(patterns['barcode_name_files'], file, flags=re.IGNORECASE)
            # print(f"Select file: {file}") if matches else ""
            # print(f"{patterns['barcode_name_files']} File: {file}")

            if enable_debug:
                print(f'File found: {file}')
            # Если файл уже был переименован ранее, переходим к следуюющему файлу.
            if re.fullmatch(patterns['barcode_name_files'], file, flags=re.IGNORECASE):
                dict_with_photo[path][file].update({
                    'status': statuses['renamed'], 'debug': f"The file '{file}' was previously renamed"})
                print(f'The file "{file}" was previously renamed. Continue...')

            # Если имя файла подпадает под шаблон имен файлов фотографий.
            elif re.fullmatch(patterns['photo_files'], file, flags=re.IGNORECASE):
                barcode_result = await barcode_reader(os.path.join(path, file))
                barcode_count = len(barcode_result)
                if enable_debug:
                    print(f'The file "{file}" matches pattern.')
                    print(f'Barcodes found {barcode_count}.')

                if barcode_count == 0:
                    photo_group.update({file: letter})
                    if enable_debug:
                        print(f'Adding a file to a group of unidentified photos: "{photo_group[file]}".')

                    # Функция ord() использована для возврата кода начальной буквы алфавита («a»), к нему прибавляется
                    # текущее смещение, задаваемое итерируемой переменной i. А далее для полученных кодов функция chr()
                    # возвращает буквы.
                    letter = chr(ord(letter) + 1)

                if barcode_count > 0:
                    match = {'barcode': barcode
                             for barcode in barcode_result if re.fullmatch(patterns['barcode'], barcode)}

                    if match is None:
                        dict_with_photo[path][file].update({
                            'status': statuses['incomprehensible'],
                            'debug': {'barcode_count': barcode_count, 'barcode_result': barcode_result, 'match': match,
                                      'file': os.path.join(path, file)}
                        })
                        if enable_debug:
                            print(
                                f"Status: {dict_with_photo[path][file]['status']}\t"
                                f"The barcode found does not match the pattern\n"
                                f"DEBUG: {barcode_result}")

                    dict_with_photo[path][file].update(match)

                    # if barcode is not None (if the barcode is read from this file)
                    if dict_with_photo[path][file]['barcode']:
                        dict_with_photo[path][file].update({'status': statuses['barcode']})
                        if enable_debug:
                            print(
                                f'We found a barcode on the photo {dict_with_photo[path][file]["barcode"]}, '
                                f'adding it to the group of files.')

                        for file_name, file_letter in photo_group.items():
                            # Get extension from file
                            ext = re.fullmatch(patterns['extension'], file, flags=re.IGNORECASE)[1].lower()

                            dict_with_photo[path][file_name].update({
                                'barcode': dict_with_photo[path][file]['barcode'],
                                'new_name': f"{dict_with_photo[path][file]['barcode']}-{file_letter}.{ext}",
                                'status': statuses['ok']
                            })

                            if enable_debug:
                                print(
                                    f'Status: {dict_with_photo[path][file_name]["status"]}\t'
                                    f'File: {file_name}\tLetter: {file_letter}\t'
                                    f'Result: {dict_with_photo[path][file_name]}')

                        # reset values to default:
                        photo_group = {}
                        letter = 'a'
                        if enable_debug:
                            print(f'Reset values to default:\tphoto_group: {photo_group}\tletter: "{letter}"')

                    # DEBUG
                    if barcode_count > 1:
                        dict_with_photo[path][file].update({'status': statuses['attention']})
                        dict_with_photo[path][file].update({'debug': f'Double BarCode: {barcode_result}'})

                        print(
                            f"Status: {dict_with_photo[path][file]['status']}!:\t"
                            f"\tbarcode_result: '{barcode_result}"
                            f"\t| Save barcode: {dict_with_photo[path][file]['barcode']}"
                            f"\t| Save path: {os.path.join(path, file)}\n"
                        )

            # Если имя файла не подпадает ни под один шаблон имен файлов.
            else:
                barcode_count = -1
                dict_with_photo[path][file].update({
                    'status': statuses['incomprehensible'],
                    'debug': {'filename': file, 'file': os.path.join(path, file)}
                })
                print(f"Status: {dict_with_photo[path][file]['status']}!:\tFile '{file}' does not match the pattern.")

    return dict_with_photo
