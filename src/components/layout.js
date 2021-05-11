import React from 'react'
import Navigation from './navigation'

class Template extends React.Component {
  render() {
    const { children } = this.props

    return (
      <div className="layout">
        <Navigation />
        {children}
      </div>
    )
  }
}

export default Template
