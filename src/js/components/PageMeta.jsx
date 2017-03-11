import React, { Component } from 'react';



class PageMeta extends Component {

    render() {

        let meta_tags = this.props.page_meta.map(function(meta, index) {
            return (
                <tr key={index}>
                    <td>{meta}</td>
                </tr>
            )
        });

        return (
            <div className="card mt-5">
                <div className="card-block">
                     <h4>Page meta tags</h4>

                     <table className="table table-striped">
                        <thead className="thead-inverse">
                            <tr>
                                <th>
                                    Meta tag
                                </th>
                            </tr>
                        </thead>

                        <tbody>

                            {meta_tags}

                        </tbody>
                    </table>
                </div>
             </div>
        )
    }
}


export default PageMeta;