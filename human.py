from json import load, dump
from test import *

with open('errors.json', encoding='cp1251') as f:
    data = load(f)


for source, errs in data.items():
    print('Ошибка в сервисе {}.'.format(source))
    for err in errs:
        if 'step' in err:
            if err['step'] == 'pagination' or err['step'] == 'exprn':
                print('На странице {}\nнайдена строка {}. Ее там быть не должно.'.format(err['link'], err['query']))
                print('Это правда' if test_text(err['link'], err['query']) != -1 else 'Это ложь')
                input()
            if err['step'] == 'expr':
                print('На странице {}\nне найдена строка {}. Должна быть там'.format(err['link'], err['query']))
                print('Это правда' if test_text(err['link'], err['query']) == -1 else 'Это ложь')
                input()