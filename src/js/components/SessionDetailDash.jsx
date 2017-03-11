import React, { Component } from 'react';

import LoadingIndicator from './LoadingIndicator';

import ResponseHeader from './ResponseHeader';
import HTMLErrors from './HTMLErrors';
import PageMeta from './PageMeta';

import $ from 'jquery';

class SessionDetailDash extends Component {

    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            data: []
        }

        this.getData = this.getData.bind(this);
        this.getYSlow = this.getYSlow.bind(this);
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

            let queue_end_point = '/api/v1.0/auditor/detail/' + this.props.params.session_id;

            $.ajax({
                type: 'GET',
                url: queue_end_point,
                success: function (data) {

                    this.setState(
                        function (prevState, props) {
                            return {
                                loading: false,
                                data: data.data
                            }
                        })
                }.bind(this)
            });
        // }

    }




    getYSlow() {
        // if (this.state.loading === false) {

            this.setState(
                function(prevState, props){
                    return {
                        loading: true
                    }
                }
            );

            let queue_end_point = '/api/v1.0/auditor/yslow/' + this.props.params.session_id;

            $.ajax({
                type: 'GET',
                url: queue_end_point,
                success: function (data) {

                    this.setState(
                        function (prevState, props) {
                            return {
                                loading: false,
                                data: data.data
                            }
                        })
                }.bind(this)
            });
        // }

    }



    render() {




        if (this.state.loading === true) {
            return (
                <div className="container-fluid">
                    <div>
                        <h2>Updating</h2>
                        <LoadingIndicator />
                    </div>
                </div>
            )
        } else {











            let generate_yslow_button = (
                <span className="btn btn-primary btn-lg" onClick={this.getYSlow} role="button">Generate YSlow analysis</span>
            );

            let yslow_data = ( null );

            if (this.state.data.yslow_results  !== "" ) {
                generate_yslow_button =  (
                    null
                )

                yslow_data = (
                    <table className="table table-striped">
                        <thead className="thead-inverse">
                            <tr>
                                <th>
                                    Yslow
                                </th>
                            </tr>
                        </thead>
                         <tbody>
                            <tr >
                                <td>Score: {this.state.data.yslow_results.score}</td>
                            </tr>
                            <tr>
                                <td>Pagesize: {Math.round(this.state.data.yslow_results.size / 1024 / 1024* 100) / 100 + ' Mb'}</td>
                            </tr>
                            <tr>
                                <td>Load time: {this.state.data.yslow_results.load_time / 1000 + ' seconds'}</td>
                            </tr>
                         </tbody>
                    </table>
                    )

            }


            return (
                <div className="container-fluid">
                    <div className="container-fluid">
                         <div>
                             <div className="jumbotron">
                                  <h1 className="display-3">{this.state.data.url}</h1>
                                  <hr className="my-4" />


                                    <h3 className="lead">{this.state.data.title}</h3>
                                    <h4>Session uuid: {this.state.data.session_uuid}</h4>

                            </div>

                             <ResponseHeader header_data={this.state.data.header} />

                             <div className="card mt-5">
                                <div className="card-block">
                                     <h4>YSlow analytics</h4>
                                     {generate_yslow_button}
                                </div>
                             </div>



                                {yslow_data}



                             <HTMLErrors html_errors={this.state.data.html_errors} />

                             <PageMeta page_meta={this.state.data.page_meta} />


                        </div>
                    </div>
                </div>
            )
        }


    }
}



export default SessionDetailDash;