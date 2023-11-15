import json
import re
import time


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
        self._deep = None

        self._cur_path = None
        self._cur_parse_urls = None
        self._cur_deep = None
        self._cur_domain = None
        self._cur_check_url = None
        # self._https = 'https://'
        # self._google = 'www.google.com/search?q='

        self._count = None

        self._save_file = 'result.json'
        self._re_domain = \
            r'https?:\/\/((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9])\/.*'

        self.set_folder(path=home_path)
        self.set_deep(deep=deep)

    def set_folder(self, path: str) -> None:
        if path is not None:
            self._dict_photo = {}.update({path: {}})

    def set_deep(self, deep: int) -> None:
        self._deep = deep

    # def set_google_search(self, search: str = 'python') -> None:
    #     self.set_folder(f'{self._https}{self._google}{search}')

    def print_info(self) -> None:
        print(json.dumps(self._dict_photo, indent=4, ensure_ascii=False, sort_keys=True))

    async def save_data_to_json(file_path: str, data: dict) -> json:
        try:
            with open(file_path, 'r') as json_file:
                data_from_file = json.load(json_file)

            try:
                _, data = data_from_file.update(data), data_from_file

            except AttributeError:
                print(f'AttributeError: object has no attribute "update"')

        except FileNotFoundError:
            print(f'FileNotFoundError: No such file or directory: {file_path}')
        except json.JSONDecodeError:
            print(f'JSONDecodeError')

    def save_info(self, file: str = None) -> None:
        if file is None:
            file = self._save_file
        with open(file, 'w') as json_file:
            json.dump(self._dict_photo, json_file, indent=4, ensure_ascii=False, sort_keys=True)

    def _read_info(self, file: str = None) -> None:
        async def save_data_to_json(path: str, data: dict) -> json:
            try:
                with open(path, 'r') as json_file:
                    data_from_file = json.load(json_file)

                try:
                    _, data = data_from_file.update(data), data_from_file

                except AttributeError:
                    print(f'AttributeError: object has no attribute "update"')

            except FileNotFoundError:
                print(f'FileNotFoundError: No such file or directory: {path}')
            except json.JSONDecodeError:
                print(f'JSONDecodeError')

    def _get_counter(self) -> None:
        return self._count

    def _update_counter(self) -> None:
        if self._count is None:
            self._count = 0
        self._count += 1
        return self._get_counter()

    def check_deep(self, deep: int) -> bool:
        return True if (self._deep is not None and deep < self._deep) else False

    def _get_url(self, urls: dict, deep: int = 0) -> None:
        if self.check_deep(deep):
            deep += 1

            for url in urls:
                print(f'count: {self._update_counter()}\t| deep: {deep}\t| url: {url}')

                self._get_urls_from_page(url)
                urls[url] = self._cur_parse_urls

                if urls[url]:
                    self._get_url(urls=urls[url], deep=deep)

    def _check_domain(self, url: str) -> str:
        match = re.fullmatch(self._re_domain, url)
        return match[1] if match and match[1] else ''

    def _get_domain_from_url(self, url: str) -> bool:
        self._cur_domain = self._check_domain(url)
        return True if self._cur_domain else False

    def _check_external_url(self, url: str) -> bool:
        domain = self._check_domain(url)
        return True if domain and domain != self._cur_domain else False

    def _get_urls_from_page(self, url: str) -> None:
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

    def run(self):
        self._get_url(urls=self._dict_photo, deep=0)


if __name__ == '__main__':
    start_url = r'https://www.google.com/search?q=requests'
    immersion_depth = 2

    renamer = PhotoHandler(home_path=start_url, deep=immersion_depth)

    try:
        renamer.run()
        print("--- %s seconds ---" % (time.time() - start_time))

        renamer.print_info()

        renamer.save_info()

    except (KeyboardInterrupt, SystemExit):
        print('Program was stopped by user.')

    # # for Example:
    # otus_parser_google = Parser()
    # otus_parser_google.set_google_search('BeautifulSoup')
    # otus_parser_google.set_deep = 3
    #
    # try:
    #     otus_parser_google.run()
    # except (KeyboardInterrupt, SystemExit):
    #     print('Program was stopped by user.')

