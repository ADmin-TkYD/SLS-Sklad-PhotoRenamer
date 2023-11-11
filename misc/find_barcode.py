import re
import os
from typing import Callable
# from misc.barcode_reader import barcode_reader


# async def find_barcode(
#         barcode_reader: Callable, dict_with_files: dict, pattern_barcode: str, pattern_photo_name: str, extension: str
# ) -> dict:
async def find_barcode(barcode_reader: Callable, dict_with_photo: dict, patterns: dict) -> dict:
    # RegExp patterns:
    # pattern_photo_files = f'{pattern_photo_name}(?:{extension})$'
    # pattern_barcode_name_files = f'{pattern_barcode}[-][a-z][.](?:{extension})$'
    # pattern_extension = r'.*[.](\w{3,4})$'

    if dict_with_photo.get('all') is None:
        print(f'File dictionary is empty.')
        return {}

    # if dict_with_files.get('barcode') is None:
    #     # print(f'Create KEY "barcode" in dictionary.')
    #     dict_with_files.update({'barcode': {}})

    if dict_with_photo.get('group') is None:
        dict_with_photo.update({'group': {}})

    if dict_with_photo.get('incomprehensible') is None:
        dict_with_photo.update({'incomprehensible': {}})

    for path, dict_files in dict_with_photo['all'].items():
        # default values:
        dict_with_photo['group'] = {}
        letter = 'a'

        for file, params in dict_files.items():
            # Если файл уже был переименован ранее, переходим к следуюющему файлу.
            if re.fullmatch(patterns['barcode_name_files'], file, flags=re.IGNORECASE):
                continue

            barcode_result = await barcode_reader(os.path.join(path, file))

            barcode_count = len(barcode_result)

            if barcode_count == 0:
                # Если имя файла подпадает под шаблон имен файлов фотографий.
                if re.fullmatch(patterns['photo_name'], file, flags=re.IGNORECASE):
                    dict_with_photo['group'].update({file: letter})

                    # Функция ord() использована для возврата кода начальной буквы алфавита («a»), к нему прибавляется
                    # текущее смещение, задаваемое итерируемой переменной i. А далее для полученных кодов функция chr()
                    # возвращает буквы.
                    letter = chr(ord(letter) + 1)
                else:
                    dict_with_photo['incomprehensible'].update({os.path.join(path, file): ''})

            if barcode_count > 0:
                match = {'barcode': barcode for barcode in barcode_result if re.fullmatch(patterns['barcode'], barcode)}

                dict_with_photo['all'][path][file].update(match)

                # if barcode is not None
                if dict_with_photo['all'][path][file]['barcode']:
                    # А оно надо? =))) - not use
                    # Update dictionary "dict_with_files['barcode']" added dictionary "{barcode: file}"
                    # dict_with_files['barcode'].update({dict_with_files['all'][path][file]['barcode']: file})

                    for file_name, file_letter in dict_with_photo['group'].items():
                        # Get extension from file
                        ext = re.fullmatch(patterns['extension'], file, flags=re.IGNORECASE)[1].lower()

                        dict_with_photo['all'][path][file_name].update({
                            'barcode': dict_with_photo['all'][path][file]['barcode'],
                            'new_name': f"{dict_with_photo['all'][path][file]['barcode']}-{file_letter}.{ext}"
                        })

                        # DEBUG
                        # print(
                        #     f'File: {file_name}\tLetter: {file_letter}\t'
                        #     f'Result: {dict_with_files["all"][path][file_name]}')

                    # reset values to default:
                    dict_with_photo['group'] = {}
                    letter = 'a'

                # DEBUG
                if barcode_count > 1:
                    dict_with_photo['all'][path][file].update({'debug': barcode_result})

                    print(
                        f"Attention!:\t"
                        f"barcode_result: '{barcode_result}\tbarcode: {dict_with_photo['all'][path][file]['barcode']}"
                    )

    del dict_with_photo['group']

    # if not (dict_with_files['incomprehensible']):
    #     del dict_with_files['incomprehensible']

    return dict_with_photo
