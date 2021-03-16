import logging

from github import Github

logger = logging.getLogger(__name__)


class GithubChecker:
    def __init__(self, token, org):
        self.g = Github(token)
        self.org = org

    def get_failing_builds(self):
        failures = []
        for repo in self.g.get_organization(self.org).get_repos():
            if repo.name == "github-build-checker":
                continue

            if repo.archived:
                logger.info("skipping %s: archived", repo.name)
                continue

            workflows = repo.get_workflows()
            if workflows.totalCount == 0:
                logger.info("skipping %s: no workflows", repo.name)
                continue

            logger.info(f"{repo.name}: {repo.get_workflows().totalCount} workflows")

            for workflow in workflows:
                if workflow.state != "active":
                    continue

                for run in workflow.get_runs():
                    if run.status != "completed":
                        continue

                    if run.head_branch != repo.default_branch:
                        continue

                    if run.conclusion == "success":
                        break

                    failure = {"repo": repo.name, "workflow": workflow.name, "url": run.html_url}
                    failures.append(failure)
                    break

        return failures
