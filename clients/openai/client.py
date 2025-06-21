import openai
import re
import lib.article_extractor


class Client:
    def __init__(self, config):
        self.api_key = config.api_key
        self.model = config.model or "gpt-3.5-turbo"
        self.client = openai.OpenAI(api_key=self.api_key)



    def summarize_article(self, url, max_length=280, include_hashtags=True, dry_run=False):
        """
        Summarize an article from URL and create an engaging social media post
        
        :param url: URL of the article to summarize
        :param max_length: Maximum length of the generated post
        :param include_hashtags: Whether to include relevant hashtags
        :param dry_run: If True, return mock response
        :return: Dictionary with summary and post content
        """
        if dry_run:
            return {
                "summary": "This is a dry run summary of the article",
                "social_post": f"🔥 Amazing insights in this article! Check it out: {url} #TechNews #AI",
                "hashtags": ["#TechNews", "#AI", "#Innovation"]
            }
        
        try:
            # Extract article content
            article_data = lib.article_extractor.extract_article_content(url)
            
            # Create prompt for summarization
            hashtag_instruction = "Include 2-3 relevant Arabic hashtags." if include_hashtags else "Do not include hashtags."
            
            prompt = f"""
            Please create an engaging Arabic social media post based on this article:
            
            Title: {article_data['title']}
            Content: {article_data['content']}
            Article URL: {url}
            
            Requirements:
            - Write in Arabic
            - Keep it under {max_length} characters
            - Make it engaging and compelling
            - Include the article link at the end (just the URL, not markdown format)
            - {hashtag_instruction}
            - Use emojis strategically (3-6 relevant emojis)
            - Focus on the key insights or benefits
            - Start with an engaging hook (اكتشف، تعلم، شاهد، etc.)
            - End with a clear call to action
            
            Format the response as a ready-to-post social media message with hashtags at the end.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a social media expert who creates engaging Arabic posts that drive clicks and engagement."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            social_post = response.choices[0].message.content.strip()
            
            # Extract hashtags from the post
            hashtags = re.findall(r'#\w+', social_post)
            
            return {
                "summary": article_data['content'][:500] + "..." if len(article_data['content']) > 500 else article_data['content'],
                "social_post": social_post,
                "hashtags": hashtags,
                "title": article_data['title']
            }
            
        except Exception as e:
            raise Exception(f"Failed to summarize article: {str(e)}")

    def extract_bite_sized_content(self, url, num_posts=3, post_length=200, dry_run=False):
        """
        Extract bite-sized information from an article to create multiple engaging posts
        
        :param url: URL of the article
        :param num_posts: Number of bite-sized posts to generate
        :param post_length: Maximum length for each post
        :param dry_run: If True, return mock response
        :return: List of bite-sized posts
        """
        if dry_run:
            return [
                {
                    "post": "💡 نصيحة رقم 1: هذه معلومة مفيدة من المقال",
                    "hashtags": ["#نصائح", "#تقنية"],
                    "type": "tip"
                },
                {
                    "post": "📊 إحصائية مثيرة: 90% من الخبراء يوافقون على هذا",
                    "hashtags": ["#إحصائيات", "#معلومات"],
                    "type": "statistic"
                },
                {
                    "post": "🔑 الخلاصة: أهم ما يجب معرفته من المقال",
                    "hashtags": ["#خلاصة", "#تعلم"],
                    "type": "key_takeaway"
                }
            ]
        
        try:
            # Extract article content
            article_data = lib.article_extractor.extract_article_content(url)
            
            prompt = f"""
            Based on this Arabic article, create {num_posts} bite-sized social media posts that will increase engagement:
            
            Title: {article_data['title']}
            Content: {article_data['content']}
            
            For each post:
            - Write in Arabic
            - Keep under {post_length} characters
            - Make it engaging and shareable
            - Include relevant emojis
            - Add 2-3 relevant Arabic hashtags
            - Focus on different aspects: tips, statistics, key insights, quotes, or surprising facts
            
            Format each post as:
            POST 1:
            [content with emojis and hashtags]
            TYPE: [tip/statistic/insight/quote/fact]
            
            POST 2:
            [content with emojis and hashtags]
            TYPE: [tip/statistic/insight/quote/fact]
            
            And so on...
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a social media expert who creates viral Arabic content that maximizes engagement."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.8
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse the response to extract individual posts
            posts = []
            post_blocks = re.split(r'POST \d+:', content)[1:]  # Skip first empty element
            
            for block in post_blocks:
                lines = block.strip().split('\n')
                post_content = ""
                post_type = "general"
                
                for line in lines:
                    if line.startswith('TYPE:'):
                        post_type = line.replace('TYPE:', '').strip().lower()
                    elif line.strip() and not line.startswith('TYPE:'):
                        post_content += line.strip() + " "
                
                post_content = post_content.strip()
                if post_content:
                    hashtags = re.findall(r'#\w+', post_content)
                    posts.append({
                        "post": post_content,
                        "hashtags": hashtags,
                        "type": post_type
                    })
            
            return posts[:num_posts]  # Ensure we return exactly the requested number
            
        except Exception as e:
            raise Exception(f"Failed to extract bite-sized content: {str(e)}")

    def generate_engaging_post(self, text, platform="general", max_length=280, dry_run=False):
        """
        Generate an engaging social media post from any text
        
        :param text: Original text to transform
        :param platform: Target platform (twitter, facebook, linkedin, instagram, general)
        :param max_length: Maximum length of the post
        :param dry_run: If True, return mock response
        :return: Engaging social media post
        """
        if dry_run:
            return {
                "post": f"🚀 منشور تجريبي جذاب: {text[:50]}... #تجربة",
                "hashtags": ["#تجربة"],
                "engagement_score": 8.5
            }
        
        try:
            platform_guidelines = {
                "twitter": "engaging and informative, can be longer with detailed insights, use trending hashtags",
                "facebook": "conversational, story-telling, community-focused, encourage discussion",
                "linkedin": "professional, insightful, industry-focused, thought leadership tone",
                "instagram": "visual-first, lifestyle-oriented, with many relevant hashtags, storytelling",
                "general": "versatile and adaptable to multiple platforms"
            }
            
            guideline = platform_guidelines.get(platform, platform_guidelines["general"])
            
            prompt = f"""
            Transform this text into an engaging Arabic social media post for {platform}:
            
            Original text: {text}
            
            Requirements:
            - Write in Arabic
            - Make it {guideline}
            - Keep under {max_length} characters
            - Include relevant emojis
            - Add appropriate Arabic hashtags
            - Make it click-worthy and shareable
            - Focus on emotional engagement
            
            Return just the final post, optimized for maximum engagement.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are a social media expert specializing in Arabic content that goes viral and drives engagement on {platform}."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            post = response.choices[0].message.content.strip()
            hashtags = re.findall(r'#\w+', post)
            
            # Simple engagement score based on content features
            engagement_score = self._calculate_engagement_score(post)
            
            return {
                "post": post,
                "hashtags": hashtags,
                "engagement_score": engagement_score,
                "platform": platform
            }
            
        except Exception as e:
            raise Exception(f"Failed to generate engaging post: {str(e)}")

    def _calculate_engagement_score(self, post):
        """
        Calculate a simple engagement score based on post features
        """
        score = 5.0  # Base score
        
        # Emoji bonus
        emoji_count = len(re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', post))
        score += min(emoji_count * 0.5, 2.0)
        
        # Hashtag bonus
        hashtag_count = len(re.findall(r'#\w+', post))
        score += min(hashtag_count * 0.3, 1.5)
        
        # Question bonus (engagement trigger)
        if '؟' in post or '?' in post:
            score += 1.0
        
        # Call to action words
        cta_words = ['شارك', 'علق', 'اكتشف', 'تعلم', 'احصل', 'جرب']
        for word in cta_words:
            if word in post:
                score += 0.5
                break
        
        # Length penalty for very long posts
        if len(post) > 280:
            score -= 1.0
        
        return min(max(score, 1.0), 10.0)  # Keep score between 1-10 