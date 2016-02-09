{/*This is the top level component which will attach to document.body*/
}

var React = require('react')
var NonterminalList = require('./NonterminalList.jsx')
var MarkupBar = require('./MarkupBar.jsx')
var findIndex = require('lodash/array/findIndex')
var ajax = require('jquery').ajax
var RuleBar = require('./RuleBar.jsx')
var NonterminalBoard = require('./NonterminalBoard.jsx')
var RuleBoard = require('./RuleBoard.jsx')
var FeedbackBar = require('./FeedbackBar.jsx')
var HeaderBar = require('./HeaderBar.jsx')


var Interface = React.createClass({

    //load data from server, use default grammar
    getInitialState: function () {
        console.log("test")
        var a
        ajax({
            url: '/default',
            dataType: 'json',
            async: false,
            cache: false,
            success: function (data) {
                a = data
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
        var b = a['nonterminals']
        var c = a['markups']
        var d = a['system_vars']
        return {
            nonterminals: b,
            markups: c,
            system_vars: d,
            expansion_feedback: "",
            markup_feedback: [],
            current_nonterminal: "",
            current_rule: -1
        }
    },

    //update state from server
    updateFromServer: function () {
        var a
        ajax({
            url: '/default',
            dataType: 'json',
            async: false,
            cache: false,
            success: function (data) {
                a = data
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
        var b = a['nonterminals']
        var c = a['markups']
        var d = a['system_vars']
        this.setState({nonterminals: b})
        this.setState({markups: c})
        this.setState({system_vars: d})

    },

    //this handles the context switching (what nonterminal are we on)
    handleNonterminalClick: function (position) {
        if (this.state.nonterminals[position]) {
            console.log("you clicked nonterminal " + this.state.nonterminals[position])
            this.setState({current_nonterminal: position})
            this.setState({current_rule: -1})
        }
    },

    //this handles the addition of a nonterminal
    handleNonterminalAdd: function () {

        console.log("add a new nonterminal")
        var nonterminal = window.prompt("Please enter Nonterminal Name")
        if (nonterminal != "") {
            console.log(nonterminal)
            if (this.state.nonterminals[nonterminal]) {
                console.log("duplicate nonterminal!")
            }
            else {
                var object = {
                    "nonterminal": nonterminal
                }
                console.log(object)
                ajax({
                    url: '/nonterminal/add',
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify(object),
                    async: false,
                    cache: false
                })
                this.updateFromServer()
            }
        }
    },

    //these handle clicking markup to add it to a nonterminal
    handleMarkupClick: function (set, tag) {
        console.log("you are clicking " + set + ":" + tag)
        if (this.state.current_nonterminal != "") {
            var object = {
                "nonterminal": this.state.current_nonterminal,
                "markupSet": set,
                "tag": tag
            }
            console.log(object)
            ajax({
                url: '/markup/toggle',
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(object),
                async: false,
                cache: false
            })
            this.updateFromServer()
        }
    },

    resetGrammar: function () {

        ajax({
            url: '/grammar/new',
            type: 'GET',
            async: false,
            cache: false
        });
        this.state.current_nonterminal = ""
        this.state.current_rule = -1
        this.updateFromServer()
    },

    handleExpand: function () {
        ajax({
            url: '/nonterminal/expand',
            type: 'POST',
            contentType: "application/json",
            data: JSON.stringify({"nonterminal": this.state.current_nonterminal}),
            dataType: 'json',
            async: true,
            cache: false,
            success: function (data) {
                this.setState({expansion_feedback: data.derivation})
                this.setState({markup_feedback: data.markup})
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },

    handleSetDeep: function (nonterminal) {
        if (this.state.current_nonterminal != "") {
            var object = {
                "nonterminal": this.state.current_nonterminal,
            }
            console.log(object)
            ajax({
                url: '/nonterminal/deep',
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(object),
                async: false,
                cache: false
            })
            this.updateFromServer()
        }
    },

    handleMarkupSetAdd: function () {
        console.log("You are adding a MarkupSet!")
        var markupTag = window.prompt("Please enter MarkupSet")
        if (markupTag != "") {
            var object = {"markupSet": markupTag}
            console.log(object)
            ajax({
                url: '/markup/addtagset',
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(object),
                async: false,
                cache: false
            })
            this.updateFromServer()
        }
    },

    handleMarkupAdd: function (set) {
        console.log("You are adding a single markup to set " + set)
        var markupTag = window.prompt("Please enter Markup Tag")
        if (markupTag != "") {
            //ensure tag does not exist in tagset
            if (this.state.markups[set].indexOf(markupTag) === -1) {
                var object = {
                    "markupSet": set,
                    "tag": markupTag
                }
                console.log(object)
                ajax({
                    url: '/markup/addtag',
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify(object),
                    async: false,
                    cache: false
                })
                this.updateFromServer()
            }
        }
    },

    handleRuleClick: function (expansion) {
        console.log(expansion)
        var rules = this.state.nonterminals[this.state.current_nonterminal].rules
        var total_len = rules.length
        for (var i = 0; total_len > i; i++) {
            if (rules[i].expansion == expansion) {
                this.setState({current_rule: i})
                console.log(i)
                break;
            }
        }
    },
    handleRuleAdd: function () {
        //AJAX GOES HERE
        console.log("add a new Rule")
        var expansion = window.prompt("Please enter Rule expansion")
        var app_rate = window.prompt("please enter application_rate")
        if (expansion != "" && !isNaN(app_rate)) {
            var object = {
                "rule": expansion,
                "app_rate": app_rate,
                "nonterminal": this.state.current_nonterminal
            }
            console.log(object)
            ajax({
                url: '/rule/add',
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(object),
                async: false,
                cache: false
            })
            console.log("adding a rule")
            this.updateFromServer()
        }
    },

    onRuleDelete: function (index) {
        var object = {
            "rule": this.state.current_rule,
            "nonterminal": this.state.current_nonterminal
        }
        console.log(object)
        ajax({
            url: '/rule/delete',
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(object),
            async: false,
            cache: false
        })
        //forceUpdate()
        this.state.current_rule -= 1
        this.updateFromServer()
    },

    handleAppModify: function () {
        var index = this.state.current_rule
        console.log("modifying application rate")
        var app_rate = window.prompt("Please enter new application rate")
        if (!isNaN(app_rate)) {
            var object = {"rule": index, "nonterminal": this.state.current_nonterminal, "app_rate": app_rate}
            console.log(object)
            ajax({
                url: '/rule/set_app',
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(object),
                async: false,
                cache: false
            })
            this.updateFromServer()
        }
    },

    importReps: function () {

    },

    loadGrammar: function () {
        var filename = window.prompt("Enter the Name of the Grammar you wish to load")
        if (filename != "") {
            ajax({
                url: 'grammar/from_file',
                type: "POST",
                contentType: "text/plain",
                data: filename,
                async: false,
                cache: false
            })
            this.updateFromServer()
        }


    },

    saveGrammar: function () {

        var filename = window.prompt("Enter the Name of file you wish to Save Grammar to")
        if (filename != "") {
            ajax({
                url: 'grammar/save',
                type: "POST",
                contentType: "text/plain",
                data: filename,
                async: true,
                cache: false
            })
        }
    },

    exportList: function () {
        var filename = window.prompt("Enter the Name of file you wish to export to")
        if (filename != "") {
            ajax({
                url: 'grammar/export',
                type: "POST",
                contentType: "text/plain",
                data: filename,
                async: true,
                cache: false
            })
        }
    },

    render: function () {
        var present_markups = []
        var def_rules = []
        var board
        if (this.state.current_nonterminal != "") {
            present_markups = this.state.nonterminals[this.state.current_nonterminal].markup
            def_rules = this.state.nonterminals[this.state.current_nonterminal].rules
            //check which board we need to render
            board = <NonterminalBoard expand={this.handleExpand} setDeep={this.handleSetDeep}
                                      name={this.state.current_nonterminal}
                                      nonterminal={this.state.nonterminals[this.state.current_nonterminal]}/>
            if (this.state.current_rule != -1) {
                board = <RuleBoard expand={this.handleExpand} name={this.state.current_nonterminal}
                                   onAppChange={this.handleAppModify}
                                   expansion={def_rules[this.state.current_rule].expansion.join('')}
                                   app_rate={def_rules[this.state.current_rule].app_rate}
                                   onDeleteRule={this.onRuleDelete} onChangeRule={this.onRuleChange}/>
            }
        }

        return (
            <div style={{position: "fixed", top: 0, right: 0, "height": "100%", "width": "100%"}}>
                <div
                    style={{ "height": "75%", "width": "75%", position: "absolute", top: 0, left: 0}}>
                    <HeaderBar reset={this.resetGrammar} loadGrammar={this.loadGrammar}
                               exportList={this.exportList} saveGrammar={this.saveGrammar}
                               systemVars={this.state.system_vars}/>
                    <div className="muwrap">
                        <div className="show-y-wrapper">
                            <MarkupBar className="markup-bar" onClickMarkup={this.handleMarkupClick}
                                       onAddMarkup={this.handleMarkupAdd}
                                       onAddMarkupSet={this.handleMarkupSetAdd} present={present_markups}
                                       total={this.state.markups}/>
                        </div>
                    </div>
                    {board}
                </div>

                <div
                    style={{"overflow": "auto", "width": "25%", "height":"100%", position: "absolute", top: 0, right: 0}}>
                    <NonterminalList nonterminals={this.state.nonterminals} onAddNonterminal={this.handleNonterminalAdd}
                                     onClickNonterminal={this.handleNonterminalClick}>Test</NonterminalList>
                </div>

                <div style={{"width": "75%", "height": "25%", position: "absolute", bottom: 0, left:0}}>
                    <div className="muwrap">
                        <RuleBar rules={def_rules} onRuleAdd={this.handleRuleAdd} onRuleClick={this.handleRuleClick}
                                 name={this.state.current_nonterminal}/>
                    </div>
                    <FeedbackBar derivation={this.state.expansion_feedback} markup={this.state.markup_feedback}/>
                </div>


            </div>
        );
    }
});

module.exports = Interface
