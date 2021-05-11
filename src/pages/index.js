import React from 'react'
import { graphql } from 'gatsby'
import get from 'lodash/get'
import { Helmet } from 'react-helmet'


//components
import Layout from '../components/layout'
import Hero from '../components/home/hero'
import Bio from '../components/home/bio'

class RootIndex extends React.Component {
  render() {

    const hero = get(this, 'props.data.contentfulHero')
    const bio = get(this, 'props.data.contentfulBio')
    return (
      <Layout location={this.props.location}>
        <Hero hero={hero} />
        <Bio bio={bio} />
        <button>Contact me</button>
      </Layout>
    )
  }
}

export default RootIndex

export const pageQuery = graphql`
  query HomeQuery {
    contentfulBio {
    bio {
      bio
    }
    title
    skills
  }
    contentfulHero(contentful_id: {eq: "15jwOBqpxqSAOy2eOO4S0m"}) {
      name
      tagline
      about {
      json
    }
      heroImage: image {
        fluid(
          quality:100,
          maxWidth: 226,
          maxHeight: 291,
          resizingBehavior: PAD
        ) {
          ...GatsbyContentfulFluid_tracedSVG
        }
      }
    }
  }
`

