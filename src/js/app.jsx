import React, { Component } from 'react';
import ReactDOM from 'react-dom';

import { Router, Route, browserHistory } from 'react-router'


import Sessions from './components/Sessions';
import SessionsDetail from './components/SessionsDetail';
import Page from './components/Page';
import PageErrors from './components/PageErrors';
import PageHeaders from './components/PageHeaders';
import PageMetaTags from './components/PageMetaTags';
import PagePerformance from './components/PagePerformance';
import PageOverview from './components/PageOverview';
import NavBar from './components/NavBar'

// Let the window know there is a React element on the page
// This means the react dev tools will work
if (typeof window !== 'undefined') {
    window.React = React;
}

ReactDOM.render((
    <div>
        <NavBar />
         <Router history={browserHistory}>
            <Route path="/" component={Sessions}/>
             <Route path="/session/" component={Sessions}/>
             <Route path="/session/:session_id" component={SessionsDetail}/>
             <Route path="/session/:session_id/page/:page_id" component={Page} >
                 <Route path="/session/:session_id/page/:page_id/overview" component={PageOverview}/>
                 <Route path="/session/:session_id/page/:page_id/errors" component={PageErrors}/>
                 <Route path="/session/:session_id/page/:page_id/headers" component={PageHeaders}/>
                 <Route path="/session/:session_id/page/:page_id/meta" component={PageMetaTags}/>
                 <Route path="/session/:session_id/page/:page_id/performance" component={PagePerformance}/>
             </Route>
          </Router>
    </div>
    ),
    document.getElementById('app')
);


