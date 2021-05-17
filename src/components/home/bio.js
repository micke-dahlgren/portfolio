import React from "react";
import styles from "./bio.module.scss";

const getSkills = (skills) => {
	return skills.map((e,i) => (
		<div className="tag" key={i}><span className="tag__text">{e}</span></div>
	))
}

const Bio = ({ bio }) => {
  let bioParagraph = bio.bio.bio
  return (
    <div className={styles.bio}>
      <h1 className={styles.bio__header}>{bio.title}</h1>
      <p className={styles.bio__paragraph}>{bioParagraph}</p>
			<p className={styles.bio__paragraph}><b>Here are a few technologies I've been working with recently:</b></p>
			<div className={styles.bio__skills}>{getSkills(bio.skills)}</div>
    </div>
  );
};

export default Bio;
