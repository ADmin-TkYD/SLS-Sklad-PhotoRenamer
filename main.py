import asyncio
# import json module
# import json

# from concurrent.futures import ThreadPoolExecutor

from misc import find_photo, find_barcode, barcode_reader, save_data_to_json


# _executor = ThreadPoolExecutor(1)


# def sync_blocking(seconds: int = 1):
#     time.sleep(seconds)


async def main(path: str, extension: list, pattern: str, data_file: str):
    ext = '|'.join(map(str, extension))

    dict_with_photo = await find_photo(path, ext)
    dict_with_photo = await find_barcode(
        barcode_reader=barcode_reader, dict_with_photo=dict_with_photo, pattern=pattern)

    await save_data_to_json(path=data_file, data=dict_with_photo)

    # await print_data_from_json(dict_with_photo)

    # run blocking function in another thread,
    # and wait for it's result:
    # await loop.run_in_executor(_executor, sync_blocking)


if __name__ == '__main__':
    photo_dir = r'e:\SLS-Photo-for-Test\СЕНТЯБРЬ_2023\01-09-2023_(169) (1)\RIOPELE'
    # photo_dir = r'e:\SLS-Photo-for-Test\СЕНТЯБРЬ_2023'
    photo_ext = ['jpg', 'jpeg', 'png']
    pattern_barcode = r'^21\d{11}$'
    data_file = r'db\.data.json'

    try:
        asyncio.run(main(path=photo_dir, extension=photo_ext, pattern=pattern_barcode, data_file=data_file))
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(main(photo_dir, photo_ext))
        # loop.close()
    except (KeyboardInterrupt, SystemExit):
        print('Program was stopped by user.')


