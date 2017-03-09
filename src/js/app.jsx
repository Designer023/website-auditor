import React, { Component } from 'react';
import ReactDOM from 'react-dom';

import { Router, Route, hashHistory } from 'react-router'

import Dashboard from './components/Dashboard';
import SessionDetailDash from './components/SessionDetailDash';

// Let the window know there is a React element on the page
// This means the react dev tools will work
if (typeof window !== 'undefined') {
    window.React = React;
}

ReactDOM.render((
     <Router history={hashHistory}>
        <Route path="/" component={Dashboard}/>
        <Route path="/session/:session_id" component={SessionDetailDash}/>
      </Router>
    ),
    document.getElementById('app')
);

