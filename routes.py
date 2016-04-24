import os
import re

from flask import session, request, render_template, Blueprint

import Markups
import NonterminalSymbol
import PCFG
from models import Grammar
from database import db

webapp = Blueprint('webapp', __name__)


def return_grammar_obj(name):
    gram_json = Grammar.query.filter_by(name=name).first()
    if gram_json:
        return gram_json.ret_obj()
    else:
        return None

def fetch_db_rep(name):
    return Grammar.query.filter_by(name=name).first()

def update_gram_db(name, grammar):
    fetch_db_rep(name).update(grammar)
    db.session.commit()

@webapp.route('/api/default', methods=['GET'])
def default():
    if 'grammarname' in session:
        print("grammar name")
        x = return_grammar_obj(session['grammarname'])
        if x:
            print("grammar exists")
            return x.to_json()
        else:
            print("grammar does not exists")
            return new_grammar().to_json()

    else:
        x = new_grammar()
        return x.to_json()




@webapp.route('/api/grammar/load', methods=['POST'])
def load_grammar():
    """
    Load a grammar from a json representation sent as a request
    """
    print request
    global flask_grammar
    flask_grammar = PCFG.from_json(str(request.data))
    return flask_grammar.to_json()


@webapp.route('/api/grammar/from_file', methods=['POST'])
def load_file_grammar():
    """
    Load a grammar from a file JSON representation
    """
    global flask_grammar
    grammar_name = secure_filename(request.data)
    user_file = os.path.abspath(os.path.join(os.path.dirname(__file__), ''.join(['grammars/load/', grammar_name])))
    grammar_file = open(user_file, 'r')
    if grammar_file:
        flask_grammar = PCFG.from_json(str(grammar_file.read()))
    return flask_grammar.to_json()


@webapp.route('/api/grammar/rename', methods=['POST'])
def rename_grammar():
    data = request.get_json()
    oldname = session['grammarname']
    newname = data['newname']
    x = fetch_db_rep(oldname)
    x.rename(newname)
    db.session.commit()
    session['grammarname'] = newname
    return 'renamed grammar'

@webapp.route('/api/grammar/load_existing', methods=['POST'])
def load_existing_grammar():
    data = request.get_json()
    grammar = data['grammarname']
    if fetch_db_rep(grammar):
        session['grammarname'] = grammar
    return 'loaded new grammar'



@webapp.route('/api/grammar/save', methods=['GET', 'POST'])
def save_grammar():
    """
    Save a file as JSON representation within the grammars directory
    """
    grammar_name = secure_filename(request.data)
    filename = os.path.abspath(os.path.join(os.path.dirname(__file__), ''.join(['grammars/load/', grammar_name])))
    outfile = open(filename, 'w+')
    outfile.write(flask_grammar.to_json(to_file=True))
    return "saving new grammar"


@webapp.route('/api/grammar/new', methods=['GET'])
def new_grammar():
    """
    Delete current grammar and start over
    """
    if 'grammarname' in session:
        grammar = Grammar.query.filter_by(name=session['grammarname']).first()
        if grammar:
            grammar.update(PCFG.PCFG())
        else:
            gram = PCFG.PCFG()
            x = Grammar(gram, session['grammarname'])
            db.session.add(x)
            db.session.commit()
            grammar = x
        return grammar.ret_obj()
    else:
        session['grammarname']='test'
        if not fetch_db_rep('test'):
            gram = PCFG.PCFG()
            x = Grammar(gram, 'test')
            print("wowee")
            db.session.add(x)
            db.session.commit()
            print("wowee")
            return x.ret_obj()
        else:
            return return_grammar_obj()


@webapp.route('/api/grammar/export', methods=['GET', 'POST'])
def export_grammar():
    """
    TODO: REMOVE defunct function
    """
    filename = ''.join(['grammars/exports/', request.data])
    print 'Exporting to {}...'.format(filename)
    flask_grammar.export_all(filename)
    print 'Finished export.'
    return "exporting grammar database"


@webapp.route('/api/nonterminal/add', methods=['POST'])
def add_nt():
    data = request.get_json()
    #print("WHERE U AT FAM")
    # Strip off excess brackets
    data['nonterminal'] = re.search('[^\[\]]+', data['nonterminal']).group(0)
    #print(data['nonterminal'])
    name = session['grammarname']
    grammar = return_grammar_obj(session['grammarname'])
    grammar.add_nonterminal(NonterminalSymbol.NonterminalSymbol(data['nonterminal']))
    update_gram_db(name, grammar)
    return grammar.to_json()


@webapp.route('/api/nonterminal/rename', methods=['POST'])
def rename_nt():
    data = request.get_json()
    old = re.search('[^\[\]]+', data['old']).group(0)
    new = re.search('[^\[\]]+', data['new']).group(0)
    name = session['grammarname']
    grammar = return_grammar_obj(session['grammarname'])
    grammar.modify_tag(old, new)
    update_gram_db(name, grammar)
    return grammar.to_json()


@webapp.route('/api/nonterminal/delete', methods=['POST'])
def delete_nt():
    data = request.get_json()
    nonterminal = re.search('[^\[\]]+', data['nonterminal']).group(0)
    name = session['grammarname']
    grammar = return_grammar_obj(session['grammarname'])
    grammar.delete_nonterminal(nonterminal)
    update_gram_db(name, grammar)
    return grammar.to_json()


