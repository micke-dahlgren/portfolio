import React from 'react'
import { graphql } from 'gatsby'
import get from 'lodash/get'
import { Helmet } from 'react-helmet'

//components
import Layout from '../components/layout'
import ProjectLink from '../components/projects/projectLink'

class Projects extends React.Component {
  render() {
    const projects = get(this, 'props.data.allContentfulProject.edges')

    return (
      <Layout location={this.props.location}>
        {projects.map((project, i) => (<ProjectLink key={i} project={project.node} />))}
      </Layout>
    )
  }
}

export default Projects

export const pageQuery = graphql`
  query projectQuery { allContentfulProject {
    edges {
      node {
        id
        title
        slug
        description {
          description
        }
        heroImage {
          fluid(quality:100, maxHeight: 800, maxWidth: 800, resizingBehavior: PAD) {
            srcSetWebp
          }
        }
      }
    }
  }
}`

