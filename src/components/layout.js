import React from 'react'
import Header from './header'
import '../scss/main.scss'

const navItems = {
  Home: "/",
  Projects: "/projects",
  Blog: "/blog",
};


const Layout = (props) => { 
  return (
    <div className="layout">
      <Header navItems={navItems} activePage={props.location.pathname}/>
      {props.children}
    </div>
  )
}

export default Layout
