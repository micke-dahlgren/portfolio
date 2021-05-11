import React from 'react'
import Img from 'gatsby-image'
import { documentToReactComponents } from '@contentful/rich-text-react-renderer'
import {BLOCKS, INLINES} from '@contentful/rich-text-types'

const RICHTEXT_OPTIONS = {
  renderNode: {
    [BLOCKS.PARAGRAPH] : (node,children) => {
      return <p>{children}</p>
    },
    [INLINES.HYPERLINK]: (node, children) => {
      return <a href={node.data.uri}>{children}</a>
    }
  }
}

const Hero = ({hero}) => {
    return(
    <div>
    {hero.name}
    <h1>{hero.tagline[0]}</h1>
    <h1>{hero.tagline[1]}</h1>
    <Img
      alt="some alt"
      fluid={hero.heroImage.fluid}
      style={{width:'200px'}}
    />
    {documentToReactComponents(hero.about.json, RICHTEXT_OPTIONS)}
  </div>
    )
}

export default Hero;