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

        return (
            <div>

                <div className="card mt-5">
                    <div className="card-block">
                         <h2>Page overview for {this.props.params.page_id}</h2>

                        <nav className="navbar navbar-toggleable-md navbar-light bg-faded">
                          <button className="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                            <span className="navbar-toggler-icon"></span>
                          </button>
                          <div className="collapse navbar-collapse" id="navbarNav">
                            <ul className="navbar-nav">
                              <li className="nav-item">
                                  {/*<NavLink className="nav-link" to={"/page/" + this.props.params.page_id } >Overview</NavLink>*/}

                                  <Link className="nav-link" to={"/session/" + this.props.params.session_id + "/page/" + this.props.params.page_id } >Overview</Link>
                              </li>
                              <li className="nav-item">
                                  <Link className="nav-link" to={"/session/" + this.props.params.session_id + "/page/" + this.props.params.page_id + "/errors/" } >Errors</Link>
                              </li>
                              <li className="nav-item">
                                  <Link className="nav-link" to={"/session/" + this.props.params.session_id + "/page/" + this.props.params.page_id + "/meta/" } >Meta tags</Link>
                              </li>
                              <li className="nav-item">
                                  <Link className="nav-link" to={"/session/" + this.props.params.session_id + "/page/" + this.props.params.page_id + "/performance/" } >Performance</Link>
                              </li>
                                <li className="nav-item">
                                    <Link className="nav-link" to={"/session/" + this.props.params.session_id + "/page/" + this.props.params.page_id + "/headers/" } >Response headers</Link>
                                </li>
                            </ul>
                          </div>
                        </nav>

                        {this.props.children}
                    </div>
                 </div>
            </div>
        )
    }
}


export default Page;