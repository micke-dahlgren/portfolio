import React, {useState} from "react";
//components
import Nav from './nav';

//static
import logo from "../../static/Logo.svg";

const navItems = {
  Home: "/",
  Projects: "/projects",
  Blog: "/blog",
};

const Header = (props) => {
  const [hamburger, setHamburger] = useState(true);

  const Hamburger = () =>(
    <a href={void(0)} onClick={() => setHamburger(!hamburger)} className="hamburger">
      <i className="hamburger__span" />
      <i className="hamburger__span" />
      <i className="hamburger__span" />
    </a>
  )

  return (
    <div className="header">
      <Hamburger />
      <img className="header__logo" src={logo} />
      {hamburger ? <Nav navItems={navItems} activePage={props.activePage}/> : null}
      <div className="header__button-container">
        <button className="cta" onClick={() => alert(window.location.href)}>
          Contact me
        </button>
      </div>
    </div>
  );
};

export default Header;
