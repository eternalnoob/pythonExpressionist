var MarkupSet = require('./MarkupSet.jsx')
var React = require('react')
var ButtonGroup = require('react-bootstrap').ButtonGroup

var MarkupBar = React.createClass({

  propTypes: {
    present: React.PropTypes.arrayOf( React.PropTypes.shape({
      set: React.PropTypes.string,
      tags: React.PropTypes.arrayOf( React.PropTypes.string)
    }))
    ,
    total: React.PropTypes.arrayOf( React.PropTypes.shape({
      set: React.PropTypes.string,
      tags: React.PropTypes.arrayOf( React.PropTypes.string)
    }))
    },

  render: function(){
    //emty output array
    var output = []
    var total_length = this.props.total.length
    //for loop iterates over the array which holds all markups
    for( var outer = 0; total_length > outer ; outer++)
    {
      //return the current markup_set
      var curr_set = this.props.total[outer]
      //check if the current markup_set is present in the nonterminal
      var curr_set_name = this.props.total[outer].set
      var present_in = -1
      var nonterminal_set_length = this.props.present.length
      //iterate over markups in nonterminal to find if the set is present in it
      for( var check_nt_counter = 0; nonterminal_set_length > check_nt_counter; check_nt_counter++)
      {
        if (this.props.present[check_nt_counter].set == curr_set_name)
        {
          present_in = check_nt_counter
          console.log("we Found it!")
        }

        if(present_in != -1)
        {
          break
        }
    
      }


      var set_present_in_nt ={}
      if(present_in >= 0)
      {
        set_present_in_nt = this.props.present[present_in]
      }

      output.push(<MarkupSet key={curr_set.set} present_nt={set_present_in_nt} current_set={curr_set}/>)
    }

    return(
    <ButtonGroup>
    <div>
    hsade
    </div>
      {output}
    </ButtonGroup>
    )
    }
});

module.exports = MarkupBar

