import facebook

class Client:
    def __init__(self, config):
        self.page_id = config.page_id
        self.graph = facebook.GraphAPI(access_token=config.access_token)

    def send(self, message, link=None, dry_run=False):
        """
        Publish a post to the Facebook page.
        :param message: The text message to post.
        :param link: (Optional) A URL to include in the post.
        :param dry_run: (Optional) If True, the post will not be published.
        :return: The response from the Facebook API.
        """
        if dry_run:
            return {"id": "dry_run"}
        
        post_args = {"message": message}
        if link:
            post_args["link"] = link
        return self.graph.put_object(
            parent_object=self.page_id,
            connection_name="feed",
            **post_args
        )