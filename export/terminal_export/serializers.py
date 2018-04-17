from rest_framework import serializers

from nutep.serializers import DateQueryEvent, FileSerializer, \
    NomenclatureSerializer, UserSerializer
from terminal_export import models


class StuffingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stuffing
        fields = '__all__'
       

class ContainerSerializer(serializers.ModelSerializer):
    stuffs = StuffingSerializer(many=True)
    class Meta:
        model = models.Container
        fields = '__all__'


class TerminalExportSerializer(serializers.HyperlinkedModelSerializer):
    container = ContainerSerializer()
    nomenclature = NomenclatureSerializer()
    class Meta:
        model = models.TerminalExport
        fields = ('nomenclature', 'container', 'rowindex')
               

class DateQueryTrackingSerializer(serializers.HyperlinkedModelSerializer):        
    files = FileSerializer(many=True)
    user = UserSerializer()  
    terminalexports = TerminalExportSerializer(many=True)
    type = serializers.SerializerMethodField()
    
    def get_type(self, obj):
        return obj.get_type_display()  
      
    class Meta:
        depth = 1
        model = DateQueryEvent
        fields = ('id', 'date', 'user', 'type', 'files', 'status', 'note', 'terminalexports')
