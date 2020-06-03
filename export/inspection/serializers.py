from rest_framework import serializers
from inspection.models import Inspection
from nutep.serializers import FileSerializer

class InspectionSerializer(serializers.ModelSerializer):           
    files = FileSerializer(many=True)
    class Meta:
        depth = 1
        model = Inspection
        fields = ('id', 'guid', 'container', 'date', 'files')