import os
import re

from github import Github

ACCESS_TOKEN = os.environ.get("GH_TOKEN")
GHE_URI = os.environ.get("GHE_URI")
GHE_TOKEN = os.environ.get("GHE_TOKEN")
if GHE_URI and GHE_TOKEN:
    gh = Github(login_or_token=GHE_TOKEN, base_url=f"https://{GHE_URI}/api/v3")
else:
    gh = Github(ACCESS_TOKEN)


class Repo:
    def __init__(self, url: str):
        self.url: str = url if not url.endswith("/") else url[0:-1]
        self.repo = None
        self.repo_name: str = ""
        self.branch_path: str = ""
        self.default_branch: str = ""
        self.branch_names: list[str] = []
        self.branch: str = ""
        self.path: str = ""
        self.is_main_branch = False
        self.url_is_file = False
        self.__get_github_info()

    def get_github_info(self):
        if not self.repo_name:
            return self.__get_github_info()
        else:
            return self.repo_name, self.branch, self.path

    def __get_github_info(self):
        # regex = r"https://github.com/([^/]+)/([^/]+)/?(tree|blob)?/?([^/]*)"
        regex = "https:\/\/github\.com\/([^\/]+)\/([^\/]+)\/?(tree|blob)?\/?(.+)?"  # noqa:W605 pylint: disable=W1401
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
                self.url_is_file = True
                # return self.repo, self.branch, self.path
            elif not self.branch_path:
                self.is_main_branch = True
                self.branch = self.default_branch
                # return self.repo, self.branch, self.path
            else:
                print("branch and/or path specified, but missing tree or blob specifier in the URL, Not a valid url")
            return self.repo_name, self.branch, self.path
        return None

    def __get_repo_info(self):
        self.repo = gh.get_repo(self.repo_name)
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
            filtered_branches: list[str] = [
                branch_name for branch_name in self.branch_names if branch_name.startswith(branch_candidate)
            ]
            if len(filtered_branches) == 1:
                _, self.branch, self.path = self.branch_path.partition(filtered_branches[0])
                self.path = self.path.removeprefix("/")
                break
            elif len(filtered_branches) == 0:
                print(f"No such branch with name: {branch_candidate}")
                # break
            branch_candidate += "/"

    @staticmethod
    def prepare_destination_dir(dst: str):
        abs_path = os.path.abspath(dst)
        os.makedirs(abs_path, exist_ok=True)
        return abs_path

    def download_contents(self, dst: str = "."):
        # get the GitTree object for the specified directory
        dst_dir = self.prepare_destination_dir(dst=dst)
        tree = self.repo.get_git_tree(sha=self.branch, recursive=True).tree
        for item in tree:
            if self.url_is_file and not item.path == self.path:
                continue
            if item.path.startswith(self.path):
                # download the file or directory
                if item.type == "blob":
                    content = self.repo.get_contents(item.path, ref=self.branch).decoded_content

                    if not self.url_is_file:
                        file_path: str = os.path.join(dst_dir, item.path.replace(self.path, ""))
                    else:
                        file_path: str = os.path.join(dst_dir, self.path.split("/")[-1])

                    with open(file_path, "wb") as file:
                        file.write(content)
                elif item.type == "tree" and item.path != self.path:
                    new_dir: str = os.path.join(dst_dir, item.path.replace(self.path, ""))
                    os.makedirs(new_dir, exist_ok=True)


if __name__ == "__main__":
    print(Repo("https://github.com/PyGithub/PyGithub/tree/dependabot/pip/jinja2-lt-3.2").get_github_info())
    print(Repo("https://github.com/PyGithub/PyGithub/tree/dependabot/pip/jinja2-lt-3.2/doc/examples").get_github_info())
    print(Repo("https://github.com/pedroelir/dir/tree/other/system/system/user/src").get_github_info())
    print(Repo("https://github.com/pedroelir/githubdir/blob/main/gitdown.py").get_github_info())
    print(Repo("https://github.com/pedroelir/dir/tree/other/system/system").get_github_info())
    print(Repo("https://github.com/pedroelir/dir/tree/other/system/system/user/src").get_github_info())
    print(Repo("https://github.com/pedroelir/dir/tree/other/system").get_github_info())
    print(Repo("https://github.com/pedroelir/dir/tree/system").get_github_info())
    print(Repo("https://github.com/pedroelir/dir/tree/main").get_github_info())
    print(Repo("https://github.com/pedroelir/dir").get_github_info())
