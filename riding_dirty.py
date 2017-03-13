#!/home/dwt27/git/riding_dirty/venv/bin/python

from git import Repo
import argparse


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
    parser = argparse.ArgumentParser(description="""
Check one or many git repositories for untracked files, uncommitted changes, or
commits not pushed to remotes""")
    parser.add_argument("path", type=str, nargs="+", help="""
The path of each repository to check""")
    parser.add_argument("-v", "--verbose", action="store_true", help="""
Verbose output: print everything we check, every step we take.""")
    args = parser.parse_args()
    paths = args.path
    verbose = args.verbose

    for path in paths:
        check_repo(path)
