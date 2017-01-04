import React from 'react';

import $ from 'jquery';
import _ from 'lodash';

import {Grid, Row, Col, Clearfix} from 'react-bootstrap';
import {Link} from 'react-router';

export default class Details extends React.Component {
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
    $.getJSON('./result.json').then( (json) => {
      this.setState({
        data: json
      })
    })
  }
  
  render(){
    let chain = this.state.data.chains[this.props.params.chainId]
    if (!chain) {
      return <p>wait...</p>;
    }
    var theaters = _.filter(this.state.data.theaters, (theater) => {
      return theater.chain == chain.id
    }).map((theater) => {
      return <Col xs={12} md={4} key={theater.id} className="chain-details-element-theater-col">
        <strong>{theater.name}</strong>
        <br />
        <Link to={`/theater/${theater.id}`} className="btn btn-default">Ver Cartelera</Link>
      </Col>
    })
    
    let n_clearfixes = Math.ceil(theaters.length / 3);

    for (var i = 0; i < n_clearfixes; i++) {
      theaters.splice(i*4, 0, <Clearfix key={Math.random()} />);
    }

    return <div className="chain-details-element">
      <Row>
        <Col xs={12}>
          <h3>{chain.name}</h3>
        </Col>
      </Row>
      <Row>
        {theaters}
      </Row>
    </div>
  };
}