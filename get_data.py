import requests
import datetime


GITLAB_URL = "https://dev.funkwhale.audio"
GITLAB_PROJECT_ID = 17


def get_commits(year, token):
    url = "{}/api/v4/projects/{}/repository/commits".format(GITLAB_URL, GITLAB_PROJECT_ID)
    while url:
        response = requests.get(
            url,
            params={
                "since": "{}-01-01T00:00:00Z".format(year),
                "until": "{}-12-31T23:59:59Z".format(year),
            },
            headers={"PRIVATE-TOKEN": token},
        )
        response.raise_for_status()
        yield from response.json()

        if "next" in response.links:
            url = response.links["next"]["url"]
        else:
            url = None


def get_tags(year, token):
    url = "{}/api/v4/projects/{}/repository/tags".format(GITLAB_URL, GITLAB_PROJECT_ID)
    while url:
        response = requests.get(
            url,
            headers={"PRIVATE-TOKEN": token},
        )
        response.raise_for_status()
        for tag in response.json():
            if datetime.datetime.fromisoformat(tag['commit']['created_at']).year == year:
                yield tag

        if "next" in response.links:
            url = response.links["next"]["url"]
        else:
            url = None
