import React, { Component } from 'react';


import Results from './Results';

class Dashboard extends Component {

    render() {

        return (
            <div className="container-fluid">
                 <div>
                     <Results />
                </div>
            </div>
        )

    }
}



export default Dashboard;