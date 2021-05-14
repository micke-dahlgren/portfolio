import React from "react";

const getSkills = (skills) => {
	return skills.map((e) => (
		<div>{e}</div>
	))
}

const Bio = ({ bio }) => {
  let bioParagraph = bio.bio.bio
  return (
    <div key="ABC">
      <h1>{bio.title}</h1>
      <p>{bioParagraph}</p>
			<p><b>Here are a few technologies I've been working with recently:</b></p>
			{getSkills(bio.skills)}
    </div>
  );
};

export default Bio;
