# api/tasks.py
from asgiref.sync import async_to_sync
from celery import shared_task
from django.utils import timezone
from socialchimp import Post
from domain.social_client import get_social_client
from domain.models.ScheduledPost import Schedule

@shared_task(bind=True, max_retries=3)
def publish_to_facebook(self, schedule_id: int):
    try:
        schedule = Schedule.objects.get(id=schedule_id)
        
        if schedule.status == "published":
            return "Already published"

        # Update status to prevent double posting if the task is picked up twice
        Schedule.objects.filter(id=schedule_id).update(status="publishing")

        client = get_social_client()
        account = client.account(schedule.social_connect.socialchimp_connection_id)

        # Media URL must be publicly accessible (e.g., ngrok or S3)
        media_urls = []
        if schedule.content.media_file:
            media_urls.append(schedule.content.media_file.url)

        post = Post(
            text=schedule.content.caption or "",
            media=media_urls,
        )

        # Publish the post to Facebook
        result = async_to_sync(account.post)(post)

        # Update success status in database
        Schedule.objects.filter(id=schedule_id).update(
            status="published",
            platform_post_id=result.id,
            published_at=timezone.now(),
        )
        return f"Published: {result.id}"

    except Exception as exc:
        # Update failure status in database
        Schedule.objects.filter(id=schedule_id).update(
            status="failed",
            error_message=str(exc),
        )
        raise self.retry(exc=exc, countdown=60)