from rest_framework import serializers

from nutep.serializers import FileSerializer, UserSerializer, DateQueryEvent
from tracking.models import Container, FreightData, FreightTracking, Platform, \
    RailData, RailFreightTracking, RailTracking


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
               

class DateQueryTrackingSerializer(serializers.HyperlinkedModelSerializer):        
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
