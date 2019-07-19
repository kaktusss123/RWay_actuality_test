from json import load

with open('clear_data.json', encoding='cp1251') as f:
    print(*load(f).keys(), sep='\n')