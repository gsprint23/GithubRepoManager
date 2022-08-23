##################################################################################
# Author: Gina Sprint
# Date: 8/11/21
# Description: The Github web app doesn't support batch changes to repos, like making
#   several repos private, changing names, etc. So this simple script uses PyGithub
#   to do this. A use case is for clean-up in a Github organization at the end of
#   an academic semester. Links to relevant documentation are included so you can
#   modify/expand to fit your specific use case. 
# Sources:
#   - Creating a personal Github access token: https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token
#   - PyGithub: https://pypi.org/project/PyGithub/
##################################################################################

import os

from github import Github # pip install PyGithub

ACCESS_KEY = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN") # add as environment variable so it doesn't end up on Github :)
# if you don't have one or yours is expired, make a new one here: https://github.com/settings/tokens
# add repo scope and optionally delete_repo scope if plan to delete repos (like clean up of student PAs)

if __name__ == "__main__":
    # NOTE: enter organization name here
    organization_name = "GonzagaCPSC222" 
    # using a Github personal access token
    g = Github(ACCESS_KEY) 

    counter = 0 # sanity check to make sure you've applied the right filters before making any regrettable changes
    # get_organization(): https://pygithub.readthedocs.io/en/latest/github_objects/AuthenticatedUser.html?highlight=get_organization#github.AuthenticatedUser.AuthenticatedUser.get_organization_membership
    # get_repos(): # https://pygithub.readthedocs.io/en/latest/github_objects/Organization.html?highlight=get_repos#github.Organization.Organization.get_repos
    for repo in g.get_organization(organization_name).get_repos(type="public", sort="full_name"): # NOTE: can set type="private"
        print(repo.name, repo.owner)
        # NOTE: set repo name filters for what you want to edit/delete here
        # if ("Fun" in repo.name or "Exam" in repo.name) and not repo.name.startswith("F20") and not repo.name.startswith("F21"):
        if (repo.name.startswith("U") or repo.name.startswith("PAs") or repo.name.startswith("DAs")): # and not repo.name.startswith("S21"):
            counter += 1 # to make sure this matches Github organization page count for filter "Public" at end of semester
            print("Match#", counter, repo.name) # https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html#repository

            # edit capabilities: https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html#github.Repository.Repository.edit
            # NOTE: uncomment this when you've filtered down to the repos you want to edit!!
            # repo.edit(private=True) 
            # repo.edit(name="S22-" + repo.name) 
            # NOTE: same here on uncommenting to delete, but be careful with this one as there is no confirmation of are you sure you want to delete? this is comment is it!!
            # if you get github.GithubException.GithubException: 403 "Must have admin rights to Repository.", you need to set the delete_repository scope on your personal access token
            # repo.delete() # https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html?highlight=repository%20delete#github.Repository.Repository.delete