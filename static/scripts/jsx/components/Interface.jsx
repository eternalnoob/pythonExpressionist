{/*This is the top level component which will attach to document.body*/}

var React = require('react')
var NonterminalList = require('./NonterminalList.jsx')
var MarkupBar = require('./MarkupBar.jsx')
var findIndex = require('lodash/array/findIndex')
var jQuery = require('jquery')

/*
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
*/

var Interface = React.createClass({
  getInitialState: function() {
    console.log("test")
    var a
    jQuery.ajax({
      url:'/default',
      dataType: 'json',
      async: false,
      cache:false,
      success: function(data) {
      console.log("we did it?")
      console.log(data)
        a = data
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
      });
      var b=a['nonterminals']
      var c=a['markups']
      var d=a['system_vars']
    return{
      nonterminals: b,
      markups: c,
      system_vars: d,
      expansion_feedback: "",
      markup_feedback: "",
      current_nonterminal: "",
      current_rule: -1
    }
  },

  updateFromServer: function() {
    console.log("test")
    jQuery.ajax({
      url:'/default',
      dataType: 'json',
      async: 'false',
      cache:false,
      success: function(data) {
      console.log("we did it?")
      console.log(data)
        return data
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
      });
  },

  //this handles the context switching (what nonterminal are we on)
  handleNonterminalClick: function(position) {
    if (this.state.nonterminals[position])
    {
      console.log("you clicked nonterminal " + this.state.nonterminals[position].name)
      this.setState({current_nonterminal: position})
      this.setState({current_rule: -1})
    }
  },

  //this handles the addition of a nonterminal
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
      //AJAX HERE
    }
    else
    {
      console.log("Duplicate Nonterminal!")
    }
  },

  //these handle clicking markup to add it to a nonterminal
  handleMarkupClick: function(set, tag)
  {
    console.log("you are clicking "+ set +":"+tag)
    if (this.state.current_nonterminal != -1)
    {
      //AJAX GOES HERE

      /*
        console.log("Active Nonterminal is "+ this.state.current_nonterminal)
      var current=this.state.nonterminals[this.state.current_nonterminal]
      var set_index = findIndex(current.markup, {'set': set} )
      
      if (set_index != -1)
      {
        var current_tags = current[set_index].tags
      }
      else
      { var temp_mark = {'set': set, tags:[tag]}
      }
      */

    }
  },
  
  handleMarkupSetAdd: function()
  {
    console.log("You are adding a MarkupSet!")
    //AJAX IT BOIII
  },
  handleMarkupAdd: function(set)
  {
    console.log("You are adding a single markup to set "+set)
    //AJAXAROONI
  },
    
  render: function() {
    var present_markups = []
    var def_rules = []
    if( this.state.current_nonterminal != "" )
    {
      present_markups=this.state.nonterminals[this.state.current_nonterminal].markup
      def_rules = this.state.nonterminals[this.state.current_nonterminal].rules
    }

    return(
    <div>
      <div style= {{"width": "75%", position: "fixed", top: 0, left: 0}}>
      <MarkupBar onClickMarkup={this.handleMarkupClick} onAddMarkup={this.handleMarkupAdd} onAddMarkupSet={this.handleMarkupSetAdd} present = {present_markups} total={this.state.markups}/>
      </div>
    <div style= {{"maxWidth": "25%","height":"100%", "minWidth": "15%", position: "fixed", top: 0, right: 0}}>
        <NonterminalList style= {{"height":"100%"}}nonterminals={this.state.nonterminals} onAddNonterminal={this.handleNonterminalAdd} onClickNonterminal={this.handleNonterminalClick}>Test</NonterminalList>
    </div>
    </div>
    );
  }
});

module.exports = Interface
