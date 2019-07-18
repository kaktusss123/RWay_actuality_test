from json import load, dump

with open('errors.json', encoding='cp1251') as f:
    data = load(f)


for source, errs in data.items():
    print('Ошибка в сервисе {}.'.format(source))
    for err in errs:
        if 'step' in err:
            if err['step'] == 'pagination' or err['step'] == 'exprn':
                print('На странице {}\nнайдена строка {}. Ее там быть не должно.'.format(err['link'], err['query']))
                input()
            if err['step'] == 'expr':
                print('На странице {}\nне найдена строка {}. Должна быть там'.format(err['link'], err['query']))
                input()