import React from "react";
import Img from "gatsby-image";
import { documentToReactComponents } from "@contentful/rich-text-react-renderer";
import { BLOCKS, INLINES } from "@contentful/rich-text-types";
import styles from "./hero.module.scss";

const RICHTEXT_OPTIONS = {
  renderNode: {
    [BLOCKS.PARAGRAPH]: (node, children) => {
      return <p className={styles.tagline__paragraph} >{children}</p>;
    },
    [INLINES.HYPERLINK]: (node, children) => {
      return <a href={node.data.uri}>{children}</a>;
    },
  },
};

const Hero = ({ hero }) => {
  return (
    <div className={styles.hero}>
      <div className={styles.tagline}>
        <h1 className={styles.tagline__header}>{hero.tagline[0]}</h1>
        <h1 className={styles.tagline__header}>{hero.tagline[1]}</h1>
        {documentToReactComponents(hero.about.json, RICHTEXT_OPTIONS)}
        <div className={styles.buttonContainer}>
          <button className="primary" onClick={() => alert("hi")}>
            My work
          </button>
        </div>
      </div>
      <Img alt="mikael dahlgren" fluid={hero.heroImage.fluid} className={styles.img}/>
    </div>
  );
};

export default Hero;
