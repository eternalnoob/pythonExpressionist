{/* This will be responsible for rendering the main data interface board when it is displaying a rule*/}

var React = require('react')
var Button = require('react-bootstrap').Button
var Glyphicon = require('react-bootstrap').Glyphicon
var Panel = require('react-bootstrap').Panel

var RuleBoard = React.createClass({
  PropTypes: {
  name: React.PropTypes.string,
  expansion: React.PropTypes.string,
  app_rate: React.PropTypes.number,
  onChangeRule: React.PropTypes.func,
  onDeleteRule: React.PropTypes.func
  },
  
  render: function() {
    
    console.log(this.props.expansion)

    return(
    <div>
      <div style={{"width": "50%", "margin": "0 auto"}}>
        <h2>{this.props.name}</h2>
      </div>

      <div>
      <h3>{this.props.name} -> {this.props.expansion}</h3><Button bsStyle="danger" title="Delete Rule" onClick={this.props.onDeleteRule}><Glyphicon glyph="warning-sign"/>Delete</Button>
      </div>

      <h2>{this.props.app_rate}<Button bsStyle="default" title="Modify Application Rate" onClick={this.props.onAppChange}><Glyphicon glyph="console"/></Button></h2>

    </div>
    )

  }
});

module.exports = RuleBoard
