{/*This is responsible for rendering and correctly updating and displaying the rules within the RuleBar*/}
var React = require('react')

var Rule = React.createClass({
  prop_types: {
  expansion: React.PropTypes.string,
  app_rate: React.PropTypes.number
  },

  render:function() {
    return( <div> {this.props.expansion}test itout {this.props.app_rate}  </div>);
  }
});
module.exports = Rule
