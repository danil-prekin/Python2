import datetime
import os
import random
import re
from flask import Flask

app = Flask(__name__)

CARS_LIST = ['Chevrolet', 'Renault', 'Ford', 'Lada']

CAT_BREEDS = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']

counter_visits = 0

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_PATH = os.path.join(BASE_DIR, 'war_and_peace.txt')

def get_words_from_book():
    try:
        with open(BOOK_PATH, 'r', encoding='utf-8') as f:
            text = f.read()
        words = re.findall(r'\b[а-яёa-z]+\b', text, re.IGNORECASE)
        return words
    except FileNotFoundError:
        return ['война', 'мир', 'толстой', 'книга']

WORDS_LIST = get_words_from_book()

@app.route('/hello_world')
def hello_world():
    return '<h1>Привет, мир!</h1>'


@app.route('/cars')
def cars():
    return ', '.join(CARS_LIST)


@app.route('/cats')
def cats():
    random_breed = random.choice(CAT_BREEDS)
    return random_breed


@app.route('/get_time/now')
def get_time_now():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f'Точное время: {current_time}'


@app.route('/get_time/future')
def get_time_future():
    future_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    future_time_str = future_time.strftime('%Y-%m-%d %H:%M:%S')
    return f'Точное время через час будет {future_time_str}'


@app.route('/get_random_word')
def get_random_word():
    random_word = random.choice(WORDS_LIST)
    return random_word


@app.route('/counter')
def counter():
    global counter_visits
    counter_visits += 1
    return str(counter_visits)


if __name__ == '__main__':
    app.run(debug=True)
