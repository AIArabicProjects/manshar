import facebook
import requests
from io import BytesIO

class Client:
    def __init__(self, config):
        self.page_id = config.page_id
        self.graph = facebook.GraphAPI(access_token=config.access_token)

    def send(self, message, link=None, image_url=None, dry_run=False):
        """
        Publish a post to the Facebook page.
        :param message: The text message to post.
        :param link: (Optional) A URL to include in the post.
        :param image_url: (Optional) URL of the image to attach.
        :param dry_run: (Optional) If True, the post will not be published.
        :return: The response from the Facebook API.
        """
        if dry_run:
            return {"id": "dry_run"}
        
        try:
            if image_url:
                try:
                    # Download the image with proper headers
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    response = requests.get(image_url, headers=headers)
                    response.raise_for_status()

                    # Create a temporary file-like object
                    image_data = BytesIO(response.content)

                    # Post the photo directly (published) - simpler and more reliable
                    return self.graph.put_photo(
                        image=image_data,
                        album_path=f"{self.page_id}/photos",
                        published=True,
                        message=message
                    )
                except Exception as e:
                    print(f"Error uploading image to Facebook: {str(e)}")
                    # Continue without the image if upload fails

            # Fallback: post without image (text + link)
            post_args = {"message": message}
            if link:
                post_args["link"] = link

            return self.graph.put_object(
                parent_object=self.page_id,
                connection_name="feed",
                **post_args
            )
        except Exception as e:
            print(f"Error posting to Facebook: {str(e)}")
            raise