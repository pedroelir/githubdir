import os
import re

from github import Github

ACCESS_TOKEN = os.environ.get("GH_TOKEN")

gith = Github(ACCESS_TOKEN)


class Repo:
    def __init__(self, url: str):
        self.url: str = url
        self.repo = None
        self.repo_name: str = ""
        self.branch_path: str = ""
        self.default_branch: str = ""
        self.branch_names: list[str] = []
        self.branch: str = ""
        self.path: str = ""
        self.is_main_branch = False
        self.__get_github_info()

    def get_github_info(self):
        if not self.repo_name:
            return self.__get_github_info()
        else:
            return self.repo_name, self.branch, self.path

    def __get_github_info(self):
        # regex = r"https://github.com/([^/]+)/([^/]+)/?(tree|blob)?/?([^/]*)"
        regex = "https:\/\/github\.com\/([^\/]+)\/([^\/]+)\/?(tree|blob)?\/?(.+)?"  # noqa:W605
        match = re.match(regex, self.url)
        if match:
            self.repo_name = match.group(1) + "/" + match.group(2)
            self.branch_path = match.group(4)
            self.__get_repo_info()
            if match.group(3) == "tree":
                self.__split_branch_path()
                self.path = self.path + "/" if self.path != "" else self.path
                # return self.repo, self.branch, self.path
            elif match.group(3) == "blob":
                self.__split_branch_path()
                # return self.repo, self.branch, self.path
            else:
                self.is_main_branch = True
                self.branch = self.default_branch
                # return self.repo, self.branch, self.path
            return self.repo_name, self.branch, self.path
        return None

    def __get_repo_info(self):
        self.repo = gith.get_repo(self.repo_name)
        self.default_branch = self.repo.default_branch
        branches = list(self.repo.get_branches())
        self.branch_names: list[str] = [branch.name for branch in branches]

    def __split_branch_path(self):
        if not self.branch_path:
            return
        branch_path_elements: list[str] = self.branch_path.split("/")
        branch_candidate: str = ""
        for path_element in branch_path_elements:
            branch_candidate += path_element
            filtered_branches = list(
                filter(lambda branch_name: branch_name.startswith(branch_candidate), self.branch_names)
            )
            if len(filtered_branches) == 1:
                _, self.branch, self.path = self.branch_path.partition(filtered_branches[0])
                self.path = self.path.removeprefix("/")
                break
            elif len(filtered_branches) == 0:
                print(f"No such branch with name: {branch_candidate}")
                # break
            branch_candidate += "/"


def extract_github_info(link):
    # regex = r"https://github.com/([^/]+)/([^/]+)/?(tree|blob)?/?([^/]*)"
    regex = "https:\/\/github\.com\/([^\/]+)\/([^\/]+)\/?(tree|blob)?\/?(.+)?"  # noqa:W605
    match = re.match(regex, link)
    if match:
        repo_name = match.group(1) + "/" + match.group(2)
        branch_path = match.group(4)
        if match.group(3) == "tree":
            branch_name, _, dir_path = branch_path.partition("/")
            return repo_name, branch_name, dir_path + "/"
        elif match.group(3) == "blob":
            return repo_name, branch_path, ""
    return None


if __name__ == "__main__":
    # print(Repo("https://github.com/PyGithub/PyGithub/tree/dependabot/pip/jinja2-lt-3.2").get_github_info())
    print(Repo("https://github.com/PyGithub/PyGithub/tree/dependabot/pip/jinja2-lt-3.2/doc/examples").get_github_info())
    print(Repo("https://github.com/pedroelir/dir/tree/other/system/system/user/src").get_github_info())
    print(Repo("https://github.com/pedroelir/githubdir/blob/main/gitdown.py").get_github_info())
    print(Repo("https://github.com/pedroelir/dir/tree/other/system/system").get_github_info())
    print(Repo("https://github.com/pedroelir/dir/tree/other/system/system/user/src").get_github_info())
    print(Repo("https://github.com/pedroelir/dir/tree/other/system").get_github_info())
    print(Repo("https://github.com/pedroelir/dir/tree/system").get_github_info())
    print(Repo("https://github.com/pedroelir/dir/tree/main").get_github_info())
    print(Repo("https://github.com/pedroelir/dir").get_github_info())
    # print(get_github_info("https://github.com/PyGithub/PyGithub/tree/dependabot/pip/jinja2-lt-3.2/doc/examples"))
