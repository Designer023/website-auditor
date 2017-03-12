import React, { Component } from 'react';


import Results from './Results';

class Dashboard extends Component {

    render() {

        return (
            <div className="container-fluid">
                 <div>

                     <input type="text" placeholder="crawl url..." />
                     <input type="submit" value="Start crawl" />

                     <Results />
                </div>
            </div>
        )

    }
}



export default Dashboard;
