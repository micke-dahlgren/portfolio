import React from "react";
import { graphql } from "gatsby";
import get from "lodash/get";
import { Helmet } from "react-helmet";

//components
import Layout from "../components/layout";
import Hero from "../components/home/hero";
import Bio from "../components/home/bio";

//static
import waves from "../../static/Waves.svg";

class RootIndex extends React.Component {
  render() {
    const hero = get(this, "props.data.contentfulHero");
    const bio = get(this, "props.data.contentfulBio");
    return (
      <Layout location={this.props.location}>
        <article className="home">
          <section className="home__section">
            <Hero hero={hero} />
          </section>
          <footer className="home__footer">
            <img alt="waves" className="home__footer__wave" src={waves} />
            <Bio bio={bio} />
          </footer>
        </article>
      </Layout>
    );
  }
}

export default RootIndex;

export const pageQuery = graphql`
  query HomeQuery {
    contentfulBio {
      bio {
        bio
      }
      title
      skills
    }
    contentfulHero(contentful_id: { eq: "15jwOBqpxqSAOy2eOO4S0m" }) {
      name
      tagline
      about {
        json
      }
      heroImage: image {
        fluid(
          quality: 100
          maxWidth: 226
          maxHeight: 291
          resizingBehavior: SCALE
        ) {
          ...GatsbyContentfulFluid_tracedSVG
        }
      }
    }
  }
`;
