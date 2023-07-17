import logging
import os
import re

from github_release_downloader import GitHubRepo, check_and_download_updates
from semantic_version import SimpleSpec


def main():
    logging.basicConfig(
        format="[%(asctime)s][%(levelname)s] %(message)s",
        datefmt='%H:%M:%S',
        level=logging.INFO
    )
    check_and_download_updates(
        GitHubRepo("SemperSolus0x3d", "WinJobster.cpp", os.environ.get("GITHUB_TOKEN")),
        SimpleSpec("~3"),
        assets_mask=re.compile(".*\\.dll"),
    )


if __name__ == '__main__':
    main()
