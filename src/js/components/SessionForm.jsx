import React, { Component } from 'react';
import $ from 'jquery';

var moment = require('moment');

class SessionForm extends Component {

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

            console.log(post_data);

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
            <div className="card mt-5">
                <div className="card-block">
                     <h2>Start crawl</h2>
                    <form>
                        <div className="form-group">
                            <label htmlFor="crawl_url">Crawl URL</label>
                            <input type="text" className="form-control" id="crawl_url" placeholder="https://your-domain.com" ref={(el) => { this.textInput = el; }} />
                        </div>
                        <div className="form-group">
                            <label>Crawl Depth </label>
                            <input type="number" className="form-control" id="crawl_depth" defaultValue={0} ref={(el) => { this.depthInput = el; }} />
                            <p id="passwordHelpBlock" className="form-text text-muted">
                              0 is just the crawl url and does not follow links on that page
                            </p>
                        </div>
                        <div className="form-group">
                            <label>Analyse performance</label>
                            <input type="checkbox" className="form-control" id="performance_review" ref={(el) => { this.performanceInput = el; }} />

                        </div>
                        <div className="form-group">
                            <button type="submit" className="btn btn-primary" ref={(el) => { this.submit = el; }} onClick={this.startCrawl}>Start Crawl</button>
                        </div>
                    </form>
                </div>
            </div>
        )
    }
}


export default SessionForm;