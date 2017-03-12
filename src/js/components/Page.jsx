import React, { Component } from 'react';

import { Link } from 'react-router'

class Page extends Component {

    render() {

        return (
            <div className="card mt-5">
                <div className="card-block">
                     <h2>Page overview for {this.props.params.page_id}</h2>


                    <Link to={"/page/" + this.props.params.page_id + "/errors/" } >Errors</Link>

                     <p>A list of stats</p>

                    {this.props.children}
                </div>
             </div>
        )
    }
}



export default Page;