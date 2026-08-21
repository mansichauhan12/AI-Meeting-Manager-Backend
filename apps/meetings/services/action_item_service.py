from apps.meetings.models import ActionItem

class ActionItemService:

    @staticmethod
    def create_action_item(validated_data):
        return ActionItem.objects.create(**validated_data)

    @staticmethod
    def update_action_item(action_item, validated_data):
        for attr, value in validated_data.items():
            setattr(action_item, attr, value)
        action_item.save()
        return action_item

    @staticmethod
    def delete_action_item(action_item):
        action_item.delete()
