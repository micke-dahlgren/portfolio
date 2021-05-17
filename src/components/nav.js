import React from 'react';
import { Link } from "gatsby";
import styles from './nav.module.scss';

const Nav = ({navItems, activePage}) => {
  return(
  <nav className={styles.navigation} role="navigation">
    <ul className={styles.navigation__menu}>
      {Object.keys(navItems).map((key) => (
        <li
          key={key}
          className={
            activePage === navItems[key]
              ? styles.navigation__menu__item + ' ' + styles.item__active
              : styles["navigation__menu__item"]
          }
        >
          <Link to={navItems[key]}>{key}</Link>
        </li>
      ))}
    </ul>
  </nav>
  );
};

export default Nav;

