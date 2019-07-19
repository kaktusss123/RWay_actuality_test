from json import load, dump

with open('../data.json', encoding='cp1251') as f:
    data = load(f)

with open('../errors.json', encoding='cp1251') as f:
    errors = load(f)

clear = {}
for k, v in data.items():
    if k not in errors:
        clear[k] = v

with open('clear_data.json', 'w', encoding='cp1251') as f:
    dump(clear, f, ensure_ascii=False)
