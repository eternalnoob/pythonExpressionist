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

@app.route('/nonterminal/add' , methods = ['POST'])
def add_nt():
    data = request.get_json()
    flask_grammar.add_nonterminal( grammar.NonterminalSymbol(data['nonterminal']))
    return data['nonterminal']

@app.route('/nonterminal/deep' , methods = [ 'POST'])
def set_deep():
    data = request.get_json()
    nonterminal = flask_grammar.nonterminals.get(data["nonterminal"])
    if nonterminal:
        if nonterminal.deep:
            nonterminal.deep = False
        else:
            nonterminal.deep = True

    return "another tests"

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
    return "tested once more"


@app.route('/rule/delete' , methods = ['POST'])
def del_rule():
    data = request.get_json()
    rule = int(data['rule'])
    nonterminal = data['nonterminal']
    flask_grammar.remove_rule_by_index(grammar.NonterminalSymbol(nonterminal), rule)
    return " are we deleting a rule here?"

@app.route('/rule/set_app' , methods = ['POST'])
def set_app():
    data = request.get_json()
    rule = data['rule']
    nonterminal = data['nonterminal']
    app_rate = data['app_rate']
    flask_grammar.modify_application_rate(grammar.NonterminalSymbol(nonterminal), rule, app_rate)
    return ""

@app.route('/markup/addtag' , methods = ['POST'])
def add_tag():
    data = request.get_json()
    markupSet = grammar.MarkupSet(data['markupSet'])
    markup = grammar.Markup(data['tag'], markupSet)
    flask_grammar.add_unused_markup(markup)
    return ""

@app.route('/markup/addtagset' , methods = ['POST'])
def add_tagset():
    data = request.get_json()
    markupSet = grammar.MarkupSet(data["markupSet"])
    flask_grammar.add_new_markup_set(markupSet)
    return ""

@app.route('/markup/toggle' , methods = ['POST'])
def toggle_tag():
    data = request.get_json()
    print data
    nonterminal = grammar.NonterminalSymbol(data["nonterminal"])
    markupSet = grammar.MarkupSet(data['markupSet'])
    markup = grammar.Markup(data['tag'], markupSet)

    flask_grammar.toggle_markup(nonterminal, markup)

    return ""


@app.route('/export', methods =  ['POST'])
def export_dir():
    return ""

if __name__ == '__main__':
    flask_grammar = test
    app.debug = debug
    app.run()

