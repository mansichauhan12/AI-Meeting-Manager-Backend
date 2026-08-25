from apps.meetings.models import Reminder

class ReminderService:

    @staticmethod
    def create_reminder(validated_data):
        return Reminder.objects.create(**validated_data)

    @staticmethod
    def update_reminder(reminder, validated_data):
        for attr, value in validated_data.items():
            setattr(reminder, attr, value)
        reminder.save()
        return reminder

    @staticmethod
    def delete_reminder(reminder):
        reminder.delete()
