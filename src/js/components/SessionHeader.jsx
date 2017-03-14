import React, { Component } from 'react';

import $ from 'jquery';

import { Link } from 'react-router'


class SessionHeader extends Component {

    constructor(props) {
        super(props);
        this.state = {
            session_loading: true,
            session: []
        };

        this.getSessionData = this.getSessionData.bind(this);
    }

    componentDidMount() {
        this.getSessionData();
    }

    getSessionData() {
         this.setState(
                function(prevState, props){
                    return {
                        session_loading: true
                    }
                }
            );

            let queue_end_point = '/api/v1.0/auditor/sessions/' + this.props.session_id;

            $.ajax({
                type: 'GET',
                url: queue_end_point,
                success: function (data) {

                    this.setState(
                        function (prevState, props) {
                            return {
                                session_loading: false,
                                session: data.sessions[0]
                            }
                        })
                }.bind(this)
            });
    }

    render() {

        if (this.state.session_loading === true) {
            return (
                <div>Loading...</div>
            )
        } else {
            return (
                <div className="jumbotron">
                    <h1 className="display-3">Session details</h1>
                    <hr className="my-4" />
                    <h3>Staring url: {this.state.session.url}</h3>
                    <h4 className="lead">Session uuid: {this.state.session.uuid}</h4>
                </div>
            )
        }
    }
}



export default SessionHeader;