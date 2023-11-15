from pyzbar.pyzbar import decode, ZBarSymbol
from PIL import Image  # pip install Pillow
# from asyncio import sleep


async def barcode_reader(path_to_image: str, code_count: int = 13):
    image = Image.open(path_to_image)  # PIL

    # decoded_list = decode(image)
    # decoded_list = await decode(image, symbols=[ZBarSymbol.EAN13, ZBarSymbol.CODE128])
    decoded_list = decode(image, symbols=[ZBarSymbol.EAN13, ZBarSymbol.CODE128])

    # await sleep(1)

    # print(f'Распознано штрих-кодов: {len(decoded_list)} | Datas: {decoded_list}')

    return [(x.data.decode()) for x in decoded_list if len(x.data.decode()) == code_count]
    # return [(x.data.decode(), x.type, x.orientation) for x in decoded_list if len(x.data.decode()) == code_count]


if __name__ == '__main__':
    import asyncio

    image_file = r'e:\SLS-Photo-for-Test\2023\2023.09\15-09-2023_(624)\DSC_7361.JPG'

    result = asyncio.run(barcode_reader(image_file))
    print(result)

    # При помощи PIL узнать размер можно так:
    # from PIL import Image
    #
    # im = Image.open("logo.jpg")
    # (width, height) = im.size
