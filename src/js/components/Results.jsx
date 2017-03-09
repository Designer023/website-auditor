import React, { Component } from 'react';

import { Link } from 'react-router'

import $ from 'jquery';

import LoadingIndicator from './LoadingIndicator';

class Results extends Component {

    constructor(props) {
        super(props);

        this.state = {
            tweets:[],
            loading: false
        };

        this.getTweets = this.getTweets.bind(this);

        //setInterval(this.getTweets, (5 * 1000));


    }

    componentDidMount() {
        this.getTweets();
    }


    getTweets() {
        if (this.state.loading === false) {

            this.setState(
                function(prevState, props){
                    return {
                        loading: true
                    }
                }
            );

            let queue_end_point = '/api/v1.0/auditor/results';

            $.ajax({
                type: 'GET',
                url: queue_end_point,
                success: function (data) {

                    this.setState(
                        function (prevState, props) {
                            return {
                                loading: false,
                                tweets: data.pages
                            }
                        })
                }.bind(this)
            });
        }

    }

    render() {

        let tweets = this.state.tweets.map(function(result) {

            return (





                <tr key={result.id}>
                    {/*<td>*/}
                        {/*{result.starting_url}*/}
                    {/*</td>*/}
                    <td>
                        <Link to={"/session/" + result.id } >{result.url}</Link>
                    </td>
                    <td>
                        {result.title}
                    </td>

                    <td>
                        { result.page_links.internal.length}
                    </td>

                    <td>
                        {result.html_errors.length}
                    </td>

                    {/*<td>*/}
                        {/*<pre dangerouslySetInnerHTML={{__html: result.header}}></pre>*/}
                    {/*</td>*/}
                </tr>



            )

        });


        return (
            <div>
                <div className="jumbotron">
                      <h1 className="display-3">Webpage Audit Results</h1>
                      <hr className="my-4" />
                      <p className="lead">
                        {this.state.tweets.length} Pages audited
                      </p>
                </div>
                <table className="table table-striped">
                    <thead className="thead-inverse">
                        <tr>
                            {/*<th>*/}
                                {/*URL*/}
                            {/*</th>*/}
                            <th>
                                Current url
                            </th>
                            <th>
                                Page title
                            </th>
                            <th>
                                Internal links
                            </th>
                            <th>
                                Validation Errors
                            </th>
                            {/*<th>*/}
                                {/*Headers*/}
                            {/*</th>*/}
                        </tr>
                    </thead>

                    <tbody>
                        {tweets}
                    </tbody>
                </table>

                <LoadingIndicator loading={this.state.loading} />
            </div>
        )
    }

}


export default Results;