import React, { Component } from 'react';

import LoadingIndicator from './LoadingIndicator';

import $ from 'jquery';

class SessionDetailDash extends Component {

    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            data: []
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
                        <h2>Details for {this.props.params.session_id}</h2>
                        <LoadingIndicator />
                    </div>
                </div>
            )
        } else {



            let html_errors = this.state.data.html_errors.map(function(error_message, index) {
                return (
                    <tr key={index}>
                        <td>{error_message}</td>
                    </tr>
                )
            });



            let meta_tags = this.state.data.page_meta.map(function(meta, index) {
                return (
                    <tr key={index}>
                        <td>{meta}</td>
                    </tr>
                )
            });



            let generate_yslow_button = (<p>No YSlow data generated</p>);
            if (this.state.data.yslow_results.length == 0) {
                generate_yslow_button =  (
                    <a className="btn btn-primary btn-lg" href="#" role="button">Generate YSlow analysis</a>
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

                            </div>


                             <h4>Response header</h4>

                            <pre>
                                {this.state.data.header}
                            </pre>


                             <h4>YSlow analytics</h4>

                             {generate_yslow_button}

                             <h4>HTML errors</h4>

                             <table className="table table-striped">
                                <thead className="thead-inverse">
                                    <tr>
                                        <th>
                                            Errors
                                        </th>
                                    </tr>
                                </thead>

                                <tbody>

                                    {html_errors}

                                </tbody>
                            </table>


                             <h4>Page meta tags</h4>

                             <table className="table table-striped">
                                <thead className="thead-inverse">
                                    <tr>
                                        <th>
                                            Meta tag
                                        </th>
                                    </tr>
                                </thead>

                                <tbody>

                                    {meta_tags}

                                </tbody>
                            </table>


                        </div>
                    </div>
                </div>
            )
        }


    }
}



export default SessionDetailDash;