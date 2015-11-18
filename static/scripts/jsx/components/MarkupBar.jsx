var MarkupSet = require('./MarkupSet.jsx')
var React = require('react')
var ButtonGroup = require('react-bootstrap').ButtonGroup
var Button = require('react-bootstrap').Button
var chunk = require('lodash/array/chunk');
var Glyphicon = require('react-bootstrap').Glyphicon

var MarkupBar = React.createClass({


  render: function(){
    //emty output array
    var output = []
    var total = Object.keys(this.props.total)
    //for loop iterates over the array which holds all markups
    for( var outer = 0; total.length > outer ; outer++)
    {
      var present_nt = []
      if (this.props.present[total[outer]])
      {
        present_nt = this.props.present[total[outer]]
      }
      else
      {
        present_nt = []
      }

      output.push(<MarkupSet onClickMarkup = {this.props.onClickMarkup}  onAddMarkup = {this.props.onAddMarkup} key={total[outer]} name={total[outer]} present_nt={present_nt} current_set={this.props.total[total[outer]]}/>)
    }



    return(
    <div style = {{"overflow": "auto","height": "50%", "width": "100%"}}>
      <ButtonGroup>
        {output}
        <Button onClick = {this.props.onAddMarkupSet} key="addnew"><Glyphicon glyph="plus"/></Button>
      </ButtonGroup>
    </div>
    )
    }
});

module.exports = MarkupBar

