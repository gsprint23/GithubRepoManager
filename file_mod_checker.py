##################################################################################
# Author: Gina Sprint
# Date: 11/21/23
# Description: Some files in a repo shouldn't be changed, or at least changes should
#   be tracked. So this simple script uses PyGithub to check modifications to certain
#   files in the commit history. A use case is assignments used with Github Classroom.
#   Students shouldn't be changing the classroom.yml and autograding.json files, and
#   in some cases they shouldn't be changing provided unit tests either. With this
#   code, you can check for that. Links to relevant documentation are included so you can
#   modify/expand to fit your specific use case. 
# Sources:
#   - Creating a personal Github access token: https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token
#   - PyGithub: https://pypi.org/project/PyGithub/
##################################################################################

import os
from datetime import datetime
import base64

from github import Github # pip install PyGithub

ACCESS_KEY = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN") # add as environment variable so it doesn't end up on Github :)
# if you don't have one or yours is expired, make a new one here: https://github.com/settings/tokens
# add repo scope and optionally delete_repo scope if plan to delete repos (like clean up of student PAs)

# NOTE: enter parameters here
ORGANIZATION_NAME = "GonzagaCPSC122" 
ASSIGNMENT_NAME = "PA3"
MIN_CREATION_DATETIME = datetime.strptime("2023-01-01", "%Y-%m-%d") # in case use same org for mult semesters
FILES_TO_TRACK = [".github/workflows/classroom.yml", ".github/classroom/autograding.json", "test/Test.cpp"]

if __name__ == "__main__":
    assignment_prefix = ASSIGNMENT_NAME.lower() + "-"
    assignment_starter_code_repo_name = os.path.join(ORGANIZATION_NAME, f"{ASSIGNMENT_NAME}StarterCode")

    # using a Github personal access token
    g = Github(ACCESS_KEY) 
    # pre-cache the correct versions of the files we are tracking by fetching their contents from starter code repo
    starter_repo_file_contents = {}
    starter_repo = g.get_repo(assignment_starter_code_repo_name)
    for filename in FILES_TO_TRACK:
        content_file = starter_repo.get_contents(filename)
        decoded_content = base64.b64decode(content_file.content).decode('utf-8')
        starter_repo_file_contents[filename] = decoded_content
    # where we will store current versions of students' files we are tracking that don't match starter code
    flags = {}
    # go through each repo and see if it matches the assignment we are looking for
    # get_organization(): https://pygithub.readthedocs.io/en/latest/github_objects/AuthenticatedUser.html?highlight=get_organization#github.AuthenticatedUser.AuthenticatedUser.get_organization_membership
    # get_repos(): # https://pygithub.readthedocs.io/en/latest/github_objects/Organization.html?highlight=get_repos#github.Organization.Organization.get_repos
    for repo in g.get_organization(ORGANIZATION_NAME).get_repos(type="private", sort="full_name"): # NOTE: can set type="public" or type="private"
        # NOTE: set repo name filters for what you want to edit/delete here    
        if (repo.name.startswith(assignment_prefix) and repo.created_at > MIN_CREATION_DATETIME):
            # https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html#github.Repository.Repository.get_commits
            commits = repo.get_commits()
            print(f"repo name: {repo.name} # of commits: {commits.totalCount}")
            final_files_to_check = set() # set so we don't get dups
            # go through each commit and see if it includes a modification to one of the files we are tracking
            for commit in commits:
                try:
                    login = commit.author.login
                except:
                    # commit.author can be None if the author's account was deleted
                    # commit.author.login can be  404 {"message": "Not Found"... if login="invalid-email-address"
                    login = "unknown"
                if login != "github-classroom[bot]": # don't count the initial commit when repo was created
                    # https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html#github.Repository.Repository.get_commit
                    detailed_commit = repo.get_commit(commit.sha)
                    for file in detailed_commit.files:
                        if file.filename in starter_repo_file_contents.keys():
                            # add this file to a list of files that have been modified that shouldn't have been
                            # we will check that the current version of these files on Github match the starter code
                            # meaning they were restored back to the "original" state
                            print(f"\tfile modified: {file.filename} message: {commit.commit.message}") # sha: {commit.sha}")
                            # get current version of file contents, not this specific commit's version
                            final_files_to_check.add(file.filename)
            # check the student's current versions with starter code's versions, flagging any that don't
            for file_to_check in final_files_to_check:
                # https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html#github.Repository.Repository.get_contents
                content_file = repo.get_contents(file_to_check)
                decoded_content = base64.b64decode(content_file.content).decode('utf-8')
                # print("orig:", starter_repo_file_contents[file.filename])
                # print("student:", decoded_content)
                same = decoded_content == starter_repo_file_contents[file_to_check]
                print(f"\tfinal version of {file_to_check} matches starter code: {same}")
                if not same:
                    if repo.name in flags.keys():
                        flags[repo.name].append(file_to_check)
                    else:
                        flags[repo.name] = [file_to_check]

    # write out final flags for manual inspection
    print("\n\n***manually inspect the following repos and files***")
    for repo_name, modified_files in flags.items():
        print(f"{repo_name}: {modified_files}")