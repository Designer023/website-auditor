import React, { Component } from 'react';

import ResponseHeader from './ResponseHeader';

import $ from 'jquery';

class PageHeaders extends Component {

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
            return (


                        <ResponseHeader header_data={this.state.data.header} />

            )
        }
    }
}


export default PageHeaders;
