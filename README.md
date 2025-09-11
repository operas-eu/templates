![](./resources/attachments/header.png)

# FAIR-by-Design Methodology - Templates Repository

This repository hosts all templates necessary for the development of FAIR-by-Design learning materials for the requirements of the Skills4EOSC project.
Use these templates together with 

- the [FAIR-by-Design Methodology for Learning Materials Development](https://fair-by-design-methodology.github.io/FAIR-by-Design_Book/).
- the [FAIR-by-Design Methodology Training of Trainers Learning materials](https://fair-by-design-methodology.github.io/FAIR-by-Design_ToT/latest/)

All content is available under CC0 [license](./LICENSE).


## Want to learn how to implement the FAIR-by-Design Methodology?

If you are interested in following the training as a learner:

- take a look at the [FAIR-by-Design Methodology learning content GitBook](https://fair-by-design-methodology.github.io/FAIR-by-Design_ToT/latest/) - based on the content of this repo
- enroll in the corresponding [FAIR-by-Design Methodology course on the Skills4EOSC learning platform](https://learning.skills4eosc.eu/course/view.php?id=19) and try to get the FAIR Instructor badge.


## How to use these templates?

If you want to start developing FAIR-by-Design learning materials based on these templates simply clone this repository.

### Gitlab Pages

This repo contains a `.gitlab-ci.yml` file for automatically deploying the content of this repo to [Gitlab Pages](https://docs.gitlab.com/ee/user/project/pages/).

#### Available workflows

The included `.gitlab-ci.yml` file provides 2 workflows:

##### Push to main branch during development

On each push to the main branch, the CI/CD pipeline will

- automatically synchronise the metadata between `CITATION.cff`, `mkdocs.yml`, `.zenodo.json`, and `linkset.json` and
- build and deploy the MkDocs document to GitLab pages under `/latest/`.

##### Create a release

If you create a [tag](https://docs.gitlab.com/user/project/repository/tags/) in the [Semantic Versioning](https://semver.org/) format `[number].[number].[number]` (e.g. 1.0.0; see the [Fair-by-Design Train of Trainers unit "Zenodo Publishing"](https://fair-by-design-methodology.github.io/FAIR-by-Design_ToT/latest/Stage%205%20%E2%80%93%20Publish/17-Zenodo%20Publishing/17-Zenodo%20Publishing/) for more information about Semantic Versioning), the CI/CD pipeline will

- reserve a DOI on Zenodo,
- synchronise the current date and version number from the tag into the `CITATION.cff`,
- run the above steps from the pipeline that runs on a push to main branch (synchronize metadata and deploy latest version to GitLab pages),
- build and deploy the MkDocs document to GitLab pages under `/<semantic-version-number>/`, and
- populate the Zenodo entry with the metadata from the repo and a snapshot of the current contents of this repository.

#### Setup the GitLab CI/CD pipeline

To setup the CI/CD pipeline, you need to complete the following steps:

- Make sure the [project feaures](https://docs.gitlab.com/ee/user/project/settings/) `CI/CD` and `Pages` are activated in your project (*Settings* > *General* > *Visibility, project features, permissions*).
- Allow the pipeline to push content back to the repository (*Settings* > *CI/CD Settings* > *Job token permissions* > *Additional permissions* > *Allow Git push requests to the repository*).
- Create a [Zenodo Access Token](https://zenodo.org/account/settings/applications/tokens/new/) and save it in GitLab under *Settings* > *CI/CD* > *Variables* > *CI/CD Variables* > *Add variable* with the following properties:
  - Type: Variable (default)
  - Environments: All (default)
  - Visibility: Masked and hidden
  - Flags:
    - Protect variable: No (if you want to increase the security and activate this protection, you need to create a rule that all release tags are marked as [protected tags]())
    - Expand variable reference: No
  - Key: ZENODO_ACCESS_TOKEN
  - Value: `<your-access-token>`
- If you want to use the Zenodo Sandbox for testing, save the access token for the Sandbox as described above, but with the Key `ZENODO_SANDBOX_ACCESS_TOKEN` and create another variable with the key `ZENODO_USE_SANDBOX` and the value `true`.

If the pipelines are still not working, make sure that there is at least [one active runner](https://docs.gitlab.com/ee/ci/runners/runners_scope.html) (navigate to *Settings* > *CI/CD Settings* > *Runners*).

---

May your learning materials always be FAIR!


The Skills4EOSC FAIR-by-Design Methodology Team

