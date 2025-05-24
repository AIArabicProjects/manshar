import yaml

class X:
    def __init__(self, data):
        self.api_key = data.get("api_key")
        self.api_secret = data.get("api_secret")
        self.access_token = data.get("access_token")
        self.access_token_secret = data.get("access_token_secret")
        self.bearer_token = data.get("bearer_token")

class Facebook:
    def __init__(self, data):
        self.access_token = data.get("access_token")
        self.page_id = data.get("page_id")

class LinkedIn:
    def __init__(self, data):
        self.client_id = data.get("client_id")
        self.client_secret = data.get("client_secret")
        self.access_token = data.get("access_token")
        self.organization_id = data.get("organization_id")

class RSS:
    def __init__(self, data):
        self.feed_url = data.get("feed_url")

class App:
    def __init__(self, data):
        self.check_interval_minutes = data.get("check_interval_minutes")
        self.log_level = data.get("log_level")

# Load YAML config
with open("config.yaml", "r") as f:
    _config = yaml.safe_load(f)

# Global config objects
x = X(_config.get("x", {}))
facebook = Facebook(_config.get("facebook", {}))
linkedin = LinkedIn(_config.get("linkedin", {}))
rss = RSS(_config.get("rss", {}))
app = App(_config.get("app", {}))
