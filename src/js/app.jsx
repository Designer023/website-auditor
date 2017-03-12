import React, { Component } from 'react';
import ReactDOM from 'react-dom';

import { Router, Route, browserHistory } from 'react-router'

import Dashboard from './components/Dashboard';
import Sessions from './components/Sessions';
import SessionsDetail from './components/SessionsDetail';
import Page from './components/Page';
import PageErrors from './components/PageErrors';
import PageHeaders from './components/PageHeaders';
import PageMetaTags from './components/PageMetaTags';
import PagePerformance from './components/PagePerformance';

// Let the window know there is a React element on the page
// This means the react dev tools will work
if (typeof window !== 'undefined') {
    window.React = React;
}

ReactDOM.render((
     <Router history={browserHistory}>
        <Route path="/" component={Sessions}/>
         <Route path="/session/" component={Sessions}/>
         <Route path="/session/:session_id" component={SessionsDetail}/>
         <Route path="/page/:page_id" component={Page} >
             <Route path="/page/:page_id/errors" component={PageErrors}/>
             <Route path="/page/:page_id/headers" component={PageHeaders}/>
             <Route path="/page/:page_id/meta" component={PageMetaTags}/>
             <Route path="/page/:page_id/performance" component={PagePerformance}/>
         </Route>
      </Router>
    ),
    document.getElementById('app')
);


