from slack_sdk import WebClient


class Slack:

    HAPPY_TEMPLATE = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "GitBot is happy, all builds are passing! :green_heart:",
        },
    }

    FAILURE_HEADER = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "GitBot is sad, some builds needs fixing. :cry:",
        },
    }

    def build_failure_block(self, repo, workflow, url):
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"<{url}|{repo} - {workflow}> :x:",
            },
        }

    def __init__(self, token, channel):
        self.channel = channel
        self.client = WebClient(token=token)

    def _post(self, blocks, text):
        print(f"sending to channel {self.channel}")
        self.client.chat_postMessage(channel=self.channel, blocks=blocks, text=text)

    def notify_happy(self):
        self._post(
            blocks=[self.HAPPY_TEMPLATE],
            text="All builds are passing",
        )

    def notify_failures(self, failures):
        blocks = [self.FAILURE_HEADER]
        for failure in failures:
            blocks.append(self.build_failure_block(**failure))

        self._post(blocks=blocks, text="Build failures detected")
