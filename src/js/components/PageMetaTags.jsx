import React, { Component } from 'react';



class PageMetaTags extends Component {

    render() {

        return (
            <div className="card mt-5">
                <div className="card-block">
                     <h2>Page meta tags for {this.props.params.page_id}</h2>

                     <p>A list of stats</p>
                </div>
             </div>
        )
    }
}


export default PageMetaTags;