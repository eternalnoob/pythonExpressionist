{/*This is responsible for rendering and correctly updating and displaying the rules within the RuleBar*/}
var React = require('react')

var Rule = React.createClass({
  prop_types: {
  expansion: React.PropTypes.string,
  app_rate: React.PropTypes.number
  },

  render:function() {
    return( <h3> {this.props.expansion} test itout </h3>);
  }
});
module.exports = Rule
