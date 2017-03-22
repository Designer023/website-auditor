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
                <SessionForm />

                <SessionTable />
            </div>
        )
    }
}


export default Sessions;