import React from "react";
import ReactDOM from "react-dom";
var Nonterminal = require('./components/Nonterminal.jsx')
var Rule = require('./components/Rule.jsx')


{/*
var Markup = React.createClass({
  getInitialState: function(){
    return{present: this.props.initialPresent};
  },

  render: function(){
    return<Button name={this.props.markup_name} bsize="large" onClick={this.handleClick}/>
  },

  handleClick: function(){
    this.setState({present: !this.state.present});

  }
});


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
      <ListGroupItem bsSize="small" bsStyle="danger" href='#'>Link3</ListGroupItem>
      <ListGroupItem bsSize="small" bsStyle='danger' href='#'>Link4</ListGroupItem>
      </ListGroup>
    );
  }
});
*/}

{/*

var MarkupList = React.createClass({
  getInitialState: function(i){
    
  handleClick: function(i) {
    console.log('You clicked: ' + this.props.markups[i].name + this.props.markups[i].present);
  },


  render: function() {
    return (
      <div>
      {this.props.markups.map(function(item, i) {
        return (
          <button onClick={this.handleClick.bind(this, i)} key={i}> {item.name}</button>
        );
      }, this)}
      </div>
    );
  }
});

var Markup = React.createClass({

  render: function() {
    return (
      <button button = {this.props.color} onClick={this.props.onClick}>{this.props.text}</button>
    );
  }

});


*/}


const nonterminal = {name: "TEST_NONTERMINAL", rules: [{expansion: "testExpand", app_rate:5},{expansion:"test1", app_rate:3}], markup: ["test","test2"]}

ReactDOM.render(
  <Nonterminal {...nonterminal}/>,
  document.getElementById('button_list'))
