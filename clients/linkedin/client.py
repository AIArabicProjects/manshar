import requests

class Client:
    def __init__(self, config):
        self.access_token = config.access_token
        self.organization_id = config.organization_id

    def send(self, message, link=None):
        """
        Publish a post to the LinkedIn organization page.
        :param message: The text message to post.
        :param link: (Optional) A URL to include in the post.
        :return: The response from the LinkedIn API.
        """
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json"
        }
        post_data = {
            "author": f"urn:li:organization:{self.organization_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": message
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        if link:
            post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "ARTICLE"
            post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
                {
                    "status": "READY",
                    "originalUrl": link
                }
            ]
        response = requests.post(url, headers=headers, json=post_data)
        response.raise_for_status()
        return response.json()