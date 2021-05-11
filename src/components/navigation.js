import React from 'react'
import { Link } from 'gatsby'
import styles from './navigation.module.scss'
import logo from '../../static/Logo.svg'

export default () => (
  <div className={styles.header}>
    <img src={logo} />
    <nav role="navigation">
      <ul className={styles.navigation}>
        
        <li className={styles.navigationItem}>
          <Link to="/">Home</Link>
        </li>
        <li className={styles.navigationItem}>
          <Link to="/projects/">Projects</Link>
        </li>
        <li className={styles.navigationItem}>
          <Link to="/blog/">Blog</Link>
        </li>
      </ul>
    </nav>
    <div className={styles.buttonContainer}>
      <button className="primary" onClick={() => alert('hi')}>Contact me</button>
    </div>
  </div>
)
