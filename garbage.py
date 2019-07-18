from json import load, dump

with open('links1.json') as f:
    data = load(f)

try:
    for k, v in data.items():
        if 'path' in v:
            continue
        print(v['pagination'])
        path = input('XPATH: ')
        data[k]['path'] = path
except KeyboardInterrupt:
    with open('links.json', 'w') as f:
        dump(data, f, ensure_ascii=False)
else:
    with open('links1.json', 'w') as f:
        dump(data, f, ensure_ascii=False)
finally:
    with open('links1.json', 'w') as f:
        dump(data, f, ensure_ascii=False)
