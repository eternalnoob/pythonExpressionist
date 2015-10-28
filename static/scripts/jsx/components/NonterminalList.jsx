{/*This will contain the list of nonterminals as nested components,
 as well as a add button to add a new Nonterminal at the bottom of the bar
 This has props of an array of Nonterminals And an Array of Markups representing
 Markups defined in the Grammar.*/}

var Nonterminal = require('./Nonterminal.jsx')


NonterminalList = react.CreateClass({
  propTypes: {
    markups: React.PropTypes.array,
    nonterminals: React.PropTypes.arrayOf(React.propTypes.shape({
      name:  React.propTypes.string,
      rules: React.propTypes.array,
      markup: React.propTypes.array,
      complete: React.propTypes.bool,
      deep: React.propTypes.bool
    }))
  },
  getDefaultProps: function() {
    return{
      markups: [],
      nonterminals: []
    };
  },

  handleClick: function(i) {
    console.log('You Clicked Nonterminal: ' + this.props.nonterminals[i].name + ' With Markup: ' +this.props.nonterminals[i].markup);
  },
  render: function() {
    return(
      <div>
        {this.props.nonterminals.map(function(nonterminal,i) {
          return(
            <Nonterminal {...nonterminal} onClick={this.handleClick.bind(this, i)} key={nonterminal.name}>{nonterminal.name}</Nonterminal>
          );
        }, this)}
      </div>
    );
  }
});
            
    
