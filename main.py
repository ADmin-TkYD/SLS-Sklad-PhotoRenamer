from misc import find_photo


def main(path: str, extension: list):
    ext = '|'.join(map(str, extension))

    dict_with_photo = find_photo.find_photo(path, ext)
    print(f'dict_with_photo: {dict_with_photo}')


if __name__ == '__main__':
    photo_dir = r'e:\SLS-Photo-for-Test\СЕНТЯБРЬ_2023'
    photo_ext = ['jpg', 'jpeg', 'png']

    main(photo_dir, photo_ext)
