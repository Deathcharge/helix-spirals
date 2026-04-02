"""
Social Media Automation Workflow Example
=========================================

This example demonstrates automating content distribution across multiple
social media platforms using Helix Spirals.

Workflow:
1. Receive content from Notion database
2. Generate social media captions using AI
3. Schedule posts across platforms (Twitter, LinkedIn, Instagram)
4. Track engagement metrics
5. Log analytics

This showcases:
- Integration with content management (Notion)
- AI-powered content generation
- Multi-platform distribution
- Scheduled execution
- Metrics tracking
"""

from helix_spirals import (
    WorkflowEngine,
    WorkflowNode,
    IntegrationNode,
    ConditionalNode,
)
from datetime import datetime, timedelta


def create_social_media_workflow():
    """Create a social media automation workflow."""
    
    engine = WorkflowEngine()
    
    # ============================================================
    # 1. TRIGGER: Scheduled trigger (daily at 9 AM)
    # ============================================================
    trigger = WorkflowNode(
        name="daily_schedule",
        node_type="trigger",
        trigger_type="schedule",
        config={
            "schedule": "cron",
            "expression": "0 9 * * *",  # Daily at 9 AM
            "timezone": "UTC"
        }
    )
    
    # ============================================================
    # 2. FETCH CONTENT: Get draft posts from Notion
    # ============================================================
    fetch_content = IntegrationNode(
        name="fetch_draft_posts",
        integration_type="notion",
        action="query_database",
        config={
            "database_id": "notion_db_123",
            "filter": {
                "property": "Status",
                "select": {"equals": "Draft"}
            },
            "limit": 5
        }
    )
    
    # ============================================================
    # 3. PROCESS EACH POST: Loop through fetched posts
    # ============================================================
    process_post = WorkflowNode(
        name="process_post",
        node_type="loop",
        action="for_each",
        config={
            "items": "${posts}",
            "parallel": False  # Process sequentially
        }
    )
    
    # ============================================================
    # 4. GENERATE CAPTIONS: AI-powered caption generation
    # ============================================================
    generate_caption = WorkflowNode(
        name="generate_captions",
        node_type="action",
        action="call_llm",
        config={
            "prompt": """Generate engaging social media captions for the following content:
            
Title: ${post.title}
Content: ${post.content}
Platform: ${platform}

Requirements:
- Keep it concise and engaging
- Include relevant hashtags
- Optimize for the platform
- Match the brand voice""",
            "model": "gpt-4",
            "temperature": 0.7
        }
    )
    
    # ============================================================
    # 5. TWITTER: Post to Twitter
    # ============================================================
    post_twitter = IntegrationNode(
        name="post_twitter",
        integration_type="twitter",
        action="create_tweet",
        config={
            "text": "${caption_twitter}",
            "media": "${post.media_urls}",
            "reply_settings": "everyone"
        }
    )
    
    # ============================================================
    # 6. LINKEDIN: Post to LinkedIn
    # ============================================================
    post_linkedin = IntegrationNode(
        name="post_linkedin",
        integration_type="linkedin",
        action="create_post",
        config={
            "text": "${caption_linkedin}",
            "media": "${post.media_urls}",
            "visibility": "PUBLIC"
        }
    )
    
    # ============================================================
    # 7. INSTAGRAM: Post to Instagram
    # ============================================================
    post_instagram = IntegrationNode(
        name="post_instagram",
        integration_type="instagram",
        action="create_post",
        config={
            "caption": "${caption_instagram}",
            "media": "${post.media_urls}",
            "hashtags": "${post.hashtags}"
        }
    )
    
    # ============================================================
    # 8. UPDATE STATUS: Mark post as published in Notion
    # ============================================================
    update_notion = IntegrationNode(
        name="update_post_status",
        integration_type="notion",
        action="update_page",
        config={
            "page_id": "${post.notion_id}",
            "properties": {
                "Status": {"select": {"name": "Published"}},
                "Published Date": {"date": {"start": "${now}"}},
                "Twitter URL": "${twitter_url}",
                "LinkedIn URL": "${linkedin_url}",
                "Instagram URL": "${instagram_url}"
            }
        }
    )
    
    # ============================================================
    # 9. TRACK METRICS: Log to analytics
    # ============================================================
    track_metrics = IntegrationNode(
        name="track_metrics",
        integration_type="mixpanel",
        action="track_event",
        config={
            "event": "social_post_published",
            "properties": {
                "post_id": "${post.id}",
                "platforms": ["twitter", "linkedin", "instagram"],
                "timestamp": "${now}",
                "content_type": "${post.type}"
            }
        }
    )
    
    # ============================================================
    # 10. SUMMARY: Send summary email
    # ============================================================
    send_summary = IntegrationNode(
        name="send_summary_email",
        integration_type="email",
        action="send_email",
        config={
            "to": "content-team@example.com",
            "subject": "Social Media Posts Published - ${date}",
            "template": "social_media_summary",
            "data": {
                "posts_published": "${posts_count}",
                "platforms": ["Twitter", "LinkedIn", "Instagram"],
                "engagement_summary": "${engagement_data}"
            }
        }
    )
    
    # ============================================================
    # END NODE
    # ============================================================
    end = WorkflowNode(
        name="complete",
        node_type="end"
    )
    
    # ============================================================
    # CONNECTIONS
    # ============================================================
    trigger.connect_to(fetch_content)
    fetch_content.connect_to(process_post)
    
    # Inside loop
    process_post.connect_to(generate_caption)
    
    # Parallel posting to all platforms
    generate_caption.connect_to(post_twitter)
    generate_caption.connect_to(post_linkedin)
    generate_caption.connect_to(post_instagram)
    
    # Converge and update
    post_twitter.connect_to(update_notion)
    post_linkedin.connect_to(update_notion)
    post_instagram.connect_to(update_notion)
    
    # Track and summarize
    update_notion.connect_to(track_metrics)
    track_metrics.connect_to(send_summary)
    send_summary.connect_to(end)
    
    return engine, trigger


