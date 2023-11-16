import json
import re
import os
import time

from misc.find_barcode import find_barcode
from misc.barcode_reader import barcode_reader


start_time = time.time()


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class PhotoHandler:
    def __init__(self, home_path: str = None, deep: int = None) -> None:
        self._dict_photo = None
        self._max_deep = None

        self._cur_path = None
        self._cur_parse_urls = None
        self._cur_deep = None
        self._cur_domain = None
        self._cur_check_url = None
        # self._https = 'https://'
        # self._google = 'www.google.com/search?q='

        self._count = None

        self._save_file = 'result.json'
        # self._re_domain = \
        #     r'https?:\/\/((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9])\/.*'

        self.set_folder(path=home_path)
        self.set_deep(deep=deep)
        self._create_dict()

    def set_folder(self, path: str = None) -> None:
        if path is not None:
            self._cur_path = path
        print(f'set_folder(self, path: str): path: {path} | self._cur_path: {self._cur_path}')

    def set_deep(self, deep: int) -> None:
        self._max_deep = 0 if deep is None else deep

    # def set_google_search(self, search: str = 'python') -> None:
    #     self.set_folder(f'{self._https}{self._google}{search}')

    async def print_info(self, data: dict = None) -> None:
        print_data = self._dict_photo if data is None else data
        print(json.dumps(print_data, indent=4, ensure_ascii=False, sort_keys=True))

    async def save_info(self, file: str = None) -> None:
        if file is None:
            file = self._save_file
        with open(file, 'w') as json_file:
            json.dump(self._dict_photo, json_file, indent=4, ensure_ascii=False, sort_keys=True)

    def _create_dict(self) -> None:
        self._dict_photo = {}

    async def _set_current_path(self, path: str = None) -> None:
        # дубликат set_folder
        if path is not None:
            self._cur_path = path

    async def _get_current_path(self) -> str:
        return self._cur_path

    async def _read_last_info(self, file_path: str = None) -> None:
        # async def save_data_to_json(path: str, data: dict) -> json:
        try:
            with open(file_path, 'r') as json_file:
                data_from_file = json.load(json_file)
            try:
                _, self._dict_photo = data_from_file.update(self._dict_photo), data_from_file
            except AttributeError:
                print(f'AttributeError: object has no attribute "update"')

        except FileNotFoundError:
            print(f'FileNotFoundError: No such file or directory: {file_path}')
        except json.JSONDecodeError:
            print(f'JSONDecodeError')

    async def _get_counter(self) -> None:
        return self._count

    async def _update_counter(self) -> None:
        self._count = 1 if self._count is None else self._count + 1
        # if self._count is None:
        #     self._count = 0
        # self._count += 1
        return await self._get_counter()

    async def _check_deep(self, deep: int) -> bool:
        if 0 < self._max_deep:
            return True if deep < self._max_deep else False
        return True

    # async def find_files(handlers: dict, path: str, patterns: dict, dict_paths: dict[dict[dict]] = None) -> dict:
    async def _find_files(self, deep: int = 0) -> None:
        # TODO: вынести экстеншены из функции
        extension = ['jpg', 'jpeg', 'png']
        ext = '|'.join(map(str, extension))

        # TODO: вынести паттерны из функции
        patterns = {
            'barcode': r'^21\d{11}',
            'extension': r'.*[.](\w{3,4})$',
            'photo_name': r'^DSC_(\d{4})[.]',
            'find_files': f'.*[.](?:{{extension}})$',
            'photo_files': f'{{photo_name}}(?:{{extension}})$',
            'barcode_name_files': f'{{barcode}}[-][a-z][.](?:{{extension}})$',
        }

        patterns['find_files'] = patterns['find_files'].format(extension=ext)
        patterns['photo_files'] = patterns['photo_files'].format(photo_name=patterns['photo_name'], extension=ext)
        patterns['barcode_name_files'] = patterns['barcode_name_files'].format(barcode=patterns['barcode'],
                                                                               extension=ext)
        patterns['barcode'] += '$'

        # ===============================

        path = await self._get_current_path()
        dictionary = self._dict_photo
        # if dictionary is None:
        #     dictionary = {}

        if not os.path.exists(path):
            print(f'Directory: "{path}" not found!')
            return

        pattern = patterns['find_files']

        # Создаем словарь для новой (данной) папки.
        dictionary.update({path: {}})

        # print(f'Path: {file_path}')

        # Перебираем все элементы в текущей директории.
        for sub_item in os.listdir(path):
            abs_path = os.path.join(path, sub_item)

            if os.path.isdir(abs_path):
                # Если полученный элемент - директория, вызываем рекурсивно функцию, передав в нее путь к директории.
                # await find_files(handlers=handlers, path=abs_path, patterns=patterns, dictionary=dictionary)
                await self._set_current_path(path=abs_path)
                await self._find_files(deep=deep)

            elif re.fullmatch(pattern, sub_item, flags=re.IGNORECASE):
                # Добавляем файлы подпавшие под паттерн в словарь.
                # dictionary[file_path].update({sub_item: {'file_path': file_path, 'file_path': sub_item}})
                # dictionary[file_path].update({sub_item: {})

                photo_data, photo_group = await find_barcode(
                    barcode_reader=barcode_reader, path=path, file=sub_item, patterns=patterns)
                dictionary[path].update({sub_item: photo_data})
                print(f'photo_group: {photo_group}')

                # dictionary[file_path].update(
                #     {sub_item: await handlers['find'](
                #         barcode_reader=handlers['read'], file_path=file_path, file_path=sub_item, patterns=patterns
                #     )}
                # )
                # default values:
                photo_group = {}
                letter = 'a'

        # Если словарь для данной папки пуст - удаляем словарь.
        if not (dictionary[path]):
            del dictionary[path]

        self._dict_photo = dictionary

    # async def _find_files(self, deep: int = 0) -> None:
    #     path = await self._get_current_path()
    #     dict_paths = self._dict_photo
    #
    #     print(f'path: {path}\nself._cur_path: {self._cur_path}')
    #     if not os.path.exists(path):
    #         print(f'Directory: "{path}" not found!')
    #         return
    #
    #     # Создаем словарь для новой (данной) папки.
    #     dict_paths.update({path: {}})
    #
    #     if await self._check_deep(deep):
    #         deep += 1
    #
    #         await self.print_info(dict_paths)
    #         print(f'deep: {deep}')
    #
    #         for item in os.listdir(path):
    #             abs_path = os.path.join(path, item)
    #             # print(f'item: {item}')
    #             # dict_paths[path].update({item: {}})
    #
    #             # print(f'count: {await self._update_counter()}\t| deep: {deep}\t| url: {item}\t')
    #
    #             # await self._get_urls_from_page(item)
    #             # dict_paths[item] = self._cur_parse_urls
    #
    #             if os.path.isdir(abs_path):
    #                 await self._set_current_path(path=abs_path)
    #                 # self._dict_photo = dict_paths
    #
    #                 await self._find_files(deep=deep)
    #         # for item in os.listdir(dict_paths):
    #         #     abs_path = os.path.join(dict_paths, item)
    #         #
    #         # for item in dict_paths:
    #         #     print(f'count: {self._update_counter()}\t| deep: {deep}\t| url: {item}')
    #         #
    #         #     await self._get_urls_from_page(item)
    #         #     dict_paths[item] = self._cur_parse_urls
    #         #
    #         #     if dict_paths[item]:
    #         #         await self._get_path(dict_paths=dict_paths[item], deep=deep)
    #
    #         # Если словарь для данной папки пуст - удаляем словарь.
    #         if not (dict_paths[path]):
    #             del dict_paths[path]
    #
    #         self._dict_photo = dict_paths

    async def _check_domain(self, url: str) -> str:
        match = re.fullmatch(self._re_domain, url)
        return match[1] if match and match[1] else ''

    async def _get_domain_from_url(self, url: str) -> bool:
        self._cur_domain = self._check_domain(url)
        return True if self._cur_domain else False

    async def _check_external_url(self, url: str) -> bool:
        domain = self._check_domain(url)
        return True if domain and domain != self._cur_domain else False

    async def _get_urls_from_page(self, url: str) -> None:
        urls = {}
        ua = UserAgent(browsers=['edge', 'firefox', 'chrome'])

        headers = {'User-Agent': ua.chrome}

        if not self._get_domain_from_url(url):
            print(f'{Bcolors.WARNING}Warning: Domain URL "{url}" is invalid.{Bcolors.ENDC}')
            return

        try:
            response = requests.get(url, headers=headers)
        # TODO: unknown error because ConnectionError does not fire if you send a one-word site address that
        #  is not an actual domain name
        except ConnectionError:
            print(f'{Bcolors.WARNING}Warning: requests.get({url}){Bcolors.ENDC}')
            return

        if response.status_code != 200:
            print(f'{Bcolors.WARNING}Warning: Response Status Code: {response}\tURL: {url}{Bcolors.ENDC}')
            return

        soup = bs(response.text, 'html.parser')

        for link in soup.find_all('a'):
            if link.get('href') is not None:
                if self._check_external_url(link.get('href')):
                    urls.update({link.get('href'): {}})

        self._cur_parse_urls = urls

    async def run(self):
        await self._find_files()


