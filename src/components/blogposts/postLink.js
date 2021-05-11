import React from "react";
import Img from "gatsby-image";
const PostLink = ({ post }) => {

  return (
    <a href={'/blog/'+post.slug}>
      <div>
        <Img
          alt="some alt"
          fluid={post.heroImage.fluid}
          style={{ width: "400px", height: "400px" }}
        />
      </div>
      <div>
        <h2>{post.title}</h2>
        <p>{post.description.description}</p>
      </div>
    </a>
  );
};

export default PostLink;
