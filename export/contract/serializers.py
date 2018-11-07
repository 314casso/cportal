
from rest_framework import serializers

from contract.models import Contract, ContractEvent
from nutep.models import DateQueryEvent, File


class ContractSerializer(serializers.ModelSerializer):    
    class Meta:
        depth = 1
        model = Contract
        exclude = ('company',)


class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ('title', 'guid', 'size', 'doc_type', 'extension')


class ContractEventSerializer(serializers.ModelSerializer):    
    files = FileSerializer(many=True)
    class Meta:
        depth = 1
        model = ContractEvent
        exclude = ('event', 'contract')


class DateQueryContractSerializer(serializers.HyperlinkedModelSerializer):        
    
    type = serializers.SerializerMethodField()
    contractevent = ContractEventSerializer()
    
    def get_type(self, obj):
        return obj.get_type_display()  
      
    class Meta:
        depth = 1
        model = DateQueryEvent
        fields = ('id', 'date', 'type', 'status', 'note', 'contractevent')