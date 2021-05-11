import React from "react";
import Img from "gatsby-image";
const ProjectLink = ({ project }) => {
  console.log(project);
  return (
    <a href={'/projects/'+project.slug}>
      <div>
        <Img
          alt="some alt"
          fluid={project.heroImage.fluid}
          style={{ width: "400px", height: "400px" }}
        />
      </div>
      <div>
        <h2>{project.title}</h2>
        <p>{project.description.description}</p>
      </div>
    </a>
  );
};

export default ProjectLink;
