{/* This is responsible for rendering the Rule Bar, which is attached directly to the Main interface*/}
var React = require('react')
var Rule = require('./Rule.jsx')

var RuleBar = React.createClass({
  propTypes: {
    rules: React.PropTypes.arrayOf( React.PropTypes.shape({
      expansion: React.PropTypes.string,
      app_rate: React.PropTypes.number
      })
    ).isRequired
  },

  render:function() {
    var rules = []
    this.props.rules.forEach(function(rule, i){
      rules.push(<rule {...rule} key={i}/>);
      },this)
    return(
          <div>
            {rules}
          </div>
      );
  }
});


module.exports = RuleBar;
