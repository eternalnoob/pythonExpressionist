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
    var present = Object.keys(this.props.present)
    //for loop iterates over the array which holds all markups
    for( var outer = 0; total.length > outer ; outer++)
    {
      //return the current markup_set
      var curr_set = this.props.total[total[outer]]
      //check if the current markup_set is present in the nonterminal
      var curr_set_name = this.props.total[total[outer]].set
      var present_in = -1
      var nonterminal_set_length = present.length
      //iterate over markups in nonterminal to find if the set is present in it
      for( var check_nt_counter = 0; nonterminal_set_length > check_nt_counter; check_nt_counter++)
      {
        if (this.props.present[present[check_nt_counter]].set == curr_set_name)
        {
          present_in = check_nt_counter
          console.log("we Found it!")
        }

        if(present_in != -1)
        {
          break
        }
    
      }


      var set_present_in_nt =[]
      if(present_in >= 0)
      {
        set_present_in_nt = this.props.present[present[present_in]]
      }

      console.log(curr_set)

      output.push(<MarkupSet onClickMarkup = {this.props.onClickMarkup}  onAddMarkup = {this.props.onAddMarkup} key={total[outer]} name={total[outer]} present_nt={set_present_in_nt} current_set={curr_set}/>)
    }



    return(
    <ButtonGroup>
      {output}
      <Button onClick = {this.props.onAddMarkupSet} key="addnew"><Glyphicon glyph="plus"/></Button>
    </ButtonGroup>
    )
    }
});

module.exports = MarkupBar

