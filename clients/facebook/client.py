import facebook

class Client:
    def __init__(self, config):
        self.page_id = config.page_id
        self.graph = facebook.GraphAPI(access_token=config.access_token)

    def send(self, message, link=None):
        """
        Publish a post to the Facebook page.
        :param message: The text message to post.
        :param link: (Optional) A URL to include in the post.
        :return: The response from the Facebook API.
        """
        post_args = {"message": message}
        if link:
            post_args["link"] = link
        return self.graph.put_object(
            parent_object=self.page_id,
            connection_name="feed",
            **post_args
        )