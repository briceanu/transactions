from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = User
        fields = ('username','email','balance')
      
    def validate_balance(self,value):
        if value < 0:
            raise serializers.ValidationError(detail="your balance can't be less than 0")
        return value