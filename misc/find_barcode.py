import re
import os
from typing import Callable
# from misc.barcode_reader import barcode_reader


async def find_barcode(barcode_reader: Callable, dict_with_photo: dict, pattern: str) -> dict:
    # for path, dict_files in dict_with_photo.items():  # ver 2
    for path, dict_files in dict_with_photo['all'].items():  # ver 3
        for file, params in dict_files.items():
            # print(f'{params["path"]}' )
            # print(f'{decode_barcode(params["path"])}')

            # print(f'{os.path.join(path, file)}')
            # os.path.join(path, file)

            # barcode_result = await barcode_reader(params["path"])
            barcode_result = await barcode_reader(os.path.join(path, file))
            # print(f'{barcode_result}')

            barcode_count = len(barcode_result)
            if barcode_count > 0:
                match = {'barcode': barcode for barcode in barcode_result if re.fullmatch(pattern, barcode)}

                # print(f'{barcode_result}\t{type(barcode_result)}')
                # dict_with_photo[path].update({dr: {'path': abs_path}})

                # dict_with_photo[path][file].update(match)  # ver 2
                dict_with_photo['all'][path][file].update(match)  # ver 3

                if barcode_count > 1:
                    # dict_with_photo[path][file].update({'debug': barcode_result})  # ver 2
                    dict_with_photo['all'][path][file].update({'debug': barcode_result})  # ver 3
                    # dict_with_photo.update({'debug': dict_with_photo[path][file]})
                    # print(  # ver 2
                    #     f"barcode_result: '{barcode_result}\n"  # ver 2
                    #     f"barcode: {dict_with_photo[path][file]['barcode']}\n"  # ver 2
                    #     f"{dict_with_photo[path][file]}")  # ver 2

                    print(  # ver 3
                        f"barcode_result: '{barcode_result}\n"  # ver 3
                        f"barcode: {dict_with_photo['all'][path][file]['barcode']}\n"  # ver 3
                        f"{dict_with_photo['all'][path][file]}")  # ver 3

    return dict_with_photo
