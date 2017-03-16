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

        this.startCrawl = this.startCrawl.bind(this);

        this.retest = this.retest.bind(this);
        this.delete = this.delete.bind(this);
        this.updateData = this.updateData.bind(this);
    }

    componentDidMount() {
        this.getData();

        // Every 5 seconds get more data
        setInterval(this.updateData, (5 * 1000));
    }

    startCrawl(e) {
        e.preventDefault();

        //get value from url submitted
        let test_url = (this.textInput.value );
        let test_depth = (this.depthInput.value);
        let performance_flag = (this.performanceInput.checked);

        //validate
        let valid = /^(ftp|http|https):\/\/[^ "]+$/.test(test_url);

        if (valid === true) {
            //Valid - send all of the AJAXES!

            let post_data = {
                url: test_url,
                depth: test_depth,
                performance: performance_flag

            };

            console.log(post_data);

            let crawl_end_point = '/api/v1.0/auditor/sessions';

            $.ajax({
                type: 'POST',
                data: post_data,
                url: crawl_end_point,
                success: function (data) {
                    console.log(data)
                }.bind(this)
            });


        } else {
            // Flag up a warning!
            alert("That's not a url!");
            return false;
        }
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

    updateData() {
        // Assume we have data already from the initial getData callback.
        // No loading state will be triggered!

        let queue_end_point = '/api/v1.0/auditor/sessions';

        $.ajax({
            type: 'GET',
            url: queue_end_point,
            success: function (data) {

                // Ste loading to false as we now have data!
                this.setState(
                    function (prevState, props) {
                        return {
                            sessions: data.sessions,
                            loading: false,
                        }
                    })
            }.bind(this)
        });

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
                             <h2>Start crawl</h2>
                            <label>
                                Crawl URL
                                <input type="text" ref={(el) => { this.textInput = el; }} />
                            </label>

                            <label>
                                Crawl Depth - 0 is just the crawl url and does not follow links on that page
                                <input type="number" ref={(el) => { this.depthInput = el; }} />
                            </label>

                            <label>
                                Analyse performance
                                <input type="checkbox" ref={(el) => { this.performanceInput = el; }} />
                            </label>

                            <input type="submit" ref={(el) => { this.submit = el; }} onClick={this.startCrawl}/>
                        </div>
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