def print_workflow_visualization():
    """Print workflow structure."""
    
    visualization = """
    Social Media Automation Workflow
    ================================
    
    daily_schedule (9 AM UTC)
           ↓
    fetch_draft_posts (Notion)
           ↓
    process_post (for each post)
           ↓
    generate_captions (LLM)
           ↓
    ┌──────┼──────┐
    ↓      ↓      ↓
    Twitter LinkedIn Instagram
    ↓      ↓      ↓
    └──────┼──────┘
           ↓
    update_post_status (Notion)
           ↓
    track_metrics (Mixpanel)
           ↓
    send_summary_email
           ↓
    complete ✅
    
    Features:
    - Scheduled daily execution
    - Multi-platform distribution
    - AI-powered caption generation
    - Parallel posting
    - Status tracking
    - Analytics logging
    """
    
    print(visualization)


def example_advanced_scheduling():
    """Example with advanced scheduling options."""
    
    print("Advanced Scheduling Options:")
    print("-" * 60)
    
    scheduling_options = {
        "daily": "0 9 * * *",
        "weekly": "0 9 * * MON",
        "business_days": "0 9 * * 1-5",
        "every_4_hours": "0 */4 * * *",
        "custom": "0 9,14,18 * * *"  # 9 AM, 2 PM, 6 PM
    }
    
    for name, cron_expr in scheduling_options.items():
        print(f"  {name:20} → {cron_expr}")
    
    print()


def example_workflow_execution():
    """Example execution of the workflow."""
    
    engine, trigger = create_social_media_workflow()
    
    # Example: Manual trigger with specific content
    trigger_data = {
        "posts": [
            {
                "id": "post_1",
                "notion_id": "notion_123",
                "title": "Introducing Helix Spirals",
                "content": "We're excited to announce Helix Spirals, an open-source workflow automation engine.",
                "type": "announcement",
                "media_urls": ["https://example.com/image1.jpg"],
                "hashtags": "#automation #workflows #openSource"
            },
            {
                "id": "post_2",
                "notion_id": "notion_456",
                "title": "5 Tips for Workflow Optimization",
                "content": "Learn how to optimize your workflows for maximum efficiency...",
                "type": "educational",
                "media_urls": ["https://example.com/image2.jpg"],
                "hashtags": "#tips #productivity #engineering"
            }
        ]
    }
    
    try:
        result = engine.execute(
            trigger,
            trigger_data=trigger_data,
            metadata={"source": "manual", "user": "content-manager"}
        )
        
        print("✅ Social media workflow executed successfully")
        print(f"   Posts published: {len(trigger_data['posts'])}")
        print(f"   Platforms: Twitter, LinkedIn, Instagram")
        print(f"   Status: {result.status}")
        
        return result
        
    except Exception as e:
        print(f"❌ Workflow execution failed: {e}")
        raise


if __name__ == "__main__":
    print("=" * 70)
    print("Helix Spirals - Social Media Automation Example")
    print("=" * 70)
    print()
    
    print("Workflow Structure:")
    print("-" * 70)
    print_workflow_visualization()
    print()
    
    example_advanced_scheduling()
    
    print("Executing workflow...")
    print("-" * 70)
    example_workflow_execution()
    print()
    
    print("=" * 70)
    print("Example completed!")
    print("=" * 70)
