import React, { Component } from 'react';

import { Link } from 'react-router'

import NavLink from './NavLink';

import LoadingIndicator from './LoadingIndicator';

import ResponseHeader from './ResponseHeader';
import HTMLErrors from './HTMLErrors';
import PageMeta from './PageMeta';

import $ from 'jquery';

class PageOverview extends Component {


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
                <div>

                    <div className="card mt-5">
                        <div className="card-block">

                            <div>
                                <div>
                                    <p>Errors: {this.state.data.html_errors.length}</p>
                                    <p>Performance: {this.state.data.yslow_results.score} / 100</p>
                                </div>

                                {this.props.children}

                            </div>
                        </div>
                    </div>
                </div>
            )
        }
    }
}


export default PageOverview;