import React, { Component } from 'react';
import $ from 'jquery';

import { Link } from 'react-router'

class SessionsDetail extends Component {

    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            pages: []
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

            let queue_end_point = '/api/v1.0/auditor/results/' + this.props.params.session_id;

            $.ajax({
                type: 'GET',
                url: queue_end_point,
                success: function (data) {

                    this.setState(
                        function (prevState, props) {
                            return {
                                loading: false,
                                pages: data.pages
                            }
                        })
                }.bind(this)
            });
        // }
    }

    render() {



            if (this.state.loading === true) {
                return (
                    <div>Loading data...</div>
                )
            } else {

                let page_results = this.state.pages.map(function(page) {

                return (

                    <tr key={page.id}>

                        <td>
                            <Link to={"/page/" + page.id } >{page.url}</Link>
                        </td>

                        <td>
                            {page.title}
                        </td>

                        <td>
                            <Link to={"/page/" + page.id + "/errors/" } >{page.html_errors.length}</Link>
                        </td>

                        <td>
                            -
                        </td>

                    </tr>

                )

            });

            return (
                <div>
                    <div className="jumbotron">
                          <h1 className="display-3">Crawl details</h1>
                          <hr className="my-4" />

                            <h3 className="lead">URL for crawl</h3>
                            <h4>Session uuid: {this.props.params.session_id}</h4>

                    </div>
                    <div className="card mt-5">
                        <div className="card-block">
                             <h2>Pages crawled</h2>

                             <table className="table table-striped">
                            <thead className="thead-inverse">
                                <tr>
                                    <th>
                                        URL
                                    </th>
                                    <th>
                                        Title
                                    </th>


                                    <th>
                                        Errors
                                    </th>
                                    <th>
                                        Performance
                                    </th>

                                </tr>
                            </thead>

                            <tbody>

                                {page_results}

                            </tbody>
                        </table>
                        </div>
                     </div>
                </div>
            )
        }

    }
}


export default SessionsDetail;