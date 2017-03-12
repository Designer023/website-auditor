import React, { Component } from 'react';



class PageHeaders extends Component {

    render() {

        return (
            <div className="card mt-5">
                <div className="card-block">
                     <h2>Page headers for {this.props.params.page_id}</h2>

                     <p>A list of stats</p>
                </div>
             </div>
        )
    }
}


export default PageHeaders;