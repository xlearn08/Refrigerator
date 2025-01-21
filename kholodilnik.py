from datetime import date, timedelta
from decimal import Decimal

def add(items, title, amount, expiration_date=None):
    """
    Добавляет товар в словарь items с указанным названием, количеством и 
    необязательной датой истечения срока годности.
    """
    # Определяем ключи, которые будут использоваться для хранения данных о товаре
    features_str = ('amount', 'expiration_date')

    # Проверяем, передана ли дата истечения срока годности
    if expiration_date is not None:
        # Разбираем строку даты в формате 'YYYY-MM-DD'
        expiration_date_parts = expiration_date.split('-')
        expiration_date_obj = date(
            int(expiration_date_parts[0]),
            int(expiration_date_parts[1]),
            int(expiration_date_parts[2])
        )
    else:
        expiration_date_obj = None

    # Создаём кортеж с данными, которые будут добавлены в словарь
    features = (amount, expiration_date_obj)
    
    # Создаём словарь из пар ключ-значение
    feature_dict = {key: value for key, value in zip(features_str, features)}

    # Если товара с таким названием ещё нет в items, создаём новый список
    # иначе добавляем новый элемент в существующий список
    if title not in items:
        items[title] = [feature_dict]
    else:
        items[title].append(feature_dict)


def add_by_note(items, note):
    """
    Добавляет товар в словарь items на основе строки note.
    Строка должна содержать название товара, количество и, возможно, дату истечения.
    """
    note_parts = note.split(' ')
    title = ''
    i = 0

    # Проверяем, является ли последняя часть строки датой
    if len(note_parts[-1]) == 10:  # Например, '2023-07-15'
        while i != len(note_parts) - 2:
            # Собираем название товара, исключая последние две части (сумму и дату)
            title += note_parts[i] + ' '
            i += 1
        title = title.rstrip(' ')  # Убираем лишний пробел в конце
        # Добавляем товар с датой истечения
        add(items, title, Decimal(note_parts[-2]), note_parts[-1])
    else:
        while i != len(note_parts) - 1:
            # Собираем название товара без даты
            title += note_parts[i] + ' '
            i += 1
        title = title.rstrip(' ')  # Убираем лишний пробел в конце
        # Добавляем товар без даты истечения
        add(items, title, Decimal(note_parts[-1]), None)


def find(items, needle):
    """
    Ищет все товары в словаре items, в названии которых встречается подстрока `needle`.
    """
    return [item for item in items.keys() if needle.lower() in item.lower()]


def amount(items, needle):
    """
    Считает общую сумму для товаров, в названии которых содержится подстрока `needle`.
    """
    total_amount = Decimal('0')  # Начальная сумма
    for item in items:
        if needle.lower() in item.lower():  # Если в названии товара есть подстрока
            for record in items[item]:
                total_amount += record['amount']  # Добавляем сумму товара
    return total_amount


def expire(items, in_advance_days=0):
    """
    Возвращает товары, срок годности которых истекает в течение `in_advance_days` дней 
    от текущей даты.
    """
    result = []  # Список для хранения результатов
    today = date.today()  # Текущая дата
    for title, records in items.items():
        total_amount = Decimal('0')  # Начальная сумма для товара
        for record in records:
            # Проверяем, если дата истечения меньше или равна текущей с учётом 'in_advance_days'
            if record['expiration_date'] and record['expiration_date'] <= today + timedelta(days=in_advance_days):
                total_amount += record['amount']  # Складываем сумму товара с истекающим сроком годности
        if total_amount > 0:  # Если сумма больше 0, добавляем товар в список результатов
            result.append((title, total_amount))
    return result


# Пример использования:
items = {}
# Добавляем товар с датой истечения
add(items, 'Яйца Фабрики №1', Decimal('4'), '2023-07-15')

# Выводим все товары в словаре
print(items)
