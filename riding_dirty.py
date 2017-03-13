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
    repo = Repo(path)
    if repo.bare:
        return
    if repo.is_dirty():
        print("{} is dirty (has uncommitted changes)".format(path))
    if len(repo.untracked_files) != 0:
        print("{} has untracked files".format(path))

    # Foreach local branch, foreach remote:
    #  Check if the remote has a copy of this branch
    #  If so, check if its commit matches our local one.
    for head in repo.heads:
        printv("Checking checkout {}".format(head))
        for remote in repo.remotes:
            printv("  Checking remote {}".format(remote))
            if head.name in remote.refs:
                printv("    Matched {}".format(head.name))
                if head.commit == remote.refs[head.name].commit:
                    printv("    Remote {} is up to date with branch {}"
                           "".format(remote, head))
                else:
                    print("    Remote {} branch {} doesn't match local".format(
                        remote, head))
            else:
                print("  Remote {} doesn't have branch {}".format(remote,
                                                                  head))


if __name__ == "__main__":
    verbose = False
    if len(sys.argv) == 2:
        if sys.argv[1] in ("-v", "-V", "--verbose"):
            verbose = True

    check_repo("/home/dwt27/git/riding_dirty")
