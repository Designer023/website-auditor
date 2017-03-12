import React, { Component } from 'react';



class HTMLErrors extends Component {

    render() {

        let html_errors = this.props.html_errors.map(function(error_message, index) {
            return (
                <tr key={index}>
                    <td>{error_message}</td>
                </tr>
            )
        });

        return (
            <div className="card mt-5">
                <div className="card-block">
                    <h4>HTML errors - <a href={ this.props.src } target="_blank">source</a></h4>

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
                </div>
            </div>
        )
    }
}


export default HTMLErrors;