import React, { Component } from 'react';
import $ from 'jquery';

var moment = require('moment');

import SessionForm from './SessionForm';
import SessionTable from './SessionTable';
import { Link } from 'react-router'

class Sessions extends Component {

    constructor(props) {
        super(props);

        this.startCrawl = this.startCrawl.bind(this);
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


    render() {

        return (
            <div className="container">
                <div className="jumbotron">
                  <h1 className="display-3">Sessions</h1>
                  <hr className="my-4" />
                </div>

                <SessionForm />

                <SessionTable />
            </div>
        )
    }
}


export default Sessions;