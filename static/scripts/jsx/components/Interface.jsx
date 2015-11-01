{/*This is the top level component which will attach to document.body*/}

var React = require('react')
var NonterminalList = require('./NonterminalList.jsx')
var MarkupBar = require('./MarkupBar.jsx')
var findIndex = require('lodash/array/findIndex')
var jQuery = require('jquery')
var RuleBar= require('./RuleBar.jsx')
var NonterminalBoard = require('./NonterminalBoard.jsx')
var RuleBoard = require('./RuleBoard.jsx')
var FeedbackBar = require('./FeedbackBar.jsx')
var HeaderBar = require('./HeaderBar.jsx')


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
      markup_feedback: [],
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
      console.log("you clicked nonterminal " + this.state.nonterminals[position])
      this.setState({current_nonterminal: position})
      this.setState({current_rule: -1})
    }
  },

  //this handles the addition of a nonterminal
  handleNonterminalAdd: function() {
    
    console.log("add a new nonterminal")
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

  handleExpand: function()
  {
    jQuery.ajax({
      url:'/nonterminal/expand',
      dataType: 'json',
      async: true,
      cache:false,
      success: function(data) {
        this.setState({expansion_feedback: data.derivation})
        this.setState({markup_feedback: data.markup})
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
      });
  },

  handleSetDeep: function()
  {

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
  handleRuleClick: function(expansion)
  {
    console.log("we're trying it")
    console.log(expansion)
    var rules=this.state.nonterminals[this.state.current_nonterminal].rules
    var total_len = rules.length
    for( var i = 0; total_len > i; i++ )
    {
      if (rules[i].expansion == expansion)
      {
        this.setState({current_rule: i})
        console.log(i)
        break
      }
    }
  },
  handleRuleAdd: function()
  {
    //AJAX GOES HERE
    console.log("adding a rule")
  },

    
  render: function() {
    var present_markups = []
    var def_rules = []
    var board
    if( this.state.current_nonterminal != "" )
    {
      present_markups=this.state.nonterminals[this.state.current_nonterminal].markup
      def_rules = this.state.nonterminals[this.state.current_nonterminal].rules
        board = <NonterminalBoard expand = {this.handleExpand} setDeep = {this.handleSetDeep} name={this.state.current_nonterminal} nonterminal={this.state.nonterminals[this.state.current_nonterminal]} />
      if( this.state.current_rule != -1)
      {
        board =<RuleBoard expand = {this.handleExpand} name={this.state.current_nonterminal} expansion={def_rules[this.state.current_rule].expansion.join('')} 
        app_rate={def_rules[this.state.current_rule].app_rate}/>
      }

    }
        <NonterminalBoard expand = {this.handleExpand} setDeep = {this.handleSetDeep} name={this.state.current_nonterminal} nonterminal={this.state.nonterminals[this.state.current_nonterminal]} />

    return(
    <div style={{position: "fixed", top: 0, right: 0, "height": "100%", "width": "100%"}}>
      <div style= {{"width": "75%", position: "absolute", top: 0, left: 0}}>
        <HeaderBar/>
        <MarkupBar onClickMarkup={this.handleMarkupClick} onAddMarkup={this.handleMarkupAdd} onAddMarkupSet={this.handleMarkupSetAdd} present = {present_markups} total={this.state.markups}/>
        {board}
      </div>

      <div style= {{"maxWidth": "250px", "minWidth": "15%","height":"100%", position: "absolute", top: 0, right: 0}}>
          <NonterminalList nonterminals={this.state.nonterminals} onAddNonterminal={this.handleNonterminalAdd} onClickNonterminal={this.handleNonterminalClick}>Test</NonterminalList>
      </div>

      <div style= {{"width": "75%", "height": "25%", position: "absolute", bottom: 0, left:0}}>
        <RuleBar rules={def_rules} onRuleAdd = {this.handleRuleAdd} onRuleClick={this.handleRuleClick} name={this.state.current_nonterminal}/>
        <FeedbackBar derivation={this.state.expansion_feedback} markup={this.state.markup_feedback}/>
      </div>


    </div>
    );
  }
});

module.exports = Interface
