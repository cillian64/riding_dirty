#!/home/dwt27/git/riding_dirty/venv/bin/python

from git import Repo
import sys


def printv(string):
    if verbose:
        print(string)


def check_repo(path):
    """
    Check if the repository has any dirty changes or commits which have not
    been pushed to any of its remotes.
    """
    repo_name = path.split("/")[-1]
    printv("Repo {}".format(repo_name))
    repo = Repo(path)
    if repo.bare:
        return
    if repo.is_dirty():
        print("Repo {} is dirty (has uncommitted changes)".format(repo_name))
    if len(repo.untracked_files) != 0:
        print("Repo {} has untracked files".format(repo_name))

    # Foreach local branch, foreach remote:
    #  Check if the remote has a copy of this branch
    #  If so, check if its commit matches our local one.
    for remote in repo.remotes:
        printv("Repo {} remote {}".format(repo_name, remote))
        for branch in repo.heads:
            if branch.name in remote.refs:
                printv("Repo {} remote {} branch {}".format(repo_name, remote,
                                                            branch))
                if branch.commit == remote.refs[branch.name].commit:
                    printv("Repo {} remote {} branch {}: Up to date".format(
                        repo_name, remote, branch))
                else:
                    print("Repo {} remote {} branch {}: Mismatch!".format(
                        repo_name, remote, branch))
            else:
                print("Repo {} remote {} branch {}: Remote doesn't have branch"
                      "".format(repo_name, remote, branch))


if __name__ == "__main__":
    verbose = False
    if len(sys.argv) == 2:
        if sys.argv[1] in ("-v", "-V", "--verbose"):
            verbose = True

    check_repo("/home/dwt27/git/riding_dirty")
