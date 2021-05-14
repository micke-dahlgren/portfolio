import React from 'react'
import Header from './header'
import '../scss/main.scss'
class Template extends React.Component {
  render() {
    const { children } = this.props

    return (
      <div className="layout">
        <Header />
        {children}
      </div>
    )
  }
}

export default Template
