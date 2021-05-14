import React from "react";
import { graphql } from "gatsby";
import Img from "gatsby-image"; 
import { Helmet } from "react-helmet";
import get from "lodash/get";
import Layout from "../components/layout";
import { documentToReactComponents } from "@contentful/rich-text-react-renderer";
import { BLOCKS, INLINES } from "@contentful/rich-text-types";

const RICHTEXT_OPTIONS = {
  renderNode: {
    [BLOCKS.PARAGRAPH]: (node, children) => {
      return <p>{children}</p>;
    },
    [BLOCKS.HEADING_1]: (node,children) => {
      return <h1>{children}</h1>;
    },
    [BLOCKS.HEADING_2]: (node,children) => {
      return <h2>{children}</h2>;
    },
    [BLOCKS.HEADING_3]: (node,children) => {
      return <h3>{children}</h3>;
    },
    [BLOCKS.HEADING_4]: (node,children) => {
      return <h4>{children}</h4>;
    },
    [BLOCKS.EMBEDDED_ASSET]: (node) => {
      return (
        <img
          src={node.data?.target?.fields?.file['en-US'].url}
          alt={node.data?.target?.fields?.title}
        />
      );
    },
    [INLINES.HYPERLINK]: (node, children) => {
      return <a href={node.data.uri}>{children}</a>;
    },
  },
};

class BlogPostTemplate extends React.Component {
  render() {
    const blogpost = get(this.props, "data.contentfulBlogPost");

    return (
      <Layout location={this.props.location}>
        <h1>{blogpost.title}</h1>
         <Img 
          alt={blogpost.heroImage.title}
          fluid={blogpost.heroImage.fluid}
          style={{ width: "920px", height: "400px" }}/>
        <div
          className="body"
          dangerouslySetInnerHTML={{
            __html: blogpost.body.childMarkdownRemark.html,
          }}
        />
      </Layout>
    );
  }
}


export default BlogPostTemplate

export const pageQuery = graphql`
  query PostBySlug($slug: String!) {
    contentfulBlogPost(slug: { eq: $slug }) {
      slug
      title
      description {
        description
      }
      body {
        childMarkdownRemark {
          html
        }
      }
      heroImage {
        fluid(quality: 100, resizingBehavior: PAD) {
          ...GatsbyContentfulFluid_withWebp
        }
      }
    }
  }`

