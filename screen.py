from flask import *
from flask import Flask, render_template
from 聊天交互 import *
import json

app = Flask(__name__)
answer = ''
handler = chat()
dict_info = {}
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['get', 'POST', 'PUT'])
def result():
    global dict_info
    name = request.args.get('name')
    if name is not None:
        # print(name)
        answer = handler.chat_main(str(name))
        # print(answer)
        dict_info = {'a': str(answer)}
        return json.dumps(dict_info)
    else:
        # print(dict_info)
        return json.dumps(dict_info)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5902)

from flask import *
from flask import Flask, render_template
from 聊天交互 import *
import json

app = Flask(__name__)
answer = ''
handler = chat()
dict_info = {}
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['get', 'POST', 'PUT'])
def result():
    global dict_info
    name = request.args.get('name')
    if name is not None:
        # print(name)
        answer = handler.chat_main(str(name))
        # print(answer)
        dict_info = {'a': str(answer)}
        return json.dumps(dict_info)
    else:
        # print(dict_info)
        return json.dumps(dict_info)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5902)
