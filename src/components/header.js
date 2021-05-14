import React from "react";
import { Link } from "gatsby";
import logo from "../../static/Logo.svg";

const Header = (props) => {
  const Nav = () => (
    <nav className="navigation" role="navigation">
      <ul className="navigation__menu">
        {Object.keys(props.navItems).map((key) => (
          <li
            key={key}
            className={
              props.activePage === props.navItems[key]
                ? "navigation__menu__item item--active"
                : "navigation__menu__item"
            }
          >
            <Link to={props.navItems[key]}>{key}</Link>
          </li>
        ))}
      </ul>
    </nav>
  );

  return (
    <div className="header">
      <img className="header__logo" src={logo} />
      <Nav />
      <div className="header__button-container">
        <button className="cta" onClick={() => alert(window.location.href)}>
          Contact me
        </button>
      </div>
    </div>
  );
};

export default Header;