@webapp.route('/api/nonterminal/deep', methods=['POST'])
def set_deep():
    data = request.get_json()
    grammar = return_grammar_obj(session['grammarname'])
    nonterminal = grammar.nonterminals.get(data["nonterminal"])
    if nonterminal:
        if nonterminal.deep:
            nonterminal.deep = False
        else:
            nonterminal.deep = True

    update_gram_db(session['grammarname'], grammar)
    return grammar.to_json()


@webapp.route('/api/nonterminal/expand', methods=['POST', 'GET'])
def expand_nt():
    data = request.get_json()
    grammarname = session['grammarname']
    grammar = return_grammar_obj(grammarname)
    return grammar.expand(NonterminalSymbol.NonterminalSymbol(data['nonterminal'])).to_json()


@webapp.route('/api/rule/expand', methods=['POST', 'GET'])
def expand_rule():
    data = request.get_json()
    grammarname = session['grammarname']
    grammar = return_grammar_obj(grammarname)
    return grammar.expand_rule(data['nonterminal'], int(data['index']) ).to_json()


@webapp.route('/api/rule/swap', methods=['POST'])
def swap_rule():
    data = request.get_json()
    index = int(data['index'])
    original = re.search('[^\[\]]+', data['original']).group(0)
    new = re.search('[^\[\]]+', data['new']).group(0)
    grammar = return_grammar_obj(session['grammarname'])
    grammar.copy_rule(original, index, new)
    update_gram_db(session['grammarname'], grammar)
    return grammar.to_json()


@webapp.route('/api/rule/add', methods=['POST'])
def add_rule():
    data = request.get_json()
    rule = data['rule']
    app_rate = int(data['app_rate'])
    nonterminal = NonterminalSymbol.NonterminalSymbol(data["nonterminal"])
    grammar = return_grammar_obj(session['grammarname'])
    grammar.add_rule(nonterminal, PCFG.parse_rule(rule), app_rate)
    update_gram_db(session['grammarname'],grammar)
    return grammar.to_json()


@webapp.route('/api/rule/delete', methods=['POST'])
def del_rule():
    data = request.get_json()
    rule = int(data['rule'])
    nonterminal = data['nonterminal']
    grammar = return_grammar_obj(session['grammarname'])
    grammar.remove_rule_by_index(NonterminalSymbol.NonterminalSymbol(nonterminal), rule)
    update_gram_db(session['grammarname'],grammar)
    return grammar.to_json()


@webapp.route('/api/rule/modify_expansion', methods=['POST'])
def modify_rule_expansion():
    data = request.get_json()
    rule = int(data['rule'])
    nonterminal = data['nonterminal']
    new = str(data['expansion'])
    grammar = return_grammar_obj(session['grammarname'])
    grammar.modify_rule(nonterminal, rule, new)
    update_gram_db(session['grammarname'], grammar)
    return grammar.to_json()


@webapp.route('/api/rule/set_app', methods=['POST'])
def set_app():
    data = request.get_json()
    rule = data['rule']
    nonterminal = data['nonterminal']
    app_rate = int(data['app_rate'])
    grammar = return_grammar_obj(session['grammarname'])
    grammar.modify_application_rate(NonterminalSymbol.NonterminalSymbol(nonterminal), rule, app_rate)
    update_gram_db(session['grammarname'], grammar)
    return grammar.to_json()


@webapp.route('/api/markup/addtag', methods=['POST'])
def add_tag():
    data = request.get_json()
    markupSet = Markups.MarkupSet(data['markupSet'])
    markup = Markups.Markup(data['tag'], markupSet)
    grammar = return_grammar_obj(session['grammarname'])
    grammar.add_unused_markup(markup)
    update_gram_db(session['grammarname'], grammar)
    return grammar.to_json()


@webapp.route('/api/markup/addtagset', methods=['POST'])
def add_tagset():
    data = request.get_json()
    markupSet = Markups.MarkupSet(data["markupSet"])
    grammar = return_grammar_obj(session['grammarname'])
    grammar.add_new_markup_set(markupSet)
    update_gram_db(session['grammarname'],grammar)
    return grammar.to_json()


@webapp.route('/api/markup/toggle', methods=['POST'])
def toggle_tag():
    data = request.get_json()
    print data
    nonterminal = NonterminalSymbol.NonterminalSymbol(data["nonterminal"])
    markupSet = Markups.MarkupSet(data['markupSet'])
    markup = Markups.Markup(data['tag'], markupSet)
    grammar = return_grammar_obj(session['grammarname'])
    grammar.toggle_markup(nonterminal, markup)
    update_gram_db(session['grammarname'], grammar)

    return grammar.to_json()


@webapp.route('/api/markup/renameset', methods=['POST'])
def rename_markupset():
    data = request.get_json()
    oldset = data['oldset']
    newset = data['newset']
    grammar = return_grammar_obj(session['grammarname'])
    grammar.modify_markupset(oldset, newset)
    update_gram_db(session['grammarname'], grammar)
    return grammar.to_json()


@webapp.route('/api/markup/renametag', methods=['POST'])
def rename_markuptag():
    data = request.get_json()
    markupset = data['markupset']
    oldtag = data['oldtag']
    newtag = data['newtag']
    grammar = return_grammar_obj(session['grammarname'])
    grammar.modify_markup(markupset, oldtag, newtag)
    update_gram_db(session['grammarname'], grammar)
    return grammar.to_json()


@webapp.route('/', defaults={'path': ''})
@webapp.route('/<path:path>')
def index(path):
    return render_template('index.html')