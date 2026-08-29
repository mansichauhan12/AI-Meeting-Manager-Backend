from rest_framework import serializers

class StatisticsSerializer(serializers.Serializer):
    total_meetings = serializers.IntegerField()
    completed_meetings = serializers.IntegerField()
    processing_meetings = serializers.IntegerField()
    failed_meetings = serializers.IntegerField()
    pending_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    upcoming_reminders = serializers.IntegerField()

class UpcomingMeetingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    meeting_date = serializers.DateTimeField()

class RecentMeetingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    status = serializers.CharField()

class PendingTaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    priority = serializers.CharField()
    deadline = serializers.DateTimeField(allow_null=True)

class UpcomingReminderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    task_title = serializers.CharField()
    send_at = serializers.DateTimeField()

class DashboardResponseSerializer(serializers.Serializer):
    statistics = StatisticsSerializer()
    upcoming_meetings = UpcomingMeetingSerializer(many=True)
    pending_tasks = PendingTaskSerializer(many=True)
    upcoming_reminders = UpcomingReminderSerializer(many=True)
    recent_meetings = RecentMeetingSerializer(many=True)
