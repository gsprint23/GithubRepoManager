# GithubRepoManager
A little collection of scripts to help manage Github repos, particularly ones in an organization used with Github Classroom.

* `org_repo_cleaner.py`: The Github web app doesn't support batch changes to repos, like making
several repos private, changing names, etc. So this simple script uses PyGithub
to do this. A use case is for clean-up in a Github organization at the end of
an academic semester.
* `file_mod_checker.py`: When using Github Classroom for programming assignments with unit tests/autograding, 
students can modifiy important files like `classroom.yml` and `autograding.json`. This simple script checks these
files (and any other ones you want to track) in student repos and flags them if they have been modified.

## Dependencies
* [PyGithub](https://pygithub.readthedocs.io/en/latest): `pip install PyGithub`
    * `get_organization()`: https://pygithub.readthedocs.io/en/latest/github_objects/AuthenticatedUser.html?highlight=get_organization#github.AuthenticatedUser.AuthenticatedUser.get_organization_membership
    * `get_repos()`: https://pygithub.readthedocs.io/en/latest/github_objects/Organization.html?highlight=get_repos#github.Organization.Organization.get_repos
* A Github personal access token with the repo and delete_repo scopes