#!/usr/bin/env python3
"""
Test script for the daily posting feature
Verifies all components work correctly in dry-run mode
"""

import sys
import lib.logger
from daily_poster import generate_and_post_daily_content
from clients.openai.client import Client as OpenAIClient
from config import openai as openai_config
import lib.rss

logger = lib.logger.get_logger(__name__)

def test_random_article_fetching():
    """Test random article fetching from RSS"""
    print("🔍 Testing random article fetching...")
    try:
        article = lib.rss.fetch_random_article()
        print(f"✅ Successfully fetched random article: {article['title']}")
        print(f"   URL: {article['link']}")
        print(f"   ID: {article['id']}")
        return True
    except Exception as e:
        print(f"❌ Failed to fetch random article: {str(e)}")
        return False

def test_daily_post_generation():
    """Test daily post generation with OpenAI"""
    print("\n🤖 Testing daily post generation...")
    try:
        # Fetch an article first
        article = lib.rss.fetch_random_article()
        
        # Generate daily posts
        openai_client = OpenAIClient(openai_config)
        posts = openai_client.generate_daily_posts(
            url=article['link'],
            num_posts=3,
            dry_run=True  # Use dry run for testing
        )
        
        print(f"✅ Successfully generated {len(posts)} daily posts:")
        for i, post in enumerate(posts, 1):
            print(f"   Post {i} ({post['type']}): {post['post'][:100]}...")
            print(f"           Hashtags: {', '.join(post['hashtags'])}")
            print(f"           Engagement Score: {post.get('engagement_score', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to generate daily posts: {str(e)}")
        return False

def test_full_daily_posting_cycle():
    """Test the complete daily posting cycle"""
    print("\n🚀 Testing complete daily posting cycle...")
    try:
        generate_and_post_daily_content(dry_run=True, num_posts_to_generate=3)
        print("✅ Daily posting cycle completed successfully")
        return True
    except Exception as e:
        print(f"❌ Daily posting cycle failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Manshar Daily Posting Feature")
    print("=" * 50)
    
    tests = [
        test_random_article_fetching,
        test_daily_post_generation,
        test_full_daily_posting_cycle
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The daily posting feature is ready to use.")
        print("\nNext steps:")
        print("1. Configure your API keys in config.yaml")
        print("2. Run: python3 daily_poster.py --dry-run")
        print("3. If successful, remove --dry-run to start posting")
    else:
        print("⚠️  Some tests failed. Please check your configuration and dependencies.")
        sys.exit(1)

if __name__ == "__main__":
    main()