{/* This will contain the operations which can be used on the grammar at any time, import, load, save, export. This is nested directly within the main interface*/}
var React = require('react')
var ButtonGroup = require('react-bootstrap').ButtonGroup
var Button = require('react-bootstrap').Button
var ButtonToolbar = require('react-bootstrap').ButtonToolbar

var HeaderBar = React.createClass({

  render: function()
  {
    return(
    <ButtonToolbar>
      <ButtonGroup>
        <Button bsStyle='primary'>Import</Button>
        <Button bsStyle='primary'>Load</Button>
        <Button bsStyle='primary'>Save</Button>
        <Button bsStyle='primary'>Export</Button>
        <Button bsStyle='primary'>Show System Vars</Button>
      </ButtonGroup>
    </ButtonToolbar>
    );
  }

})
module.exports = HeaderBar
