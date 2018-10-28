from flask import Flask, request, render_template, url_for, redirect, flash, json, session, Blueprint
import flask_login
from pymongo import MongoClient
from passlib.hash import sha256_crypt
import requests
from os import urandom, remove
from binascii import hexlify
import utility.flask_loginmanager as log
from paths.OnlineIde.OnlineIdeSingleton import Singleton

app = Blueprint('online_ide', __name__)


languages = {"ada": 53,"bash": 14, "brainfuck": 19, "c": 1,"clojure": 13,"cobol": 36, "coffeescript": 59, "cpp": 2, "cpp14": 58,
             "csharp": 9,"db2": 44,"elixir": 52, "erlang": 16, "fortran": 54,"fsharp": 33, "go": 21, "groovy": 31,
             "haskell": 12, "haxe": 69, "java": 3, "nodejs": 20,"julia": 57, "kotlin": 71, "lolcode": 38, "lua": 18,
             "maven": 45, "mysql": 10, "prolog": 64, "objectivec": 32, "ocaml": 23, "octave": 46, "oracle": 11,
             "pascal": 25, "perl": 6, "php": 7, "pypy": 61, "pypy3": 62,"python2": 5, "python3": 30, "r": 24, "racket": 49, "ruby": 8,
             "rust": 50, "d": 26, "sbt": 70,"scala": 15, "smalltalk": 39, "swift": 51, "tcl": 40, "text": 28,
             "tsql": 42, "visualbasic": 37, "whitespace": 41, "unlamda": 48}




class OnlineIde(metaclass=Singleton):

    def hackerrank_api(username=None, title=None, code=None, language=None, input_=None):
        language = int(language)
        s_lang = (list(languages.keys())[list(languages.values()).index(language)])
        print(s_lang)
        try:
            RUN_URL = 'https://api.jdoodle.com/v1/execute'
            headers = {'content-type': 'application/json'}
            data = {
                'script': code,
                'language': s_lang,
                'stdin': input_,
                'versionIndex': '0',
                'clientId': '5cd01283205107ec2f32a6380c097804',
                'clientSecret': '9c7bb43dab2f76c610a7ed85870d00d20754e9717a0e09bd3d1fc9cbd457165a',

            }

            r = requests.post(RUN_URL, data=json.dumps(data), headers=headers)
            response = r.json()
            output = response['output']
            result = "Compilation Error"
            time = None
            mem = None
            print(response)
            if output:
                message = response['statusCode']
                if message == 200:
                    result = "Successfully Executed"
                    output = response['output']
                    time = response['cpuTime']
                    mem = response['memory']
                elif message != "200":
                    result = "Runtime Error"
                    output = response['error']
        except Exception as e:
            print(e)
            result = "Unable to process your request. Please try again later. Sorry for inconvenience."
            output = None
            time = None
            mem = None
        O_IDE = {}
        O_IDE['code'] = code
        O_IDE['lang'] = int(language)
        O_IDE['input'] = input_
        O_IDE['output'] = output
        O_IDE['result'] = result
        O_IDE['time'] = time
        O_IDE['memory'] = mem
        if username is not None:
            # Authenticated User
            O_IDE['username'] = username
            O_IDE['title'] = title
        # print(O_IDE)
        return O_IDE


@app.route('/online_ide/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template("/editor/home.html", **locals(), languages=languages)
    elif request.method == 'POST':
        code = request.form.get('code')
        language = request.form.get('lang')
        input_ = request.form.get('testcase')
        if language == "-1":
            flash("Please enter language")
            return render_template("/editor/home.html", **locals(), languages=languages)
        if input_ == "":
            input_ = " "
        ide = OnlineIde()
        guest = ide.hackerrank_api(code=code, language=language, input_=input_)
        flag = False
        if guest['result'] == "Successfully Executed":
            flag = True
        return render_template('/editor/home_submit.html', **locals(), input=input_,
                               output=guest['output'],
                               result=guest['result'], time=guest['time'], mem=guest['memory'], languages=languages)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("/editor/404.html", **locals())


