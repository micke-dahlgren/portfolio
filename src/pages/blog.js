import React from 'react'
import { graphql } from 'gatsby'
import get from 'lodash/get'
//components
import Layout from '../components/layout'
import PostLink from '../components/blogposts/postLink'

class BlogPosts extends React.Component {
  render() {
    const posts = get(this, 'props.data.allContentfulBlogPost.edges')

    return (
      <Layout location={this.props.location}>
        {posts.map((post, i) => (<PostLink key={i} post={post.node}/>))}
      </Layout>
    )
  }
}
export const pageQuery = graphql`
  query blogpostBySlug {
  allContentfulBlogPost(sort: {fields: createdAt, order: DESC}) {
    edges {
      node {
        title
        slug
        publishDate
        body {
          body
        }
        heroImage {
          fluid(
            quality:100,
            resizingBehavior: PAD
          ) {
            ...GatsbyContentfulFluid_tracedSVG
          }
        }
        description {
          description
        }
      }
    }
  }
}`

export default BlogPosts
