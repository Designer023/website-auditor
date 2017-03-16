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
            let percentStyle = {
                width: session.percent + '%'
            };

            let percentBarStyle = ' bg-danger ';
            if (session.percent > 10 && session.percent <= 25) {
                percentBarStyle = ' bg-warning ';
            } else if (session.percent > 25 && session.percent < 100) {
                percentBarStyle = ' bg-info ';
            } else if (parseInt(session.percent) == 100){
                percentBarStyle = ' bg-success ';
            }

            let animated_progress = '';
            if (session.status_code === 1) {
                animated_progress = ' progress-bar-animated '
            }


            return (
                <tr key={session.uuid}>
                    <td><Link to={"/session/" + session.uuid } >{session.url}</Link></td>
                    {/*<td>{session.uuid}</td>*/}
                    <td>{moment(session.timestamp).fromNow()}</td>

                    <td>{session.pages}</td>
                    <td>{session.queue}</td>
                    <td>
                        <div className="progress">
                          <div className={"progress-bar progress-bar-striped " + percentBarStyle + animated_progress} role="progressbar" style={percentStyle} aria-valuenow="{session.percent}" aria-valuemin="0" aria-valuemax="100">{session.percent}%</div>
                        </div>
                    </td>
                    <td>{session.status}</td>
                    <td className="text-right">
                        <i className="fa fa-refresh" onClick={this.retest}></i> | <i className="fa fa-trash-o" onClick={() => this.delete(session.uuid)}></i>
                        {/*<i className="fa fa-refresh" onClick={this.retest}></i> | <i className="fa fa-trash-o" onClick={() => this.delete(session.uuid)}></i> | <i className="fa fa-pause-circle" onClick={this.retest}></i> | <i className="fa fa-play-circle" onClick={() => this.delete(session.uuid)}></i> | <i className="fa fa-archive" onClick={() => this.delete(session.uuid)}></i>*/}

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
                <div className="container">
                    <div className="jumbotron">
                          <h1 className="display-3">Sessions</h1>
                          <hr className="my-4" />


                    </div>

                     <div className="card mt-5">
                        <div className="card-block">
                             <h2>Start crawl</h2>
                            <form>
                                <div className="form-group">
                                    <label htmlFor="crawl_url">Crawl URL</label>
                                    <input type="text" className="form-control" id="crawl_url" placeholder="https://your-domain.com" ref={(el) => { this.textInput = el; }} />
                                </div>
                                <div className="form-group">
                                    <label>Crawl Depth </label>
                                    <input type="number" className="form-control" id="crawl_depth" defaultValue={0} ref={(el) => { this.depthInput = el; }} />
                                    <p id="passwordHelpBlock" className="form-text text-muted">
                                      0 is just the crawl url and does not follow links on that page
                                    </p>
                                </div>
                                <div className="form-group">
                                    <label>Analyse performance</label>
                                    <input type="checkbox" className="form-control" id="performance_review" ref={(el) => { this.performanceInput = el; }} />

                                </div>
                                <div className="form-group">
                                    <button type="submit" className="btn btn-primary" ref={(el) => { this.submit = el; }} onClick={this.startCrawl}>Start Crawl</button>
                                </div>
                            </form>
                        </div>
                     </div>


                    <div className="card mt-5">
                        <div className="card-block">



                             <table className="table table-striped table-responsive">
                            <thead className="thead-inverse">
                                <tr>
                                    <th >
                                        URL
                                    </th>
                                    {/*<th>*/}
                                        {/*Session*/}
                                    {/*</th>*/}

                                    <th className="col-md-2">
                                        When
                                    </th>

                                    <th className="col-md-1">
                                        Crawled
                                    </th>

                                    <th className="col-md-1">
                                        Queue
                                    </th>

                                    <th className="col-md-3">
                                        Completion
                                    </th>

                                    <th className="col-md-2">
                                        Status
                                    </th>

                                    <th className="col-md-1">
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