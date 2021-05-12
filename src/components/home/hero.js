import React from 'react'
import Img from 'gatsby-image'
import { documentToReactComponents } from '@contentful/rich-text-react-renderer'
import {BLOCKS, INLINES} from '@contentful/rich-text-types'
import styles from './home.module.scss'

const RICHTEXT_OPTIONS = {
  renderNode: {
    [BLOCKS.PARAGRAPH] : (node,children) => {
      return <p className="alt">{children}</p>
    },
    [INLINES.HYPERLINK]: (node, children) => {
      return <a href={node.data.uri}>{children}</a>
    }
  }
}

const Hero = ({hero}) => {
    return(
    <section className={styles.hero}>
      <div>
        <h1>{hero.tagline[0]}</h1>
        <h1>{hero.tagline[1]}</h1>
        {documentToReactComponents(hero.about.json, RICHTEXT_OPTIONS)}
        <button className="primary" onClick={() => alert('hi')}>My work</button>
      </div>
      <Img
        alt="some alt"
        fluid={hero.heroImage.fluid}
        style={{width:'200px'}}
      />
  </section>
    )
}

export default Hero;