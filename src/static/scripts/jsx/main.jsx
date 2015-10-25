var React = require('react')
var ReactDOM = require('react-dom')
var ButtonGroup = require('react-bootstrap').ButtonGroup
var ListGroup = require('react-bootstrap').ListGroup
var Button = require('react-bootstrap').Button
var ListGroupItem = require('react-bootstrap').ListGroupItem
var Panel = require('react-bootstrap').Panel

var MarkupClass = React.createClass({
  getInitialState: function(){
    return{present: this.props.initialPresent};
  },

  render:function(){
  }
});

var Markup = React.createClass({
  getInitialState: function(){
    return{present: this.props.initialPresent};
  },

  render: function(){
    return<button name={this.props.markup_name} bsize="large" onClick={this.handleClick}/>
  },

  handleClick: function(){
    this.setState({present: !this.state.present});
    console.log("I fucking despise this")

  }
});
const wellStyles = {maxWidth: 400, margin: '0 auto 10px'};

const buttonsInstance = (
  <div className="well" style={wellStyles}>
  <Button bsStyle="primary" bsSize="large" block>Block level button</Button>
  <Button bsSize="large" block>Block level button</Button>
  </div>
);

ReactDOM.render(buttonsInstance, document.getElementById('example'));


const listStyles = {maxWidth: 200, margin: '0', overflowY: scroll};
var NonterminalList = React.createClass({
  render: function() {
    console.log(this.props)
    return (
        <ListGroup style={listStyles}>
          <ListGroupItem bsSize="small" bsStyle="success" href='#'>Link1</ListGroupItem>
          <ListGroupItem bsSize="small" bsStyle="success" href='#'>Link2</ListGroupItem>
          <ListGroupItem bsSize="small" bsStyle="success" href='#'>Link1</ListGroupItem>
          <ListGroupItem bsSize="small" bsStyle="success" href='#'>Link1</ListGroupItem>
          <ListGroupItem bsSize="small" bsStyle="success" href='#'>Link1</ListGroupItem>
          <ListGroupItem bsSize="small" bsStyle="success" href='#'>Link1</ListGroupItem>
          <ListGroupItem bsSize="small" bsStyle="success" href='#'>Link1</ListGroupItem>
          <ListGroupItem bsSize="small" bsStyle="success" href='#'>Link2</ListGroupItem>
          <ListGroupItem bsSize="small" bsStyle="success" href='#'>Link2</ListGroupItem>
          <ListGroupItem bsSize="small" bsStyle="success" href='#'>Link2</ListGroupItem>
          <ListGroupItem bsSize="small" bsStyle="success" href='#'>Link2</ListGroupItem>
          <ListGroupItem bsSize="small" bsStyle="success" href='#'>Link2</ListGroupItem>
          <ListGroupItem bsSize="small" bsStyle='danger'>Link3</ListGroupItem>
          <ListGroupItem bsSize="small" bsStyle='danger'>Link4</ListGroupItem>
        </ListGroup>
    );
  }
});

ReactDOM.render(<NonterminalList/>, document.getElementById('nonterminal_list'));

