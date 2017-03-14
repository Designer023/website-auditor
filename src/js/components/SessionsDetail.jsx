import React, { Component } from 'react';


import { Link } from 'react-router'

import SessionHeader from './SessionHeader';
import SessionResults from './SessionResults';

class SessionsDetail extends Component {

    render() {

        return (
            <div className="container">

                <SessionHeader session_id={this.props.params.session_id}/>

                <SessionResults session_id={this.props.params.session_id}/>

            </div>
        )
    }

}


export default SessionsDetail;