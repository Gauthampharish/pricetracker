from rest_framework import serializers

from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    """
    Serializer for the Alert model. This serializer handles the validation,
    creation, and representation of Alert instances.
    """

    class Meta:
        model = Alert
        fields = ['id', 'cryptocurrency', 'target_price', 'status', 'user']
        read_only_fields = ['id', 'user']

    def validate(self, data):
        """
        Validate the incoming data for the Alert instance.

        Args:
            data (dict): The data to validate.

        Raises:
            serializers.ValidationError: If the target_price is less than or equal to 0,
                                         if the cryptocurrency field is not provided,
                                         or if a duplicate alert exists.

        Returns:
            dict: The validated data.
        """
        user = self.context['request'].user
        cryptocurrency = data.get('cryptocurrency')
        target_price = data.get('target_price')
        if data['target_price'] <= 0:
            raise serializers.ValidationError("Target price must be greater than 0")
        if not cryptocurrency:
            raise serializers.ValidationError("Coin field is required")
        if Alert.objects.filter(user=user, cryptocurrency=cryptocurrency,target_price=target_price).exists():
            raise serializers.ValidationError("Alert for this cryptocurrency already exists")

        return data

    def create(self, validated_data):
        """
        Create a new Alert instance with the validated data.

        Args:
            validated_data (dict): The data that has been validated.

        Raises:
            serializers.ValidationError: If there is an error during the creation of the Alert instance.

        Returns:
            Alert: The created Alert instance.
        """
        try:
            alert = Alert.objects.create(user=self.context['request'].user, **validated_data)
            return alert
        except Exception as e:
            raise serializers.ValidationError(f"Error creating alert: {str(e)}")

    def delete(self, instance):
        """
        Delete an Alert instance.

        Args:
            instance (Alert): The Alert instance to delete.

        Raises:
            serializers.ValidationError: If there is an error during the deletion of the Alert instance.
        """
        try:
            instance.delete()
        except Exception as e:
            raise serializers.ValidationError(f"Error deleting alert: {str(e)}")
