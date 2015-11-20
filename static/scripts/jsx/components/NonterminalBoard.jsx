var React = require('react')
var Button = require('react-bootstrap').Button
var Glyphicon = require('react-bootstrap').Glyphicon
var Panel = require('react-bootstrap').Panel

var NonterminalBoard = React.createClass({
  PropTypes: {
    name: React.PropTypes.string,
    nonterminal: React.PropTypes.object,
    expand: React.PropTypes.func,
    setDeep: React.PropTypes.func
  },
  
  render: function() {
    
    var expand
    var rules
    var markup
    var glyph_nt
    if( this.props.nonterminal )
    {
      var name = this.props.name
      var deep_str = ""
      if ( this.props.nonterminal && this.props.nonterminal.deep )
      {
        deep_str = name +" is a deep representation"
        glyph_nt=<Glyphicon glyph="asterisk"/>
      }
      else
      {
        deep_str = name +" is NOT a deep representation"
        glyph_nt=<Glyphicon glyph="remove"/>
      }

      if( name != "" )
      {
        expand = <h1><Button bsStyle={this.props.nonterminal.deep ? "success" : "danger" } onClick={this.props.setDeep} title={deep_str}>{glyph_nt}</Button>
        {name}<Button onClick={this.props.expand} title="Expand This"><Glyphicon glyph="resize-full"/></Button></h1>

      }

      rules = this.props.nonterminal.rules

      markup = this.props.nonterminal.markup
    }

    return(
    <div>
      <div style={{"width": "50%", "margin": "0 auto"}}>
        {expand}
      </div>

      <div>


      </div>

    </div>
    )

  }


});

module.exports = NonterminalBoard
