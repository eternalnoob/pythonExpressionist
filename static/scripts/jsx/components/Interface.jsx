{/*This is the top level component which will attach to document.body*/}

var React = require('react')
var NonterminalList = require('./NonterminalList.jsx')
var MarkupBar = require('./MarkupBar.jsx')

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

      {name: "COMPLETE DEEPREP", deep: true, complete: true, rules: [{expansion: "testExpand", app_rate:5},
      {expansion:"test1", app_rate:3}], markup: [{set:"markupset2",tags:["test2mark"]},{set:"markupset1",tags:["test4mark"]}]},

      {name: "Second_nonterminal", deep:true, complete: true, rules: [{expansion:"firstExpand", app_rate:5}],
      markup: [{set: "markupset1",tags:["test1"]},{set:"markupset2",tags:["test2mark"]}]},

      {name: "Incomplete nondeep", deep: false, complete: false, rules: [], markup: []},
      {name: "Incomplete deep", deep: true, complete: false, rules:[], markup: []}
      ],
      markups: [ {set: "markupset1", tags: ["test1","test3mark","test4mark"]} , {set: "markupset2", tags: ["test2mark"]} ],
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
    var present_markups = []
    var def_rules = []
    if( this.state.current_nonterminal != -1 )
    {
      present_markups=this.state.nonterminals[this.state.current_nonterminal].markup
      def_rules = this.state.nonterminals[this.state.current_nonterminal].rules
    }

    return(
    <div>
      <div style= {{"width": "75%", position: "fixed", top: 0, left: 0}}>
      <h1>Markupbar here</h1>
      <MarkupBar present = {present_markups} total={this.state.markups}/>
      </div>
    <div style= {{"maxWidth": "25%","height":"100%", "minWidth": "15%", position: "fixed", top: 0, right: 0}}>
        <NonterminalList style= {{"height":"100%"}}nonterminals={this.state.nonterminals} onAddNonterminal={this.handleNonterminalAdd} onClickNonterminal={this.handleNonterminalClick}>Test</NonterminalList>
    </div>
    </div>
    );
  }
});

module.exports = Interface
