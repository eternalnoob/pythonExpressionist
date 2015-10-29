{/*This will contain the list of nonterminals as nested components,
  as well as a add button to add a new Nonterminal at the bottom of the bar
  This has props of an array of Nonterminals And an Array of Markups representing
  Markups defined in the Grammar.*/}

  var React = require('react')
  var Nonterminal = require('./Nonterminal.jsx')
  var ListGroup = require('react-bootstrap').ListGroup
  var ListGroupItem = require('react-bootstrap').ListGroupItem
  var Input = require('react-bootstrap').Input


  var NonterminalList = React.createClass({
    PropTypes: {
      nonterminals: React.PropTypes.arrayOf(React.PropTypes.shape({
        name:  React.PropTypes.string,
        rules: React.PropTypes.array,
        markup: React.PropTypes.array,
        complete: React.PropTypes.bool,
        deep: React.PropTypes.bool
      })),
      onAddNonterminal: React.PropTypes.func,
      onClickNonterminal: React.PropTypes.func
    },
    getDefaultProps: function() {
      return{
        nonterminals: []
      };
    },


    handleClick: function(i) {
      console.log("you clicked " + this.props.nonterminals[i].name +" from NonterminalList! at number " + i);
      this.props.onClickNonterminal
    },

    handleAdd: function(name) {
      console.log("you clicked add" + name +" from NonterminalList!");
      this.props.onAddTerminal
    },

    render: function() {
      const ExampleInput = React.createClass({
        getInitialState() {
          return {
            value: ''
          };
        },
        handleChange() {
          this.setState({
            value: this.refs.value
          });
        },
        render() {
          return (
            <Input
            type="text"
            value={this.state.value}
            placeholder="Enter text"
            label="Working example with validation"
            help="Validation is based on string length."
            bsStyle={this.validationState()}
            hasFeedback
            ref="input"
            groupClassName="group-class"
            labelClassName="label-class"
            className="list-group-item"
            onChange={this.handleChange} />
          );
        }
      });

      var incomplete = []
      var complete = []
      var deep_inc = []
      var deep_comp = []

      var arr_length = this.props.nonterminals.length

      {/*forgive me for I have sinned*/}
      for ( var i = 0; i < arr_length; i++ )
      {
        var current = this.props.nonterminals[i]
        if(this.props.nonterminals[i].complete == false)
        {
          if(current.deep == true)
          {
            deep_inc.push(<Nonterminal {...current} onClick={this.props.onClickNonterminal.bind(this, i)} key={current.name}>{current.name}</Nonterminal>);
          }
          else
          {
          incomplete.push(<Nonterminal {...current} onClick={this.props.onClickNonterminal.bind(this, i)} key={current.name}>{current.name}</Nonterminal>);
          }

        }
        else
        {
          if(current.deep == true)
          {
            deep_comp.push(<Nonterminal {...current} onClick={this.props.onClickNonterminal.bind(this, i)} key={current.name}>{current.name}</Nonterminal>);
          }
          else
          {
          complete.push(<Nonterminal {...current} onClick={this.props.onClickNonterminal.bind(this, i)} key={current.name}>{current.name}</Nonterminal>);
          }
        }
      }
      var total = deep_inc.concat(incomplete.concat(deep_comp.concat(complete)))


      return(
        <ListGroup>
        {total}
        <ListGroupItem bsSize="xsmall" key ="ADDNEW" onClick={this.props.onAddNonterminal.bind(this, "test")}>Add New Nonterminal</ListGroupItem>
        </ListGroup>
      );
    }
  });

  module.exports = NonterminalList

