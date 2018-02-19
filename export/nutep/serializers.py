from django.contrib.auth.models import User, Group
from rest_framework import serializers
from nutep.models import DateQueryEvent, File, UserProfile, RailFreightTracking,\
    Container, Platform, RailData, RailTracking, FreightData, FreightTracking


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('middle_name', 'position')
    

class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer()
    
    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'email', 'profile')
        

class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ('title', 'file')


class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = '__all__'
        

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'        
        

class RailDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RailData
        fields = '__all__'        
        
        
class RailTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RailTracking
        fields = '__all__'        
        

class FreightDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreightData
        fields = '__all__'          
        
        
class FreightTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreightTracking
        fields = '__all__'        
        

class TrackSerializer(serializers.HyperlinkedModelSerializer):
    container = ContainerSerializer()
    platform = PlatformSerializer()
    raildata = RailDataSerializer()
    railtracking = RailTrackingSerializer()
    freightdata = FreightDataSerializer()
    freighttracking = FreightTrackingSerializer()
    class Meta:
        model = RailFreightTracking
        fields = ('container', 'platform', 'raildata', 'railtracking', 'freightdata', 'freighttracking')
               

class DateQueryEventSerializer(serializers.HyperlinkedModelSerializer):        
    files = FileSerializer(many=True)
    user = UserSerializer()  
    tracks = TrackSerializer(many=True)
    type = serializers.SerializerMethodField()
    
    def get_type(self, obj):
        return obj.get_type_display()  
      
    class Meta:
        depth = 1
        model = DateQueryEvent
        fields = ('id', 'date', 'user', 'type', 'files', 'status', 'note', 'tracks')



