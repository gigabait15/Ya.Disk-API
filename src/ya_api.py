import aiohttp


async def get(link: str, path: str):
    """
    функция для получения доступа к файлам яндекс диска
    :param link: ссылка на подключение к яндекс диску (находиться в config.py)
    :param path: публичная ссылка на яндекс диск
    :return: список с названиями файлов и ссылкой для скачивания
    """
    items_list = []
    async with aiohttp.ClientSession() as session:
        async with session.get(link + path, headers={'Accept': 'application/hal+json'}) as response:
            html = await response.json()
            for i in html.items():
                if i[0] == '_embedded':
                    for item in i[1]['items']:
                        if item.get('file') is None:
                            pass
                        else:
                            item_dict = {
                                'name': item.get('name'),
                                'link': item.get('file')
                            }
                            items_list.append(item_dict)
    return items_list


