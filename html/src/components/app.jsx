import React from 'react';
import NavBar from './navbar.jsx';
import Main from './main.jsx';

import {Button, Glyphicon} from 'react-bootstrap';

export default class App extends React.Component {
  
  render(){
    return <div className="app-element">
      <NavBar />
      <div className="container">
        {this.props.children}
      </div>
    </div>
  } 
}