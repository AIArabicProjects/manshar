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
        self.app_id = data.get("app_id")
        self.app_secret = data.get("app_secret")

class LinkedIn:
    def __init__(self, data):
        self.client_id = data.get("client_id")
        self.client_secret = data.get("client_secret")
        self.access_token = data.get("access_token")
        self.organization_id = data.get("organization_id")

class Telegram:
    def __init__(self, data):
        self.bot_token = data.get("bot_token")
        self.chat_id = data.get("chat_id")

class OpenAI:
    def __init__(self, data):
        self.api_key = data.get("api_key")
        self.model = data.get("model", "gpt-3.5-turbo")
        self.max_tokens = data.get("max_tokens", 1000)
        self.temperature = data.get("temperature", 0.7)

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
telegram = Telegram(_config.get("telegram", {}))
openai = OpenAI(_config.get("openai", {}))
rss = RSS(_config.get("rss", {}))
app = App(_config.get("app", {}))
