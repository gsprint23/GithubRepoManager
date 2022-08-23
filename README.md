# GithubRepoManager

The Github web app doesn't support batch changes to repos, like making
several repos private, changing names, etc. So this simple script uses PyGithub
to do this. A use case is for clean-up in a Github organization at the end of
an academic semester.

## Dependencies
* [PyGithub](https://pygithub.readthedocs.io/en/latest): `pip install PyGithub`
    * `get_organization()`: https://pygithub.readthedocs.io/en/latest/github_objects/AuthenticatedUser.html?highlight=get_organization#github.AuthenticatedUser.AuthenticatedUser.get_organization_membership
    * `get_repos()`: https://pygithub.readthedocs.io/en/latest/github_objects/Organization.html?highlight=get_repos#github.Organization.Organization.get_repos
* A Github personal access token with the repo and delete_repo scopes