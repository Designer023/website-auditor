import React, { Component } from 'react';
import $ from 'jquery';

import { Link } from 'react-router'

class Sessions extends Component {

    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            sessions: []
        }

        this.getData = this.getData.bind(this);
    }

    componentDidMount() {
        this.getData();
    }


    getData() {
        // if (this.state.loading === false) {

            this.setState(
                function(prevState, props){
                    return {
                        loading: true
                    }
                }
            );

            let queue_end_point = '/api/v1.0/auditor/sessions';

            $.ajax({
                type: 'GET',
                url: queue_end_point,
                success: function (data) {

                    this.setState(
                        function (prevState, props) {
                            return {
                                loading: false,
                                sessions: data.sessions
                            }
                        })
                }.bind(this)
            });
        // }
    }

    render() {

        let sessions = this.state.sessions.map(function(session){
            return (
                <tr key={session.uuid}>
                    <td><Link to={"/session/" + session.uuid } >{session.url}</Link></td>
                    <td>{session.uuid}</td>
                    <td>{session.pages}</td>
                    <td>{session.queue}</td>
                    <td>{session.percent}%</td>
                </tr>
            )
        });

        if (this.state.loading === true) {
            return (
                <div>Loading data...</div>
            )
        } else {
            return (
                <div className="container">
                    <div className="jumbotron">
                          <h1 className="display-3">Sessions</h1>
                          <hr className="my-4" />


                    </div>
                    <div className="card mt-5">
                        <div className="card-block">



                             <table className="table table-striped">
                            <thead className="thead-inverse">
                                <tr>
                                    <th>
                                        URL
                                    </th>
                                    <th>
                                        Session
                                    </th>

                                    <th>
                                        Pages
                                    </th>

                                    <th>
                                        Queue
                                    </th>

                                    <th>
                                        Completion %
                                    </th>
                                </tr>
                            </thead>

                            <tbody>

                                {sessions}

                            </tbody>
                        </table>
                        </div>
                     </div>
                </div>
            )
        }

    }
}


export default Sessions;