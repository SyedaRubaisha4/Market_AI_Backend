# api/tasks.py
from celery import shared_task
from asgiref.sync import async_to_sync
from django.utils import timezone
from socialchimp import Post
from domain.social_client import get_social_client
from domain.models.ScheduledPost import Schedule

@shared_task(bind=True, max_retries=3)
def publish_scheduled_post(self, schedule_id: int):
    schedule = Schedule.objects.get(id=schedule_id)
    if schedule.status == "published":
        return "Already published"

    Schedule.objects.filter(id=schedule_id).update(status="publishing")

    try:
        client = get_social_client()
        account = client.account(schedule.social_connect.socialchimp_connection_id)

        media_urls = []
        if schedule.content.media_file:
            media_urls.append(schedule.content.media_file.url)

        post = Post(
            text=schedule.content.caption or "",
            media=media_urls,
        )
        
        result = async_to_sync(account.post)(post)

        Schedule.objects.filter(id=schedule_id).update(
            status="published",
            platform_post_id=result.id,
            published_at=timezone.now(),
        )
        return f"Published on {schedule.social_connect.platform}: {result.id}"

    except Exception as exc:
        Schedule.objects.filter(id=schedule_id).update(
            status="failed",
            error_message=str(exc),
        )
        raise self.retry(exc=exc, countdown=60)