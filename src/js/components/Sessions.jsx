import React, { Component } from 'react';
import $ from 'jquery';

var moment = require('moment');

import { Link } from 'react-router'

class Sessions extends Component {

    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            sessions: []
        };

        this.getData = this.getData.bind(this);

        this.retest = this.retest.bind(this);
        this.delete = this.delete.bind(this)
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


    retest() {

        let retest_end_point = '/api/v1.0/auditor/sessions';

        $.ajax({
            type: 'GET',
            url: retest_end_point,
            success: function (data) {

            }.bind(this)
        });

    }

    delete(uuid) {
        let delete_end_point = '/api/v1.0/auditor/sessions/' + uuid;

        $.ajax({
            type: 'DELETE',
            url: delete_end_point,
            success: function (data) {

                //delete success
                if (data === true) {
                    this.getData()
                } else {
                    // Handle deletion error
                    alert('error deleting session: ' + uuid)
                }
            }.bind(this)
        });
    }


    render() {

        let sessions = this.state.sessions.map(function(session){
            return (
                <tr key={session.uuid}>
                    <td><Link to={"/session/" + session.uuid } >{session.url}</Link></td>
                    <td>{session.uuid}</td>
                    <td>{moment(session.timestamp).fromNow()}</td>

                    <td>{session.pages}</td>
                    <td>{session.queue}</td>
                    <td>{session.percent}%</td>
                    <td>{session.status}</td>
                    <td>
                        <span onClick={this.retest}>Retest</span> | <span onClick={() => this.delete(session.uuid)}>Delete</span>


                    </td>
                </tr>
            )
        }.bind(this));

        if (this.state.loading === true) {
            return (
                <div>Loading data...</div>
            )
        } else {
            return (
                <div>
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
                                        When
                                    </th>

                                    <th>
                                        Crawled
                                    </th>

                                    <th>
                                        Queue
                                    </th>

                                    <th>
                                        Completion %
                                    </th>

                                    <th>
                                        Status
                                    </th>

                                    <th>
                                        Actions
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