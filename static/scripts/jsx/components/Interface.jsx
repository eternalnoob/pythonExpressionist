{/*This is the top level component which will attach to document.body*/}

var React = require('react')
var NonterminalList = require('./NonterminalList.jsx')

{/*
        <HeaderBar/>
        <MarkupList present = {this.state.nonterminals[current_nonterminal].markup} total={this.state.markups}/>
        <Board rule={this.state.current_rule} nonterminal={this.state.current_rule}/>
        <RuleList {...this.state.nonterminals[current_nonterminal].rules}/>
        <Feedback expansion = {this.state.expansion_feedback} markup_feedback = {this.state.markup_feedback} />
*/}
var Interface = React.createClass({
  getInitialState: function() {
    return{
      nonterminals: [
      {name: "TEST_NONTERMINAL", deep: false, complete: true, rules: [{expansion: "testExpand", app_rate:5},{expansion:"test1", app_rate:3}], markup: ["test","test2"]},
      {name: "Second_nonterminal", deep:true, complete: false, rules: [{expansion:"firstExpand", app_rate:5}], markup: ["set1:act1","set2:act2"]},
      {name: "COMPLETE DEEP REP", deep: true, complete: true, rules: [], markup: []}
      ],
      markups: ["test","test2","set1:act1","set2:act2"],
      expansion_feedback: "",
      markup_feedback: "",
      current_nonterminal: -1,
      current_rule: -1
    }
  },

  handleNonterminalClick: function(position) {
    if (this.state.nonterminals[position])
    {
      console.log("you clicked nonterminal " + this.state.nonterminals[position].name)
      this.setState({current_nonterminal: position})
      this.setState({current_rule: -1})
    }
  },

  handleNonterminalAdd: function(name) {
    
    console.log("You are Adding a nonterminal with name: " + name)
    var duplicate = 0
    var arr_length = this.state.nonterminals.length
    for ( var i = 0; i < arr_length; i++) {
      if (this.state.nonterminals[i].name == name){
      duplicate = 1
      }
    }
    if(duplicate == 0)
    {
      this.setState({nonterminals: this.state.nonterminals.concat( [{name: name, rules:[], markup:[], deep:false, complete:false}])} );
    }
    else
    {
      console.log("Duplicate Nonterminal!")
    }
  },
    

  render: function() {
    return(
    <div>
      <h1>THIS IS A TEST</h1>
        <NonterminalList nonterminals={this.state.nonterminals} onAddNonterminal={this.handleNonterminalAdd} onClickNonterminal={this.handleNonterminalClick}>Test</NonterminalList>
    </div>
    );
  }
});

module.exports = Interface
