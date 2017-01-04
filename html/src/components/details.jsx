import React from 'react';

import $ from 'jquery';
import _ from 'lodash';

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
    let movie = this.state.data.movies[this.props.params.movieId]

    if (!movie) {
      return <span>wait...</span>;
    }
    
    movie.chains = movie.chains.map((chainId) => {
      return this.state.data.chains[chainId]
    })
    movie.theaters = movie.theaters.map((theaterId) => {
      return this.state.data.theaters[theaterId]
    });

    let showTimeDetails = _.map(movie.showtimes, (showtime) => {
      let theater = this.state.data.theaters[showtime.theater];
      let chain = this.state.data.chains[theater.chain];

      let showtimes = showtime.showtime.map((st, i) => {
        return <span>
          {i == 0 ? '' : '-'}
          {" "}
          <strong>{st}</strong>
          {" "}
        </span>
      });


      return <tr key={movie.id+showtime.theater}>
        <td>{theater.name}</td>
        <td>{showtimes}</td>
      </tr>
    });

    return <div>
      <h1>{movie.name}</h1>
      <table className="table">
        <tr>
          <th>Sucursal</th>
          <th>Horas</th>
        </tr>
        {showTimeDetails}
      </table>
    </div>;
  }
}