{/*This will contain the Individual NonterminalSymbols which are nested within NonterminalList*/}
var React = require('react')
var RuleBar = require('./RuleBar.jsx') 

var Nonterminal = React.createClass({
  propTypes: {
    name: React.PropTypes.string.isRequired,
    rules: React.PropTypes.array.isRequired,
    markup: React.PropTypes.array.isRequired,
    onClick: React.PropTypes.func
  },

  render: function() {
          {/*
            <div>
              {this.props.rules.map(function(derivation, i) {
                  return(<Rule expansion={derivation} key={i}/>);
                  }
              ),this}
              {this.props.markup.map(function(tag, i) {
                  return(<Markup representation={tag} key={i}/>);
                  }
              ),this}
            </div>
          */}
    return(
        <RuleBar rules = {this.props.rules}/>
    );}


});

module.exports = Nonterminal
