const Promise = require('bluebird')
const path = require('path')

exports.createPages = ({ graphql, actions }) => {
  const { createPage } = actions

  return new Promise((resolve, reject) => {
    const project = path.resolve('./src/templates/project.js')
    resolve(
      graphql(
        `
          {
            allContentfulProject {
              edges {
                node {
                  title
                  slug
                }
              }
            }
          }
        `
      ).then(result => {
        if (result.errors) {
          console.log(result.errors)
          reject(result.errors)
        }

        const projects = result.data.allContentfulProject.edges
        projects.forEach(proj => {
          createPage({
            path: `/projects/${proj.node.slug}/`,
            component: project,
            context: {
              slug: proj.node.slug,
            },
          })
        })
      })
    )
  })
}
