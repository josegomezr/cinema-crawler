import React from 'react';
import $ from 'jquery';
import _ from 'lodash';
import {Link} from 'react-router';
import {Nav, NavItem, MenuItem, NavDropdown, Navbar} from 'react-bootstrap';

import {LinkContainer} from 'react-router-bootstrap';

export default class NavBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: {
        movies: {},
        theaters: {},
        chains: {}
      }
    }
  }
  componentDidMount() {
    $.getJSON(window._url_json).then( (json) => {
      this.setState({
        data: json
      })
    })   
  }

  render(){

    let menuItems = _.map(this.state.data.chains, (chain) => {
      return <LinkContainer key={chain.id} to={`/chain/${chain.id}`}>
        <MenuItem>{chain.name}</MenuItem>
      </LinkContainer>
    })

    return <div className="navbar-element">
      <Navbar inverse collapseOnSelect staticTop>
        <Navbar.Header>
          <Navbar.Brand>
            <a href="#">Cartelera</a>
          </Navbar.Brand>
          <Navbar.Toggle />
        </Navbar.Header>
        <Navbar.Collapse>
          <Nav>
            <NavDropdown eventKey={3} title="Cadenas" id="basic-nav-dropdown">
              {menuItems}
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    </div>
  }
}
