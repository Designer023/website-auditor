import React, {Component} from 'react'
import { Link } from 'react-router'



class NavLink extends Component {
    render() {
        // return (
        //     <li className="nav-item">
        //         <Link {...this.props} />
        //     </li>
        // )


        const { router } = this.context;
        const { index, onlyActiveOnIndex, to, children, ...props } = this.props;

        const isActive = router.isActive(to, onlyActiveOnIndex);
        const LinkComponent = index ? Link : IndexLink;

        return (
          <li className={isActive ? 'active' : ''}>
            <LinkComponent {...props}>{children}</LinkComponent>
          </li>
        )
    }



}

export default NavLink