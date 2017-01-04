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
    let theater = this.state.data.theaters[this.props.params.theaterId]
    if (!theater) {
      return <p>wait...</p>;
    }
    var movies = _(this.state.data.movies).filter((movie) => {
      return movie.theaters.indexOf(theater.id) >= 0;
    }).sortBy('name').map((movie) => {
      return <Link to={`/movie/${movie.id}`} className="list-group-item" key={movie.id}>
        {movie.name}
      </Link>
    }).value();

    var movieTpl = (<p>Esta sucursal no tiene películas para hoy.</p>);

    if (movies.length > 0) {
      movieTpl = <div className="list-group" id="main-movie-list">
        {movies}
      </div>
    }

    return <Grid>
      <Row>
        <Col xs={12}>
          <h3>{theater.name}</h3>
        </Col>
      </Row>
      <Row>
        <Col xs={12}>
          {movieTpl}
        </Col>
      </Row>
        
    </Grid>
  };
}