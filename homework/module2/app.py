import os
import sys
from datetime import datetime
from flask import Flask, abort

app = Flask(__name__)

WEEKDAYS = ('понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье')

@app.route('/hello-world/<name>')
def hello_world(name):
    weekday_num = datetime.today().weekday()
    day_name = WEEKDAYS[weekday_num]
    return f'Привет, {name}. Хорошего {day_name}!'


@app.route('/max_number/<path:numbers>')
def max_number(numbers):
    parts = numbers.split('/')
    nums = []
    for p in parts:
        try:
            nums.append(int(p))
        except ValueError:
            return f'Ошибка: "{p}" не является числом', 400
    if not nums:
        return 'Не передано ни одного числа', 400
    maximum = max(nums)
    return f'Максимальное число: <i>{maximum}</i>'


@app.route('/preview/<int:size>/<path:relative_path>')
def preview(size, relative_path):
    abs_path = os.path.abspath(relative_path)
    if not os.path.exists(abs_path):
        abort(404, description='Файл не найден')
    if not os.path.isfile(abs_path):
        abort(400, description='Указанный путь не является файлом')

    try:
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read(size)
    except Exception as e:
        abort(500, description=f'Ошибка чтения файла: {e}')

    actual_size = len(content)
    return f'<b>{abs_path}</b> {actual_size}<br>{content}'


storage = {}

@app.route('/add/<date>/<int:number>')
def add_expense(date, number):
    if len(date) != 8 or not date.isdigit():
        return 'Неверный формат даты. Используйте YYYYMMDD', 400
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:])

    if not (1 <= month <= 12):
        return 'Неверный месяц', 400
    storage.setdefault(year, {}).setdefault(month, 0)
    storage[year][month] += number
    return f'Добавлено {number} руб. за {date}'


@app.route('/calculate/<int:year>')
def calculate_year(year):
    if year not in storage:
        return f'За {year} год трат нет', 404
    total = sum(storage[year].values())
    return f'Суммарные траты за {year} год: {total} руб.'


@app.route('/calculate/<int:year>/<int:month>')
def calculate_month(year, month):
    if year not in storage or month not in storage[year]:
        return f'За {year}-{month:02d} трат нет', 404
    total = storage[year][month]
    return f'Суммарные траты за {year}-{month:02d}: {total} руб.'


if __name__ == '__main__':
    app.run(debug=True)
