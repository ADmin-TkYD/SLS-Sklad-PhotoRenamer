import re
# from misc.barcode_reader import barcode_reader


async def find_barcode(barcode_reader, dict_with_photo: dict, pattern: str) -> dict:
    for path, dict_files in dict_with_photo.items():
        for file, params in dict_files.items():
            # print(f'{params["path"]}')
            # print(f'{decode_barcode(params["path"])}')

            # print(f'{os.path.join(path, file)}')
            # os.path.join(path, file)

            barcode_result = await barcode_reader(params["path"])
            # print(f'{barcode_result}')

            barcode_count = len(barcode_result)
            if barcode_count > 0:
                match = {'barcode': barcode for barcode in barcode_result if re.fullmatch(pattern, barcode)}

                # print(f'{barcode_result}\t{type(barcode_result)}')
                # dict_with_photo[path].update({dr: {'path': abs_path}})

                dict_with_photo[path][file].update(match)

                if barcode_count > 1:
                    dict_with_photo[path][file].update({'debug': barcode_result})
                    # dict_with_photo.update({'debug': dict_with_photo[path][file]})
                    print(f"barcode_result: '{barcode_result}\nbarcode: {dict_with_photo[path][file]['barcode']}\n"
                          f"{dict_with_photo[path][file]}")

    return dict_with_photo
