import React from 'react';
import Header from './header';
import '../scss/main.scss';




const Layout = (props) => { 
  return (
    <div className="layout">
      <Header activePage={props.location.pathname}/>
      {props.children}
    </div>
  )
}

export default Layout
