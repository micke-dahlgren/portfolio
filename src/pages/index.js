import React from 'react'
import { graphql } from 'gatsby'
import get from 'lodash/get'
import Img from 'gatsby-image'
import { Helmet } from 'react-helmet'
import Hero from '../components/hero'
import Layout from '../components/layout'
import ArticlePreview from '../components/article-preview'

class RootIndex extends React.Component {
  render() {

    const hero = get(this, 'props.data.contentfulPerson')
    console.log(hero)
    return (
      <Layout location={this.props.location}>
        <div>
          {hero.name}
          <div>{hero.title}</div>
          <Img
            alt="some alt"
            fluid={hero.heroImage.fluid}
            style={{width:'200px'}}
          />
        </div>
      </Layout>
    )
  }
}

export default RootIndex

export const pageQuery = graphql`
  query HomeQuery {
    contentfulPerson(contentful_id: {eq: "15jwOBqpxqSAOy2eOO4S0m"}) {
      name
      title
      heroImage: image {
        fluid(
          quality:100
          maxWidth: 226
          maxHeight: 291
          resizingBehavior: PAD

        ) {
          ...GatsbyContentfulFluid_tracedSVG
        }
      }
    }
  }
`

// export const pageQuery = graphql`
//   query HomeQuery {
//     allContentfulPerson(
//       filter: { contentful_id: { eq: "15jwOBqpxqSAOy2eOO4S0m" } }
//     ) {
//       edges {
//         node {
//           name
//           about {
//             about
//           }
//           title
//           heroImage: image {
//             fluid(
//               quality:100
//               maxWidth: 226
//               maxHeight: 291
//               resizingBehavior: PAD
              
//             ) {
//               ...GatsbyContentfulFluid_tracedSVG
//             }
//           }
//         }
//       }
//     }
//   }
// `
