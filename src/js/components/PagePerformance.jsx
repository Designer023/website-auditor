import React, { Component } from 'react';

import PageMeta from './PageMeta';

import $ from 'jquery';

class PagePerformance extends Component {


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
                <div className="container-fluid">
                    <div>
                        <p>Loading...</p>
                    </div>
                </div>
            )
        } else {


            let generate_yslow_button = (null)
            let yslow_data = ( null );

            if (this.state.data.yslow_results  !== "" ) {

                yslow_data = (
                    <div>
                        <table className="table table-striped">
                            <thead className="thead-inverse">
                                <tr>
                                    <th>
                                        Overview
                                    </th>
                                    <th>
                                        Score
                                    </th>
                                </tr>
                            </thead>
                             <tbody>
                                <tr >
                                    <td>Score</td>
                                    <td>{this.state.data.yslow_results.score}</td>
                                </tr>
                                <tr>
                                    <td>Pagesize</td>
                                    <td>{Math.round(this.state.data.yslow_results.size / 1024 / 1024* 100) / 100 + ' Mb'}</td>
                                </tr>
                                <tr>
                                    <td>Load time</td>
                                    <td>{this.state.data.yslow_results.load_time / 1000 + ' seconds'}</td>
                                </tr>
                             </tbody>
                        </table>

                        <table className="table table-striped">
                            <thead className="thead-inverse">
                                <tr>
                                    <th>
                                        YSlow rule name
                                    </th>
                                    <th>
                                        Score
                                    </th>
                                </tr>
                            </thead>
                             <tbody>

                                 <tr >
                                    <td>Make fewer HTTP requests</td>
                                    <td>{this.state.data.yslow_results.breakdown.ynumreq}</td>
                                </tr>

                                <tr >
                                    <td>Use a CDN</td>
                                    <td>{this.state.data.yslow_results.breakdown.ycdn}</td>
                                </tr>

                                <tr >
                                    <td>Avoid empty src or href</td>
                                    <td>{this.state.data.yslow_results.breakdown.yemptysrc}</td>
                                </tr>

                                <tr >
                                    <td>Add an Expires header</td>
                                    <td>{this.state.data.yslow_results.breakdown.yexpires}</td>
                                </tr>

                                <tr >
                                    <td>Compress components</td>
                                    <td>{this.state.data.yslow_results.breakdown.ycompress}</td>
                                </tr>

                                <tr >
                                    <td>Put CSS at top</td>
                                    <td>{this.state.data.yslow_results.breakdown.ycsstop}</td>
                                </tr>

                                <tr >
                                    <td>Put Javascript at the bottom</td>
                                    <td>{this.state.data.yslow_results.breakdown.yjsbottom}</td>
                                </tr>

                                <tr >
                                    <td>Avoid CSS expression</td>
                                    <td>{this.state.data.yslow_results.breakdown.yexpressions}</td>
                                </tr>

                                <tr >
                                    <td>Make JS and CSS external</td>
                                    <td>{this.state.data.yslow_results.breakdown.yexternal}</td>
                                </tr>

                                <tr >
                                    <td>Reduce DNS lookups</td>
                                    <td>{this.state.data.yslow_results.breakdown.ydns}</td>
                                </tr>

                                <tr >
                                    <td>Minify JS and CSS</td>
                                    <td>{this.state.data.yslow_results.breakdown.yminify}</td>
                                </tr>

                                <tr >
                                    <td>Avoid redirects</td>
                                    <td>{this.state.data.yslow_results.breakdown.yredirects}</td>
                                </tr>

                                <tr >
                                    <td>Remove duplicate JS and CSS</td>
                                    <td>{this.state.data.yslow_results.breakdown.ydupes}</td>
                                </tr>

                                <tr >
                                    <td>Configure ETags</td>
                                    <td>{this.state.data.yslow_results.breakdown.yetags}</td>
                                </tr>

                                <tr >
                                    <td>Make Ajax cacheable</td>
                                    <td>{this.state.data.yslow_results.breakdown.yxhr}</td>
                                </tr>

                                <tr >
                                    <td>Use GET for AJAX requests</td>
                                    <td>{this.state.data.yslow_results.breakdown.yxhrmethod}</td>
                                </tr>

                                <tr >
                                    <td>Reduce the Number of DOM elements</td>
                                    <td>{this.state.data.yslow_results.breakdown.ymindom}</td>
                                </tr>

                                <tr >
                                    <td>No 404s</td>
                                    <td>{this.state.data.yslow_results.breakdown.yno404}</td>
                                </tr>

                                <tr >
                                    <td>Reduce Cookie Size</td>
                                    <td>{this.state.data.yslow_results.breakdown.ymincookie}</td>
                                </tr>

                                <tr >
                                    <td>Use Cookie-free Domains</td>
                                    <td>{this.state.data.yslow_results.breakdown.ymincookie}</td>
                                </tr>

                                <tr >
                                    <td>Avoid filters</td>
                                    <td>{this.state.data.yslow_results.breakdown.ynofilter}</td>
                                </tr>

                                <tr >
                                    <td>Don't Scale Images in HTML</td>
                                    <td>{this.state.data.yslow_results.breakdown.yimgnoscale}</td>
                                </tr>

                                <tr >
                                    <td>Make favicon Small and Cacheable</td>
                                    <td>{this.state.data.yslow_results.breakdown.yfavicon}</td>
                                </tr>

                             </tbody>
                        </table>
                    </div>
                    )

            } else {
                generate_yslow_button = (
                    <span className="btn btn-primary btn-lg"  role="button">Generate YSlow analysis</span>
                )
            }

            return (
                <div>
                    <div className="card mt-5">
                        <div className="card-block">
                             {yslow_data}
                        </div>
                    </div>
                </div>

            )
        }
    }
}


export default PagePerformance;