from requests import get, post
from json import load, dump, loads
from re import match
from lxml import html
from random import choice, shuffle
import traceback

from strings import *

serv_iter = None
serv = None
prox = None
failed = {}
clear_data = {}

with open('settings.json', encoding='utf-8') as f:
    settings = load(f)


def url_concat(pagination, item_xpathed):
    """
    Concatenating base and card links
    :param pagination: url to pagination
    :param item_xpathed: full/not full url to card
    :type pagination: string
    :type item_xpathed: string
    :return: full url to card
    """
    base = match(settings['regulars']['base'], pagination).group(0)
    for k, v in settings['format_templates'].items():
        if k in base:
            return v.format(base=base, item=item_xpathed)
    if item_xpathed.startswith(base):
        return item_xpathed[:8] + item_xpathed[8:].replace('//', '/')
    else:
        return (base + '/' + item_xpathed)[:8] + (base + '/' + item_xpathed)[
                                                 8:].replace('//', '/')


def get_proxy():
    """Получить свежие прокси Натана"""

    proxy_url = 'http://10.199.13.39:8085/get_data'
    proxy_lim = 500
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
        if not settings['proxies']:
            serv = list(map(lambda x: x['value'], loads(get_proxy())))
        else:
            serv = settings['proxies']
    nxt = choice(serv)
    return {nxt['schema']: nxt['proxy']}


with open('links1.json', encoding='utf-8') as f:
    links = load(f)
with open('data.json', encoding='cp1251') as f:
    data = load(f)

for k, v in list(data.items()):
    item = None
    pagination = None
    try:
        """
        Check for filtered from json addresses
        """
        if not k in links:
            print(filtered_msg.format(k))
            del data[k]
            continue

        print(testing_msg.format(k))

        for _ in range(settings['retries_count']):  # 20 retries
            try:
                pagination = get(links[k]['pagination'], proxies=prox, headers=settings['headers']).text
            except:
                print(settings['indent'] + proxy_err.format(prox["https"]) if prox else no_proxy_err)
                prox = proxy()
                continue
            else:
                break

        """
        Test for pagination expr and exprn
        """
        print(settings['indent'] + testing_pagination_msg, end='...')

        for e in list(v['expr']):
            if pagination.lower().find(e.lower()) != -1:
                failed.setdefault(k, []).append({'step': 'pagination', 'query': e, 'link': links[k]['pagination']})
                print(failed_msg)
                break
        else:
            print(ok_msg)

        """
        Trying to get new item from pagination using xpath from instruction
        """
        print(settings['indent'] + itemgetting_msg, end='.....')
        try:
            new_item = choice(html.fromstring(pagination).xpath(links[k]['path']))
            links[k]['item'] = url_concat(links[k]['pagination'], new_item)
        except Exception as e:
            failed.setdefault(k, []).append(
                {'step': 'item', 'pagination': links[k]['pagination'], 'path': links[k]['path']})
            print(failed_msg)
            print(settings['indent'] + getting_item_msg)
        else:
            print(ok_msg)

        """
        Trying to get an item from json if there is no item in instruction
        """
        for _ in range(settings['retries_count']):  # 20 retries
            try:
                item = get(url_concat(links[k]['pagination'], links[k]['item']), proxies=prox,
                           headers=settings['headers']).text if not new_item else get(
                    url_concat(links[k]['pagination'], new_item), headers=settings['headers']).text
            except:
                print(settings['indent'] + (proxy_err.format(prox['https']) if prox else no_proxy_err))
                prox = proxy()
                continue
            else:
                break

        """
        If we found item neither in pagination nor in instruction
        """
        print(settings['indent'] + testing_item_expr_msg, end='...')
        if not item:
            print(settings['indent'] + no_item_err + '...')
            continue

        """
        Item testing
        """
        for e in list(v['expr']):
            if item.lower().find(e.lower()) == -1:
                failed.setdefault(k, []).append({'step': 'expr', 'query': e, 'link': links[k]['item']})
                print(failed_msg)
                # quit()
                break
        else:
            print(ok_msg)

        print(settings['indent'] + testing_item_exprn_msg, end='...')
        for e in list(v['exprn']):
            if item.lower().find(e.lower()) != -1:
                failed.setdefault(k, []).append({'step': 'exprn', 'query': e, 'link': links[k]['item']})
                print(failed_msg)
                break
        else:
            print(ok_msg)

    # """
    # Main Exception-handler
    # """
    # TODO: make an error-recognizer
    except Exception as e:
        print(exception_caught_msg.format(str(e)))
        failed.setdefault(k, []).append({'Exception': str(e), 'content': v, 'Traceback': str(traceback.format_exc())})
    else:
        clear_data[k] = v

"""
Writing new data into files
"""
with open('errors.json', 'w') as f:
    dump(failed, f, ensure_ascii=False)

with open('data.json', 'w') as f:
    dump(data, f, ensure_ascii=False)

with open('clear_data.json', 'w') as f:
    dump(clear_data, f, ensure_ascii=False)
