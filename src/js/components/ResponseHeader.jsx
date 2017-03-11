import React, { Component } from 'react';



class ResponseHeader extends Component {

    render() {
        return (
            <div className="card mt-5">
                  <div className="card-block">
                    <h4>Response header</h4>

                    <pre>
                        {this.props.header_data}
                    </pre>
                </div>
            </div>
        )
    }
}



export default ResponseHeader;