import React from "react";
import { Link } from "gatsby";
import logo from "../../static/Logo.svg";

const navItems = {
  Home: "/",
  Projects: "/projects/",
  Blog: "/blog",
};

console.log("con: ", Object.keys(navItems));

const navigation = () => (
  <nav className="navigation" role="navigation">
    <ul className="navigation-item-container">
      {Object.keys(navItems).map((key) => (
        <li className="navigation-item">
          <Link to={navItems[key]}>{key}</Link>
        </li>
      ))}
    </ul>
  </nav>
);

export default () => (
  <div className="header">
    <img src={logo} />
    {navigation()}
    <div className="buttonContainer">
      <button className="cta" onClick={() => alert("hi")}>
        Contact me
      </button>
    </div>
  </div>
);
