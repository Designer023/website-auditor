import React, { Component } from 'react';



class SessionsDetail extends Component {

    render() {

        return (
            <div className="card mt-5">
                <div className="card-block">
                     <h2>Session Detail for {this.props.params.session_id}</h2>

                     <p>List of pages for this session</p>
                </div>
             </div>
        )
    }
}


export default SessionsDetail;