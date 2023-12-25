import json


async def save_data_to_json(path: str, data: dict) -> json:
    try:
        # with open(path, 'r', encoding='utf-8') as json_file:
        with open(path, 'r') as json_file:
            data_from_file = json.load(json_file)

        try:
            _, data = data_from_file.update(data), data_from_file

        except AttributeError:
            print(f'AttributeError: object has no attribute "update"')

    except FileNotFoundError:
        print(f'FileNotFoundError: No such file or directory: {path}')
    except json.JSONDecodeError as e:
        print(f'JSONDecodeError: {e}')
    # except UnicodeEncodeError as e:
        # print(f'UnicodeEncodeError: {e}')

    with open(path, 'w') as json_file:
        # Convert Python to JSON
        # https://www.geeksforgeeks.org/how-to-convert-python-dictionary-to-json/
        # JSON string with double quotes (ensure_ascii=False)
        # JSON string with sorted keys (sort_keys=True)
        json.dump(data, json_file, indent=4, ensure_ascii=False, sort_keys=True)

    # return json_object


async def print_data_from_json(data: [dict, json]):
    if isinstance(data, dict):
        data = json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True)

    # Print JSON object
    print(data)


if __name__ == '__main__':
    import asyncio

    data_file = r'../db/.data__2023.12.04.json'
    test_data = {"id": 121, "name": "Naveen", "course": "MERN Stack"}

    asyncio.run(save_data_to_json(data_file, test_data))

    with open(data_file, 'r') as file:
        try:
            data_json = json.load(file)

            asyncio.run(print_data_from_json(data_json))
        except json.JSONDecodeError:
            print(f'JSON file is Empty')

