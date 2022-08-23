GithubRepoManager
------------------------------

The Github web app doesn't support batch changes to repos, like making
several repos private, changing names, etc. So this simple script uses PyGithub
to do this. A use case is for clean-up in a Github organization at the end of
an academic semester. Links to relevant documentation are included so you can
modify/expand to fit your specific use case.

## Dependencies
* PyGithub: `pip install PyGithub`
* A Github personal access token with the repo and delete_repo scopes