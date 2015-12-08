from flask import Flask, render_template, request, jsonify
from test_gram import test
import grammar

app = Flask(__name__)
debug = True

@app.route('/' , methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/default' , methods = ['GET'])
def default():
    return flask_grammar.to_json()

"""
globals are horrible in these two, but because we're not in python 3.x
we don't have nonlocal keywords. Make sure we modify our copy instead of make a new one this way
"""

@app.route('/grammar/load', methods = ['POST'])
def load_grammar():
    print request.data
    global flask_grammar
    flask_grammar = grammar.from_json(str(request.data))
    return flask_grammar.to_json()

@app.route('/grammar/save', methods = ['POST'])
def save_grammar():
    return flask_grammar.to_json()

@app.route('/grammar/new', methods = ['GET'])
def new_grammar():
    global flask_grammar
    flask_grammar = grammar.PCFG()
    return flask_grammar.to_json()

@app.route('/nonterminal/add' , methods = ['POST'])
def add_nt():
    data = request.get_json()
    flask_grammar.add_nonterminal( grammar.NonterminalSymbol(data['nonterminal']))
    return flask_grammar.to_json()

@app.route('/nonterminal/deep' , methods = [ 'POST'])
def set_deep():
    data = request.get_json()
    nonterminal = flask_grammar.nonterminals.get(data["nonterminal"])
    if nonterminal:
        if nonterminal.deep:
            nonterminal.deep = False
        else:
            nonterminal.deep = True

    return flask_grammar.to_json()

@app.route('/nonterminal/expand', methods=['POST', 'GET'])
def expand_nt():
    data = request.get_json()
    return test.expand(grammar.NonterminalSymbol(data['nonterminal'])).to_json()

@app.route('/rule/add', methods=['POST'])
def add_rule():
    data = request.get_json()
    rule = data['rule']
    app_rate = int(data['app_rate'])
    nonterminal = grammar.NonterminalSymbol(data["nonterminal"])
    flask_grammar.add_rule(nonterminal, grammar.parse_rule(rule), app_rate)
    return flask_grammar.to_json()


@app.route('/rule/delete' , methods = ['POST'])
def del_rule():
    data = request.get_json()
    rule = int(data['rule'])
    nonterminal = data['nonterminal']
    flask_grammar.remove_rule_by_index(grammar.NonterminalSymbol(nonterminal), rule)
    return flask_grammar.to_json()

@app.route('/rule/set_app' , methods = ['POST'])
def set_app():
    data = request.get_json()
    rule = data['rule']
    nonterminal = data['nonterminal']
    app_rate = int(data['app_rate'])
    flask_grammar.modify_application_rate(grammar.NonterminalSymbol(nonterminal), rule, app_rate)
    return flask_grammar.to_json()

@app.route('/markup/addtag' , methods = ['POST'])
def add_tag():
    data = request.get_json()
    markupSet = grammar.MarkupSet(data['markupSet'])
    markup = grammar.Markup(data['tag'], markupSet)
    flask_grammar.add_unused_markup(markup)
    return flask_grammar.to_json()

@app.route('/markup/addtagset' , methods = ['POST'])
def add_tagset():
    data = request.get_json()
    markupSet = grammar.MarkupSet(data["markupSet"])
    flask_grammar.add_new_markup_set(markupSet)
    return flask_grammar.to_json()

@app.route('/markup/toggle' , methods = ['POST'])
def toggle_tag():
    data = request.get_json()
    print data
    nonterminal = grammar.NonterminalSymbol(data["nonterminal"])
    markupSet = grammar.MarkupSet(data['markupSet'])
    markup = grammar.Markup(data['tag'], markupSet)

    flask_grammar.toggle_markup(nonterminal, markup)

    return flask_grammar.to_json()


@app.route('/export', methods =  ['POST'])
def export_dir():
    flask_grammar.export_all()
    return "exported grammars"

if __name__ == '__main__':
    global flask_grammar
    flask_grammar = test
    app.debug = debug
    app.run()

