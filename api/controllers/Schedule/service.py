<<<<<<< HEAD
from domain.models.ScheduledPost import ScheduledPost as Schedule
from domain.serializers.serializers import ScheduledPostSerializer as ScheduleSerializer
from domain.models.ScheduledPost import ScheduledPost
from domain.serializers.serializers import ScheduledPostSerializer
import uuid
=======
from domain.models.ScheduledPost import ScheduledPost
from domain.serializers.serializers import ScheduledPostSerializer
>>>>>>> 03068d74c73c51b4e0028b6152608326ed2983e5
from uuid import UUID
from utility.common.createresponse import CreateResponse
import traceback


def create_or_update_schedule(data, request):
    try:
        schedule_id = data.get("id")
        schedule = None

        if schedule_id:
            try:
                schedule_id = UUID(str(schedule_id))
            except (ValueError, TypeError, AttributeError):
                return CreateResponse.error("Invalid schedule ID.")

            schedules = ScheduledPost.objects.filter(
                pk=schedule_id,
                action_type=1,
                brand__user=request.user,
            )
            schedule = schedules.first()

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
        brand = values.get("brand", schedule.brand if schedule else None)
        if brand is None or brand.user_id != request.user.id:
            return CreateResponse.error("Brand not found.")

        product = values.get("product", schedule.product if schedule else None)
        if product is not None and product.brand_id != brand.id:
            return CreateResponse.error("Product does not belong to this brand.")

        generated_content = values.get(
            "generated_content",
            schedule.generated_content if schedule else None,
        )
        if (
            generated_content is not None
            and generated_content.product.brand_id != brand.id
        ):
            return CreateResponse.error(
                "Generated content does not belong to this brand."
            )

        if schedule is None:
            if values.get("created_by_user") != request.user:
                return CreateResponse.error(
                    "A schedule must be created by the authenticated user."
                )
        else:
            values.pop("created_by_user", None)

        if schedule is None:
            schedule = ScheduledPost(**values)
        else:
            for key, value in values.items():
                setattr(schedule, key, value)

        schedule.save()
        return CreateResponse.success(
            {"id": str(schedule.id)},
            "Schedule saved successfully.",
        )

    except Exception as e:
        traceback.print_exc()
        return CreateResponse.error(f"An error occurred: {str(e)}")


def get_schedule_by_id(schedule_id, request):
    try:
        try:
            schedule_id = UUID(str(schedule_id))
        except (ValueError, TypeError, AttributeError):
            return CreateResponse.error("Invalid schedule ID.")

        schedules = ScheduledPost.objects.filter(
            pk=schedule_id,
            action_type=1,
            brand__user=request.user,
        )
        schedule = schedules.first()

        if not schedule:
            return CreateResponse.error("Schedule not found.")

        serializer = ScheduledPostSerializer(schedule)
        return CreateResponse.success(
            serializer.data,
            "Schedule retrieved successfully.",
        )

    except Exception as e:
        traceback.print_exc()
        return CreateResponse.error(f"An error occurred: {str(e)}")


def delete_schedule(schedule_id, request):
    try:
        try:
            schedule_id = UUID(str(schedule_id))
        except (ValueError, TypeError, AttributeError):
            return CreateResponse.error("Invalid schedule ID.")

        schedules = ScheduledPost.objects.filter(
            pk=schedule_id,
            action_type=1,
            brand__user=request.user,
        )
        schedule = schedules.first()

        if not schedule:
            return CreateResponse.error("Schedule not found.")

        schedule.action_type = 3
        schedule.save(update_fields=["action_type", "updated_on"])
        return CreateResponse.success(None, "Schedule deleted successfully.")

    except Exception as e:
        traceback.print_exc()
        return CreateResponse.error(f"An error occurred: {str(e)}")

<<<<<<< HEAD
def get_all_schedules(request):
    try:
        schedules = Schedule.objects.filter(brand__user=request.user, action_type=1)
        
        serializer = ScheduleSerializer(schedules, many=True)
        return CreateResponse.success("Schedules retrieved successfully.", serializer.data)
=======

def get_all_schedules(request):
    try:
        schedules = ScheduledPost.objects.filter(
            brand__user=request.user,
            action_type=1,
        )
        serializer = ScheduledPostSerializer(schedules, many=True)
        return CreateResponse.success(
            serializer.data,
            "Schedules retrieved successfully.",
        )
>>>>>>> 03068d74c73c51b4e0028b6152608326ed2983e5
    except Exception as e:
        traceback.print_exc()
        return CreateResponse.error(f"An error occurred: {str(e)}")