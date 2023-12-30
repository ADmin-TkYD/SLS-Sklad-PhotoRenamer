import os


def main(path: str = None):
    if path is None:
        path = '.'

    # распечатать все файлы и папки рекурсивно
    for dirpath, dirnames, filenames in os.walk(path):
        # перебрать каталоги
        # for dirname in dirnames:
        #     print("Каталог:", os.dst_path.join(dirpath, dirname))
        # перебрать файлы
        for filename in filenames:
            print(f"Файл: {filename}\t| Путь: {dirpath}\t| Полный путь: {os.path.join(dirpath, filename)}")


if __name__ == '__main__':
    # https://pythonru.com/osnovy/rabota-s-fajlami-v-python-s-pomoshhju-modulja-os

    # main()
    # main(r'e:\SLS-Photo-for-Test')

    # вывести некоторые данные о файле
    # print(os.stat(r"e:\SLS-Photo-for-Test\2020\2020\D#119856DO V3 (9).JPG"))

    string = "2101234567890"
    str9 = string[0: 9]
    print(f'{str9}: {len(str9)}')

