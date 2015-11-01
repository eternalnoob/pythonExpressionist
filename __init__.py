from flask import Flask, render_template, request
from test_gram import test
from grammar import NonterminalSymbol

app = Flask(__name__)
debug = True

@app.route('/' , methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/default' , methods = ['GET', 'POST'])
def default():
    return test.to_json()

@app.route('/nonterminal/add' , methods = ['GET', 'POST'])
def add_nt():
    return "test"

@app.route('/nonterminal/deep' , methods = ['GET', 'POST'])
def set_deep():
    return "another tests"

@app.route('/nonterminal/expand' , methods = ['GET', 'POST'])
def expand_nt():
    return test.expand(NonterminalSymbol("ask_day")).to_json()

@app.route('/rule/add' , methods = ['GET', 'POST'])
def add_rule():
    return "tested once more"


@app.route('/rule/delete' , methods = ['GET', 'POST'])
def del_rule():
    return ""

@app.route('/rules/set_app' , methods = ['GET', 'POST'])
def set_app():
    return ""

@app.route('/markup/addtag' , methods = ['GET', 'POST'])
def add_tag():
    return ""

@app.route('/markup/addtagset' , methods = ['GET', 'POST'])
def add_tagset():
    return ""

@app.route('/markup/toggle' , methods = ['GET', 'POST'])
def toggle_tag():
    return ""


if __name__ == '__main__':
    app.debug = debug
    app.run()