if __name__ == '__main__':
    import asyncio

    root_dir = os.path.dirname(os.path.abspath(__file__))
    photo_dir = root_dir
    examples_dir = r'..\examples'
    photo_dir = examples_dir

    photo_dir = r'e:\SLS-Photo-for-Test'
    # photo_dir = r'e:\SLS-Photo-for-Test\СЕНТЯБРЬ_2023'

    data_json_file = r'db\.data.json'

    photo_ext = ['jpg', 'jpeg', 'png']

    worker = PhotoHandler(home_path=photo_dir)

    print(vars(worker))

    try:
        asyncio.run(
            worker.run()
            # main(
            #     path=photo_dir,
            #     extension=photo_ext,
            #     data_file=data_json_file
            # )
        )

        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(main(photo_dir, photo_ext))
        # loop.close()
    except (KeyboardInterrupt, SystemExit):
        print('Program was stopped by user.')


# if __name__ == '__main__':
#     start_url = r'https://www.google.com/search?q=requests'
#     immersion_depth = 2
#
#     renamer = PhotoHandler(home_path=start_url, deep=immersion_depth)
#
#     try:
#         renamer.run()
#         print("--- %s seconds ---" % (time.time() - start_time))
#
#         renamer.print_info()
#
#         renamer.save_info()
#
#     except (KeyboardInterrupt, SystemExit):
#         print('Program was stopped by user.')
#
#     # # for Example:
#     # otus_parser_google = Parser()
#     # otus_parser_google.set_google_search('BeautifulSoup')
#     # otus_parser_google.set_deep = 3
#     #
#     # try:
#     #     otus_parser_google.run()
#     # except (KeyboardInterrupt, SystemExit):
#     #     print('Program was stopped by user.')
