from domain.models.ScheduledPost import ScheduledPost
from domain.serializers.serializers import ScheduledPostSerializer

import uuid
from uuid import UUID
from utility.common.createresponse import CreateResponse
from utility.helper import errormessages
from utility.helper.constant import ErrorCodes
import traceback
import os
from django.core.files.storage import default_storage


def create_or_update_schedule(data, request=None):
    try:
        schedule_id = data.get("id")
        schedule = None

        if schedule_id:
            try:
                schedule_id = UUID(str(schedule_id))
            except (ValueError, TypeError, AttributeError):
                return CreateResponse.error("Invalid schedule ID.")

            schedule = ScheduledPost.objects.filter(pk=schedule_id).first()

            if not schedule:
                return CreateResponse.error("Schedule not found.")

        serializer = ScheduledPostSerializer(
            instance=schedule,
            data=data,
            partial=schedule is not None
        )

        if not serializer.is_valid():
            return CreateResponse.error(serializer.errors)

        values = dict(serializer.validated_data)
        values.pop("action_type", None)

        if schedule is None:
            schedule = ScheduledPost(**values)
        else:
            for key, value in values.items():
                setattr(schedule, key, value)

        schedule.save()
        return CreateResponse.success("Schedule saved successfully.", {"id": str(schedule.id)})

    except Exception as e:
        traceback.print_exc()
        return CreateResponse.error(f"An error occurred: {str(e)}")


def get_schedule_by_id(schedule_id):
    try:
        try:
            schedule_id = UUID(str(schedule_id))
        except (ValueError, TypeError, AttributeError):
            return CreateResponse.error("Invalid schedule ID.")

        schedule = ScheduledPost.objects.filter(pk=schedule_id).first()

        if not schedule:
            return CreateResponse.error("Schedule not found.")

        serializer = ScheduledPostSerializer(schedule)
        return CreateResponse.success("Schedule retrieved successfully.", serializer.data)

    except Exception as e:
        traceback.print_exc()
        return CreateResponse.error(f"An error occurred: {str(e)}")


def delete_schedule(schedule_id):
    try:
        try:
            schedule_id = UUID(str(schedule_id))
        except (ValueError, TypeError, AttributeError):
            return CreateResponse.error("Invalid schedule ID.")

        schedule = ScheduledPost.objects.filter(pk=schedule_id).first()

        if not schedule:
            return CreateResponse.error("Schedule not found.")

        schedule.action_type = 3
        schedule.save(update_fields=["action_type", "updated_on"])
        return CreateResponse.success("Schedule deleted successfully.")

    except Exception as e:
        traceback.print_exc()
        return CreateResponse.error(f"An error occurred: {str(e)}")


def get_all_schedules(query_params=None):
    try:
        schedules = ScheduledPost.objects.filter(action_type=1)
        serializer = ScheduledPostSerializer(schedules, many=True)
        return CreateResponse.success("Schedules retrieved successfully.", serializer.data)

    except Exception as e:
        traceback.print_exc()
        return CreateResponse.error(f"An error occurred: {str(e)}")    

def create_facebook_schedule(content, social_connect, scheduled_time):
    if social_connect.platform != "facebook":
        raise ValueError("This function is only for Facebook.")
        
    schedule = Schedule.objects.create(
        content=content,
        social_connect=social_connect,
        brand=social_connect.brand,
        scheduled_time=scheduled_time,
        status="pending",
    )

    # If the time has already passed, run immediately; otherwise, schedule for later
    if scheduled_time <= timezone.now():
        publish_to_facebook.delay(schedule.id)
    else:
        publish_to_facebook.apply_async(args=[schedule.id], eta=scheduled_time)

    return schedule