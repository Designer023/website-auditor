import React, { Component } from 'react';

import { Link } from 'react-router'

import NavLink from './NavLink';

import LoadingIndicator from './LoadingIndicator';

import ResponseHeader from './ResponseHeader';
import HTMLErrors from './HTMLErrors';
import PageMeta from './PageMeta';

import $ from 'jquery';

class Page extends Component {


    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            data: []
        }

        this.getData = this.getData.bind(this);
        this.retestPage = this.retestPage.bind(this)
    }

    componentDidMount() {
        this.getData();
    }


    retestPage() {

        let queue_end_point = '/api/v1.0/auditor/detail/' + this.props.params.page_id;

        let post_data = {
            url: this.state.data.url,
            performance: false,
            uuid: this.props.params.session_id
        };

        $.ajax({
            type: 'POST',
            data: post_data,
            url: queue_end_point,
            success: function (data) {

                console.log(data)

            }.bind(this)
        });
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

            let queue_end_point = '/api/v1.0/auditor/detail/' + this.props.params.page_id;

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
                <div>Loading...</div>
            )
        } else {
            return (
                <div className="container">

                     <div className="jumbotron">
                          <h1 className="display-3">Page overview</h1>
                          <hr className="my-4" />

                         <h3 className="lead">URL: <a href={this.state.data.url} target="_blank">{this.state.data.url}</a></h3>
                         <h4>Session uuid: <Link to={"/session/" + this.props.params.session_id } >{this.props.params.session_id}</Link></h4>
                         <span className="btn btn-primary" onClick={this.retestPage}>Restest</span>
                    </div>


                    <nav
                        className="navbar navbar-toggleable-md navbar-light bg-faded">
                        <button
                            className="navbar-toggler navbar-toggler-right"
                            type="button" data-toggle="collapse"
                            data-target="#navbarNav"
                            aria-controls="navbarNav"
                            aria-expanded="false"
                            aria-label="Toggle navigation">
                            <span
                                className="navbar-toggler-icon"></span>
                        </button>
                        <a className="navbar-brand" href="/">Page</a>
                        <div className="collapse navbar-collapse"
                             id="navbarNav">
                            <ul className="navbar-nav">
                                <li className="nav-item">
                                    {/*<NavLink className="nav-link" to={"/page/" + this.props.params.page_id } >Overview</NavLink>*/}

                                    <Link className="nav-link"
                                          to={"/session/" + this.props.params.session_id + "/page/" + this.props.params.page_id + '/overview/'}>Overview</Link>
                                </li>
                                <li className="nav-item">
                                    <Link className="nav-link"
                                          to={"/session/" + this.props.params.session_id + "/page/" + this.props.params.page_id + "/errors/" }>Errors</Link>
                                </li>
                                <li className="nav-item">
                                    <Link className="nav-link"
                                          to={"/session/" + this.props.params.session_id + "/page/" + this.props.params.page_id + "/meta/" }>Meta
                                        tags</Link>
                                </li>
                                <li className="nav-item">
                                    <Link className="nav-link"
                                          to={"/session/" + this.props.params.session_id + "/page/" + this.props.params.page_id + "/performance/" }>Performance</Link>
                                </li>
                                <li className="nav-item">
                                    <Link className="nav-link"
                                          to={"/session/" + this.props.params.session_id + "/page/" + this.props.params.page_id + "/headers/" }>Response
                                        headers</Link>
                                </li>
                            </ul>
                        </div>
                    </nav>

                    <div>

                        {this.props.children}

                    </div>

                </div>
            )
        }
    }
}


export default Page;