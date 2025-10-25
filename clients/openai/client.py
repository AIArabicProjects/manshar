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

    def generate_daily_posts(self, url, num_posts=5, dry_run=False):
        """
        Generate various types of daily social media posts from an article
        Focus on informative, bite-sized, and funny content
        
        :param url: URL of the article
        :param num_posts: Number of posts to generate
        :param dry_run: If True, still generate real posts but mark as dry run
        :return: List of diverse posts (tips, facts, quotes, definitions, etc.)
        """
        # Even in dry run, we want to test the real generation for quality
        # The dry_run flag is handled at the posting level, not generation level
        
        try:
            # Extract article content
            article_data = lib.article_extractor.extract_article_content(url)
            
            # First, let's extract key information and validate content quality
            content_summary = self._analyze_article_content(article_data['content'], article_data['title'])
            
            prompt = f"""
            أنت خبير في إنشاء محتوى عربي جذاب لوسائل التواصل الاجتماعي. اقرأ هذا المقال بعناية وأنشئ {num_posts} منشورات متنوعة ودقيقة:

            عنوان المقال: {article_data['title']}
            
            محتوى المقال: {article_data['content'][:3000]}
            
            تحليل المحتوى: {content_summary}
            
            مطلوب إنشاء منشورات من الأنواع التالية (استخدم المعلومات الفعلية من المقال فقط):
            
            1. "هل تعلم؟" - معلومة مثيرة أو إحصائية حقيقية من المقال
            2. "تعريف اليوم" - شرح مصطلح تقني مذكور فعلياً في المقال
            3. "نصيحة سريعة" - نصيحة عملية مستخرجة من المقال
            4. "اقتباس ملهم" - جملة أو فكرة ملهمة من النص الأصلي
            5. "حقيقة مدهشة" - معلومة مثيرة مذكورة في المقال
            
            شروط مهمة:
            ✅ استخدم المعلومات الموجودة في المقال فقط - لا تختلق معلومات
            ✅ تأكد من دقة الحقائق والأرقام المذكورة
            ✅ اكتب بالعربية الفصحى البسيطة
            ✅ كل منشور 120-180 حرف (بدون الرابط)
            ✅ استخدم 2-3 إيموجي مناسبة فقط
            ✅ أضف 2-3 هاشتاغات عربية ذات صلة
            ✅ اجعل كل منشور مفيد ومثير للاهتمام
            ✅ اربط المعلومة بالحياة اليومية عند الإمكان
            
            صيغة الإجابة:
            POST 1:
            [نوع المنشور]: [المحتوى مع الإيموجي والهاشتاغات]
            TYPE: [did_you_know/definition/quick_tip/inspiring_quote/amazing_fact]
            
            POST 2:
            [نوع المنشور]: [المحتوى مع الإيموجي والهاشتاغات]
            TYPE: [النوع]
            
            مثال:
            POST 1:
            هل تعلم؟ الذكاء الاصطناعي يمكنه تحليل 10000 صورة في الثانية الواحدة! 🤖⚡ هذا ما يساعد الأطباء في تشخيص الأمراض بسرعة #ذكاء_اصطناعي #تقنية #طب
            TYPE: did_you_know
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": """أنت خبير في إنشاء محتوى عربي دقيق وجذاب لوسائل التواصل الاجتماعي. 

مبادئك الأساسية:
1. الدقة أولاً - لا تختلق معلومات أبداً
2. استخدم المعلومات الموجودة في المقال فقط
3. تحقق من صحة الأرقام والإحصائيات
4. اكتب بأسلوب جذاب ولكن احترافي
5. اربط المعلومة بالواقع العملي
6. استخدم اللغة العربية الواضحة والبسيطة

تذكر: الهدف هو تقديم قيمة حقيقية للقارئ من خلال معلومات دقيقة ومفيدة."""
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.5  # Lower temperature for more accurate content
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
                        # Remove the post type prefix if it exists (e.g., "هل تعلم؟:")
                        cleaned_line = re.sub(r'^[^:]+:\s*', '', line.strip())
                        post_content += cleaned_line + " "
                
                post_content = post_content.strip()
                if post_content and len(post_content) > 20:  # Ensure we have substantial content
                    hashtags = re.findall(r'#[\w\u0600-\u06FF]+', post_content)  # Support Arabic hashtags
                    engagement_score = self._calculate_engagement_score(post_content)
                    
                    # Validate post quality
                    if self._validate_post_quality(post_content, post_type):
                        posts.append({
                            "post": post_content,
                            "hashtags": hashtags,
                            "type": post_type,
                            "engagement_score": engagement_score
                        })
            
            return posts[:num_posts]  # Ensure we return exactly the requested number
            
        except Exception as e:
            raise Exception(f"Failed to generate daily posts: {str(e)}")

    def generate_engaging_post(self, text, platform="general", max_length=280, dry_run=False):
        """
        Generate an engaging social media post from any text
        
        :param text: Original text to transform
        :param platform: Target platform (twitter, facebook, linkedin, instagram, general)
        :param max_length: Maximum length of the post
        :param dry_run: If True, still generate real posts but mark as dry run
        :return: Engaging social media post
        """
        # Generate real content even in dry run mode for testing
        
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

    def _analyze_article_content(self, content, title):
        """
        Analyze article content to extract key themes and information
        This helps the AI generate more accurate posts
        """
        try:
            analysis_prompt = f"""
            حلل هذا المقال العربي واستخرج:
            1. الموضوع الرئيسي
            2. أهم 3 نقاط أو معلومات
            3. أي أرقام أو إحصائيات مذكورة
            4. المصطلحات التقنية المهمة
            5. النصائح أو التوصيات العملية

            العنوان: {title}
            المحتوى: {content[:2000]}

            اكتب تحليلاً مختصراً (150 كلمة كحد أقصى) يركز على المعلومات الدقيقة فقط.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "أنت محلل محتوى دقيق يستخرج المعلومات الأساسية من النصوص العربية."},
                    {"role": "user", "content": analysis_prompt}
                ],
                max_tokens=300,
                temperature=0.3  # Lower temperature for more accurate analysis
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # If analysis fails, return a basic summary
            return f"مقال عن {title}. يحتوي على معلومات تقنية ونصائح عملية."

    def _validate_post_quality(self, post_content, post_type):
        """
        Validate that the generated post meets quality standards
        """
        # Check minimum length
        if len(post_content) < 30:
            return False
        
        # Check for generic/template phrases that indicate poor generation
        generic_phrases = [
            "هذا مثال",
            "هذه معلومة",
            "تجربة",
            "dry run",
            "مثال على",
            "نموذج",
            "اختبار"
        ]
        
        for phrase in generic_phrases:
            if phrase in post_content.lower():
                return False
        
        # Check that it has proper structure for the type
        if post_type == "did_you_know" and "هل تعلم" not in post_content:
            return False
        elif post_type == "definition" and "تعريف" not in post_content:
            return False
        elif post_type == "quick_tip" and "نصيحة" not in post_content:
            return False
        
        # Check for Arabic content (should have some Arabic characters)
        arabic_chars = len(re.findall(r'[\u0600-\u06FF]', post_content))
        if arabic_chars < 10:  # Should have at least 10 Arabic characters
            return False
        
        return True 