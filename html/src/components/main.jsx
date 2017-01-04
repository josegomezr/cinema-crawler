import React from 'react';

import _ from 'lodash';
import {Link} from 'react-router';

import $ from 'jquery';

export default class Main extends React.Component {
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
    let movies = _(this.state.data.movies).map((movie) => {
      return movie;
    }).sortBy('name').map( (movie) => {
      return <Link to={`/movie/${movie.id}`} className="list-group-item" key={movie.id}>
        {movie.name}
      </Link>
    }).value();

    return <div>
      <h1>Cartelera</h1>
      <div className="list-group" id="main-movie-list">
        {movies}
      </div>
    </div>
  }
}