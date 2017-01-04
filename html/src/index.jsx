import React from 'react';
import {render} from 'react-dom';

import { Router, IndexRoute, Route, hashHistory } from 'react-router';

import Components from './components/index.jsx';

render((
  <Router history={hashHistory}>
    <Route path="/" component={Components.App}>
      <IndexRoute component={Components.Main} />
      <Route path="details/:movieId" component={Components.Details} />
    </Route>
  </Router>
), document.getElementById("app"))
