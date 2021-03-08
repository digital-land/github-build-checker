import logging
import os
import sys

from github_checker import GithubChecker
from slack import Slack

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    github_token = os.environ.get("GITHUB_TOKEN", None)
    if not github_token:
        logging.error("no token found in env GITHUB_TOKEN")
        sys.exit(1)

    gc = GithubChecker(github_token, "digital-land")
    failures = gc.get_failing_builds()

    slack_token = os.environ["SLACK_BOT_TOKEN"]
    slack = Slack(slack_token, "#dl-developers")

    if failures:
        slack.notify_failures(failures)
    else:
        slack.notify_happy()
