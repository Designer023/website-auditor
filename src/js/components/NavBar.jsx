import React, { Component } from 'react';



class NavBar extends Component {

    render() {

        return(

             <nav className="navbar navbar-toggleable-md navbar-light bg-faded mb-3">
              <button className="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation" >
                <span className="navbar-toggler-icon"></span>
              </button>
              <a className="navbar-brand" href="/">Website Auditor</a>

            </nav>

        )

    }
}



export default NavBar;