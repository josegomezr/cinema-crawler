import React from 'react';
import NavBar from './navbar.jsx';
import Main from './main.jsx';

import {Button, Glyphicon} from 'react-bootstrap';

export default class App extends React.Component {
  
  render(){
    
    return <div>
      <NavBar />
      <div className="container">
      {/*}
        <div className="pull-right">
          <Button>
            <Glyphicon glyph="search" />
            Buscar
          </Button>
        </div>
        <div className="clearfix"></div>
        <br />
      {*/}
        {this.props.children}
      </div>
    </div>
  } 
}