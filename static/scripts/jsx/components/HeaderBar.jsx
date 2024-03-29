{/* This will contain the operations which can be used on the grammar at any time, import, load, save, export. This is nested directly within the main interface*/
}
var ReactDOM = require('react-dom')
var React = require('react')
var ButtonGroup = require('react-bootstrap').ButtonGroup
var Button = require('react-bootstrap').Button
var ButtonToolbar = require('react-bootstrap').ButtonToolbar
var Modal = require('react-bootstrap').Modal
var DropzoneComponent = require('react-dropzone-component')

/*<Button onClick={this.props.saveGrammar} bsStyle='primary'>Save</Button>*/
var HeaderBar = React.createClass({
    getInitialState() {
        return {showModal: false, showfileModal: false};
        
    },

    close() {
        this.setState({showModal: false});
    },

    open() {
        this.setState({showModal: true});
    },
    
    closemodal(){
        this.setState({showfileModal: false});
    },

    openmodal(){
        this.setState({showfileModal: true});
        console.log("whyyy")
    },






    render: function () {
        var componentconfig= {postUrl: 'api/grammar/upload_grammar', showFiletypeIcon: true, iconFileTypes: ['.json']}
        return (
            <div>
                <ButtonToolbar>
                    <ButtonGroup>
                        <Button onClick={this.props.loadGrammar} bsStyle='primary'>Load Existing</Button>
                        <Button onClick={this.props.renameGrammar} bsStyle='primary'>Rename Grammar</Button>
                        <Button onClick={this.props.saveGrammar} bsStyle='primary'>Save Grammar</Button>
                        <Button onClick={this.openmodal} bsStyle='primary'>Upload A Grammar</Button>
                        <Button onClick={this.open} bsStyle='primary'>Show System Vars</Button>
                        <Button onClick={this.props.reset} bsStyle='danger'>Start Over</Button>
                    </ButtonGroup>
                </ButtonToolbar>
                <Modal show={this.state.showModal} onHide={this.close}>
                    <Modal.Header closeButton>
                        <Modal.Title>Defined System Variables</Modal.Title>
                    </Modal.Header>
                </Modal>
                <Modal show={this.state.showfileModal} onHide={this.closemodal}>
                    <Modal.Header closeButton>
                        <Modal.Title>Upload A Grammar</Modal.Title>
                    </Modal.Header>
                    {<DropzoneComponent ref="test"
                                        config={componentconfig}/>}
                </Modal>
            </div>
        );
    }

})
module.exports = HeaderBar
