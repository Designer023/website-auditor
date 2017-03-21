import React, { Component } from 'react';

var moment = require('moment');

import SessionForm from './SessionForm';
import SessionTable from './SessionTable';

class Sessions extends Component {

    constructor(props) {
        super(props);
    }

    render() {

        return (
            <div className="container">
                <div className="jumbotron">
                  <h1 className="display-3">Sessions</h1>
                  <hr className="my-4" />
                </div>

                <SessionForm />

                <SessionTable />
            </div>
        )
    }
}


export default Sessions;