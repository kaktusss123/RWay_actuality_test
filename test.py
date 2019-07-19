from lxml import html, etree
from requests import get, post
from json import load, loads
from random import choice


def test_text(url, text):
    return get(url).text.find(text)

def test_xpath(url, path):
    page = html.fromstring(get(url).text)
    return page.xpath(path)


serv, serv_iter = None, None

def get_proxy():
        '''Получить свежие прокси Натана'''

        proxy_url = 'http://10.199.13.39:8085/get_data'
        proxy_lim = 50
        proxy_offset = 86500

        json = {}
        json['topic'] = 'proxies'
        json['time_offset'] = proxy_offset
        json['amount'] = proxy_lim
        json['filter'] = ['schema', ['https']]
        resp = post(proxy_url, json=json)
        return resp.text


def proxy():
    """
    generate next proxy from list (free or personal)
    :return type: dict
    :return: {"https": "ip:host"}
    """
    global serv_iter
    global serv
    if not serv_iter:
        serv = list(map(lambda x: x['value'], loads(get_proxy())))
    nxt = choice(serv)
    return {nxt['schema']: nxt['proxy']}

if __name__ == '__main__':
    # with open('data.json', encoding='cp1251') as f:
    #     data = load(f)

    # with open('errors.json') as f:
    #     errors = load(f)

    # for i in data:
    #     if not i in errors:
    #         print(i)

    # for source, errs in data.items():
    #     print('Working with {}'.format(source))
    #     for err in errs:
    #         try:
    #             if 'Exception' in err:
    #                 continue
    #             if err['step'] == 'item':
    #                 print('XPath:', test_xpath(err['pagination'], err['path']))
    #             else:
    #                 print(err['step'], test_text(err['link'], err['query']))
    #         except etree.ParserError as e:
    #             print(e)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    url = 'https://aliant.pro/catalog/commercial/g.-vologda,-ul.-batyushkova,-d.-7'
    query = 'itemDescription'
    for i in range(20):
        try:
            text = get(url, headers=headers).text
            print(text.find(query))
        except:
            print('Retry {}'.format(i+1))
            continue
        else:
            break



    # with open('clear_data.json') as f:
    #     print(*list(load(f).keys()), sep='\n')