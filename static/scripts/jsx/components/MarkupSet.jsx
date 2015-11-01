var React = require('react')
var DropdownButton = require('react-bootstrap').DropdownButton
var MenuItem = require('react-bootstrap').MenuItem
var Glyphicon = require('react-bootstrap').Glyphicon

var MarkupSet = React.createClass({
  
  propTypes: {
    current_set:      React.PropTypes.array,
    present_nt:      React.PropTypes.array,
    name: React.PropTypes.string,
    onClickMarkup: React.PropTypes.func,
    onAddMarkup: React.PropTypes.func
  },

  render: function() {

  var tagset_rep = this.props.name
  var out_arr = []
  var total_length = this.props.current_set.length
  var any = 0

  var successStyle = { 
    backgroundColor: "#5cb85c",
  }
  for ( var tag = 0 ; total_length > tag ; tag++ )
  {
    var current_tag = this.props.current_set[tag]
    //if the tag is present in the nonterminal
    if( this.props.present_nt.indexOf(current_tag) != -1)
    {
      out_arr.push(<MenuItem style={successStyle} key ={tag} eventKey={tag} onClick={this.props.onClickMarkup.bind(null, tagset_rep, current_tag)}
      >{current_tag}</MenuItem>)
      any = 1
    }
    else
    {
      out_arr.push(<MenuItem bsStyle = 'default' onClick={this.props.onClickMarkup.bind(null, tagset_rep, current_tag)}
      key={tag} eventKey={tag}>{current_tag}</MenuItem>)
    }

  }

  out_arr.push(<MenuItem bsStyle = 'primary' key ={total_length} eventkey={total_length} onClick = {this.props.onAddMarkup.bind(null, tagset_rep)}><Glyphicon glyph="plus"/></MenuItem>)



    return (
      <DropdownButton id={this.props.name} title={this.props.name} bsStyle={any ? 'success' : 'default'}>
        {out_arr}
      </DropdownButton>
      );
  }

});

module.exports = MarkupSet



