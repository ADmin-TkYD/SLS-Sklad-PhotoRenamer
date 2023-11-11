import os
import re
# from misc import barcode_reader


# Union[Union[int, str], float]
async def find_photo(path: str, extension: str, dict_with_photo: dict[dict[dict]] = None) -> dict:
    if dict_with_photo is None:
        # dict_with_photo = {'dirs': {}, 'files': {}}
        dict_with_photo = {}

    # text_barcodes_read = f'Прочитано штрих-кодов: {{barcode_count}}!'
    # text_photo_does_not_contain_barcode = f'\nФото не содержит штрих-кода, либо его не удалось прочитать!'

    pattern_photo = r'.*[.](?:' + extension + ')$'

    """
    # pattern_photo = r'^DSC_(\d{4})[.](?:' + extension + ')$'
    # pattern_barcode = r'^21\d{11}$'
    # pattern_end_file_name = r'^\d{13}[-]\w$'

    # count_dirs = len(dict_with_photo['dirs'])
    # count_files = len(dict_with_photo['files'])

    # datas['products'].update({code[0]: 0 for code in barcode_result if code[0] not in datas['products']})
    # dict_with_photo['dirs'].update({count_dirs: path})
    # count_dirs = len(dict_with_photo['dirs'])
    """

    # Создаем словарь для новой (данной) папки.
    dict_with_photo.update({path: {}})

    # print(f'Path: {path}')

    # Перебираем все элементы в текущей директории.
    for dr in os.listdir(path):
        abs_path = os.path.join(path, dr)
        # print(f'\tabs_path: {abs_path}')

        if os.path.isdir(abs_path):
            # print(f'\t\tDir: {dr}')
            # Если полученный элемент - директория, вызываем рекурсивно функцию, передав в нее путь к директории.
            await find_photo(path=abs_path, extension=extension, dict_with_photo=dict_with_photo)

        elif re.fullmatch(pattern_photo, dr, flags=re.IGNORECASE):
            # Добавляем файлы подпавшие под паттерн в словарь.
            # dict_with_photo[path].update({len(dict_with_photo[path]): abs_path})
            # dict_with_photo[path].update({dr: {'barcode': 0, 'letter': '', 'path': abs_path}})
            dict_with_photo[path].update({dr: {'path': abs_path, 'file': dr}})

        """
        # elif '.jpg' in dr[-4:].lower():
        # print(f'\t\tfile: {dr}')

        # else:
        #     match = re.fullmatch(pattern_photo, dr, flags=re.IGNORECASE)
        #     if match:
        #         # print(f'{dr}: YES: {match}' if match else f'{dr}: NO: {match}')
        #         # print(f'В строке {dr}, найдена подстрока >{match[1]}< с позиции {match.start(1)} до {match.end(1)}')
        #         file_number = match[1]
        #
        #         barcode_result = barcode_reader.decode_barcode_symbols(abs_path)
        #
        #         barcode_count = len(barcode_result)
        #         if barcode_count > 0:




            # if barcode_count != 1:
            #     text_msg = text_barcodes_read
            #
            #     if barcode_count < 1:
            #         text_msg += text_photo_does_not_contain_barcode
            #         continue
            #
            #     print(f'{text_msg.format(barcode_count=barcode_count)}')
            #
            #     if barcode_count > 1:
            #         print(f'{text_msg.format(barcode_count=barcode_count)} | Datas: {barcode_result} '
            #               f'| File: {abs_path}')
            #         match = re.fullmatch(pattern_barcode, dr, flags=re.IGNORECASE)
        """

    # Если словарь для данной папки пуст - удаляем словарь.
    if not (dict_with_photo[path]):
        del dict_with_photo[path]

    return dict_with_photo
