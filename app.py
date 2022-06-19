from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

questions = [
    {
        'question': {
            'text': 'Согласны ли вы с утверждением, что Flask в Python используют для создания сайтов?',
        },
        'answer': 'да',
    },
    {
        'question': {
            'text': 'Можно ли на Flask написать API?',
        },
        'answer': 'да',
    },
    {
        'question': {
            'text': 'Приложения для {ОС}{операционной системы} Windows имеют разширение ".sh"?',
        },
        'answer': 'нет',
    },
    {
        'question': {
            'text': 'Можно ли в Unity написать игру?',
        },
        'answer': 'да',
    },
    {
        'question': {
            'text': 'Можно ли установить приложение на Android не загружая его в Google Play Market?',
        },
        'answer': 'да',
    },
    {
        'question': {
            'text': 'Приложения на андроид в основном пишутся на ^C{#}{шарп}^, верно?',
        },
        'answer': 'нет',
    },
    {
        'question': {
            'text': 'Изображения в opencv-python хранятся в памяти в виде {numpy}{нампай} array, это так?',
        },
        'answer': 'да',
    },
    {
        'question': {
            'text': 'Может ли компьютер найти на картинке машину и определить её цвет?',
        },
        'answer': 'да',
    },

]


@app.route('/', methods=['POST'])
def index():
    command = request.json['request']['command']

    response = {}
    response['version'] = request.json['version']
    response['session'] = request.json['session']

    response['response'] = {'end_session': False}

    if request.json['session']['new']:
        request.json['state']['session'] = {}
    response['session_state'] = request.json['state']['session']

    number = request.json['state']['session'].get('number', None)

    if 'amoгуsь' in command and ('вездеход' in command or 'вездекод' in command):
        response['response']['text'] = 'Привет {вездекодерам}{вездек`одерам}!'

    elif 'начать тест' == command:
        response['response']['text'] = questions[0]['question']['text'] + ' (ответьте только "да" или "нет")'
        response['session_state']['number'] = 0
        response['session_state']['user_ans'] = []

    elif number is not None and number <= 8:

        if command not in ('да', 'нет'):
            response['response']['text'] = 'ответьте только "да" или "нет"'
        else:
            if 'user_ans' in response['session_state']:
                response['session_state']['user_ans'].append(command == questions[number]['answer'])
            else:
                response['session_state']['user_ans'] = [command == questions[number]['answer']]
            number += 1
            if number != 8:
                response['response']['text'] = questions[number]['question']['text']
            else:
                user_ans = [0 for _ in range(4)]
                for x in range(4):
                    for i in range(x * 2, x * 2 + 2):
                        user_ans[x] += 1 if response['session_state']['user_ans'][i] else 0

                categories = ['Back End', 'GameDev', 'Мобильная разработка', 'Computer vision']

                user_categories = [categories[i] for i in range(len(categories)) if user_ans[i] == max(user_ans)]

                if max(user_ans) == 2:
                    response['response']['text'] = \
                        f'Вы отлично ответили на вопросы по категори{"ям" if len(user_categories) > 1 else "и"} ' \
                        f'{", ".join(user_categories)}. Рекомендую решить их в первую очередь.'
                    response['response']['tts'] = f'''
                        Вы отлично ответили на вопросы по категори{"ям" if len(user_categories) > 1 else "и"} \
                        {", ".join(user_categories)}.
                        <speaker audio=marusia-sounds/game-win-1>
                        Рекомендую решить их в первую очередь.
                    '''

                elif max(user_ans) == 1:
                    response['response']['text'] = \
                        f'Вы удовлетворительно ответили на вопросы по категори{"ям" if len(user_categories) > 1 else "и"} ' \
                        f'{", ".join(user_categories)}. Поэтому предлагаю Вам поучаствовать в ' \
                        f'{"них" if len(user_categories) > 1 else "нём"}, но можете посмотреть и другие категории.'
                    response['response']['tts'] = f'''
                        Вы удовлетворительно ответили на вопросы по категори{"ям" if len(user_categories) > 1 else "и"} \
                        {", ".join(user_categories)}. <speaker audio=marusia-sounds/game-win-3> Поэтому предлагаю Вам поучаствовать в ' \
                        {"них" if len(user_categories) > 1 else "нём"}, но можете посмотреть и другие категории.
                    '''
                else:
                    response['response']['text'] = 'Попробуйте любую категорию и приходите на следующий Вездекод.'
                    response['response']['tts'] = '''
                        Попробуйте любую категорию и приходите на следующий Вездекод.
                        <speaker audio=marusia-sounds/game-loss-1>
                    '''

                response['response']['end_session'] = True

        response['session_state']['number'] = number


    else:
        response['response']['text'] = 'Привет. Если хотите начать тест, скажите "начать тест"'

    return jsonify(response)


if __name__ == "__main__":
    app.run(ssl_context='adhoc', debug=True)
