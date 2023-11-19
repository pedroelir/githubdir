# import os

# from github import Github
import json
import yaml
import os
from repo import Repo

# replace with your GitHub access token
# ACCESS_TOKEN = os.environ.get("GH_TOKEN")

# specify the repository and the directory to download
# rep = Repo("https://github.com/pedroelir/dir/tree/system")
# rep = Repo("https://github.com/pedroelir/dir/tree/system/system")
# rep = Repo("https://github.com/pedroelir/dir/system/system")  # Mising tree or blob keyword (not exissting)
# rep = Repo("https://github.com/pedroelir/dir/tree/system/system/")
# rep = Repo("https://github.com/pedroelir/dir/blob/system/system/")  # wrong existing (blob instead of tree)
# rep = Repo("https://github.com/pedroelir/dir/fejk/system/system/")  # suppsed not existence (fejk instad of tree)
# rep = Repo("https://github.com/pedroelir/dir/tree/fake/url/not/exist")  # not existing
# rep = Repo("https://github.com/pedroelir/dir")
# rep = Repo("https://github.com/pedroelir/dir/")
# rep = Repo("https://github.com/pedroelir/dir/blob/other/user/system/user/src/file.txt")
# rep = Repo("https://github.com/pedroelir/dir/blob/main/.gitignore")
# rep.download_contents("example2\example")


def check_yaml_file(yaml_file_name, expected_attr1="attr1", expected_attr2="attr2"):
    if not os.path.isfile(yaml_file_name):
        return False

    with open(yaml_file_name, encoding="UTF-8") as fp:
        first_key_level = "FirstKey"
        second_key_level = "SecondKey"
        key_attribute_1 = "attr1"
        keyattribute_2 = "attr2"

        try:
            loaded_yaml: dict[str, dict[str, dict[str, str]]] = yaml.safe_load(fp)
            attr1 = loaded_yaml.get(first_key_level).get(second_key_level).get(key_attribute_1)
            attr2 = loaded_yaml.get(first_key_level).get(second_key_level).get(keyattribute_2)
        except AttributeError:
            return False
        if any([attr1 is None, attr2 is None]):
            return False
        if attr1.casefold() != expected_attr1.casefold():
            return False
        if attr2.casefold() != expected_attr2.casefold():
            return False

    return True


if __name__ == "__main__":
    with open("repos.json", encoding="UTF-8") as fp:
        repos: list[str] = json.load(fp=fp)

    for repo in repos:
        folder_name = repo.split("/")[-1]
        rep = Repo(repo)
        # rep.download_contents(folder_name)
        yaml_file_name = os.path.join(folder_name, "Myyamlfile.yaml")
        if not check_yaml_file(yaml_file_name=yaml_file_name):
            print(folder_name)
