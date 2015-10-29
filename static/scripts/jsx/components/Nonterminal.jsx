{/*This will contain the Individual NonterminalSymbols which are nested within NonterminalList*/}
var React = require('react')
var ListGroupItem = require('react-bootstrap').ListGroupItem

var Nonterminal = React.createClass({
  propTypes: {
    name: React.PropTypes.string.isRequired,
    complete: React.PropTypes.bool.isRequired,
    onClick: React.PropTypes.func,
    deep: React.PropTypes.bool
  },

  render: function() {
    return(
          <ListGroupItem bsSize = "xsmall" bsStyle = {this.props.complete ? "success" : "danger" } onClick = {this.props.onClick}>{this.props.name}</ListGroupItem>
    );}


});

module.exports = Nonterminal
