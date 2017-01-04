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

    let showTimeDetails = _.map(movie.showtimes, (theaterShowtime, chainId) => {
      let chain = this.state.data.chains[chainId];

      let rows = _.map(theaterShowtime, (showtime, theaterId) => {
        let theater = this.state.data.theaters[theaterId];
        
        let showtimes = showtime.showtime.join(' - ');

        return <tr key={movie.id+showtime.theater}>
          <td>{theater.name}</td>
          <td>{showtimes}</td>
        </tr>
      });

      return <div key={chain.id}>
        <h3>{chain.name}</h3>
        <table className="table movie-details-element-table">
          <thead>
            <tr>
              <th>Sucursal</th>
              <th>Horas</th>
            </tr>
          </thead>
          <tbody>
            {rows}
        </tbody>
        </table>  
      </div>
    });

    return <div className="movie-details-element">
      <h1>{movie.name}</h1>
      {showTimeDetails}
    </div>;
  }
}