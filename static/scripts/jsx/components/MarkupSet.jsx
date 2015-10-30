var React = require('react')
var DropdownButton = require('react-bootstrap').DropdownButton

var MarkupSet = React.createClass({
  
  propTypes: {
    current_set:      React.PropTypes.shape({
      set: React.PropTypes.string,
      tags: React.PropTypes.array}),
    present_nt:      React.PropTypes.shape({
      set: React.PropTypes.string,
      tags: React.PropTypes.array})
  },

  render: function() {

  var set_length = []


  return(<div>{this.props.current_set.set} {this.props.present_nt.tags}</div>);
  }

});

module.exports = MarkupSet



