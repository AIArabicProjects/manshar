#!/usr/bin/env python3
"""
Daily Social Media Poster
Manually generates and posts engaging content from aiinarabic.com articles
"""

import lib.rss
import lib.logger
import random
import time
from datetime import datetime

from clients.facebook.client import Client as FacebookClient
from clients.x.client import Client as XClient
from clients.linkedin.client import Client as LinkedinClient
from clients.telegram.client import Client as TelegramClient
from clients.openai.client import Client as OpenAIClient

from config import facebook as facebook_config
from config import x as x_config
from config import linkedin as linkedin_config
from config import telegram as telegram_config
from config import openai as openai_config

logger = lib.logger.get_logger(__name__)


def post_to_platform(platform_client, post_data, platform_name, article_link=None, dry_run=False):
    """Post content to a specific social media platform"""
    try:
        post_content = post_data['post']
        
        # Add article reference if not already included
        if article_link and "اقرأ المزيد:" not in post_content and "aiinarabic.com" not in post_content:
            post_content += f"\n\nاقرأ المزيد: {article_link}"
        
        # X client doesn't accept 'link' parameter, others do
        if platform_name == "X":
            response = platform_client.send(
                message=post_content,
                dry_run=dry_run
            )
        else:
            response = platform_client.send(
                message=post_content, 
                link=article_link,
                dry_run=dry_run
            )
        
        logger.info(f"{platform_name} daily post successful: {response}")
        return True
    except Exception as e:
        logger.error(f"Failed to post to {platform_name}: {str(e)}")
        return False

def select_best_post(posts, platform_preferences=None):
    """Select the best post based on engagement score and platform preferences"""
    if not posts:
        return None
    
    # Platform-specific preferences
    platform_prefs = platform_preferences or {}
    
    # Weight posts by engagement score and type preferences
    weighted_posts = []
    for post in posts:
        weight = post.get('engagement_score', 5.0)
        
        # Boost certain types for specific platforms
        post_type = post.get('type', '')
        if 'did_you_know' in post_type or 'amazing_fact' in post_type:
            weight += 1.0  # These tend to perform well
        elif 'definition' in post_type:
            weight += 0.5  # Educational content is good
        
        weighted_posts.append((post, weight))
    
    # Sort by weight and add some randomness to avoid always picking the same type
    weighted_posts.sort(key=lambda x: x[1] + random.uniform(0, 1), reverse=True)
    
    return weighted_posts[0][0]

def generate_and_post_daily_content(dry_run=False, num_posts_to_generate=5):
    """
    Main function to generate and post daily engaging content
    
    :param dry_run: If True, don't actually post to social media
    :param num_posts_to_generate: Number of different posts to generate and choose from
    """
    try:
        # Fetch a random article
        article = lib.rss.fetch_random_article()
        if not article:
            logger.error("No articles found")
            return
        
        logger.info(f"Selected article for daily content generation: {article['title']}")
        
        # Generate multiple daily posts from the article
        openai_client = OpenAIClient(openai_config)
        daily_posts = openai_client.generate_daily_posts(
            url=article['link'],
            num_posts=num_posts_to_generate,
            dry_run=dry_run
        )
        
        if not daily_posts:
            logger.error("Failed to generate daily posts")
            return
        
        logger.info(f"Generated {len(daily_posts)} daily posts")
        
        # Log the generated posts in dry run mode
        if dry_run:
            logger.info("=== GENERATED POSTS (DRY RUN) ===")
            for i, post in enumerate(daily_posts, 1):
                logger.info(f"Post {i} ({post.get('type', 'unknown')}):")
                logger.info(f"  Content: {post['post']}")
                logger.info(f"  Hashtags: {', '.join(post.get('hashtags', []))}")
                logger.info(f"  Engagement Score: {post.get('engagement_score', 'N/A')}")
                logger.info("  " + "-" * 50)
        
        # Select the best posts for each platform
        platforms = [
            (FacebookClient(facebook_config), "Facebook"),
            (XClient(x_config), "X"),
            (TelegramClient(telegram_config), "Telegram")
        ]
        
        posted_count = 0
        for platform_client, platform_name in platforms:
            selected_post = select_best_post(daily_posts)
            if not selected_post:
                continue
            
            # Post to the platform
            success = post_to_platform(
                platform_client=platform_client,
                post_data=selected_post,
                platform_name=platform_name,
                article_link=article['link'],
                dry_run=dry_run
            )
            
            if success:
                posted_count += 1
                
                # Add some delay between posts to avoid rate limiting
                if not dry_run:
                    time.sleep(5)
        
        if posted_count > 0:
            logger.info(f"Successfully posted daily content to {posted_count} platforms")
            # Mark the article as used (optional - you might want to reuse articles for different post types)
            # update_posted_history(article['id'], "history.txt")
        else:
            logger.warning("Failed to post to any platforms")
            
    except Exception as e:
        logger.error(f"Error in daily content generation: {str(e)}")
        raise

if __name__ == "__main__":
    import sys
    
    # Check for dry-run flag
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        logger.info("Running in DRY RUN mode - no actual posts will be made")
    
    # Run the daily posting cycle once
    start_time = datetime.now()
    logger.info(f"Starting daily posting cycle at {start_time}")
    
    try:
        generate_and_post_daily_content(dry_run=dry_run)
        
        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"Daily posting cycle completed successfully in {duration}")
        
    except Exception as e:
        logger.error(f"Daily posting cycle failed: {str(e)}")
        sys.exit(1)