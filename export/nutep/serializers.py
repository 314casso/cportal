from django.contrib.auth.models import Group, User
from rest_framework import serializers

from nutep.models import DateQueryEvent, Employee, File, News, Nomenclature, \
    UserProfile


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
        fields = ('title', 'file', 'extension')


class DateQueryReviseSerializer(serializers.HyperlinkedModelSerializer):        
    files = FileSerializer(many=True)
    user = UserSerializer() 
    type = serializers.SerializerMethodField()
    
    def get_type(self, obj):
        return obj.get_type_display()  
      
    class Meta:
        depth = 1
        model = DateQueryEvent
        fields = ('id', 'date', 'user', 'type', 'files', 'status', 'note')


class EventStatusSerializer(serializers.HyperlinkedModelSerializer):       
    user = UserSerializer()  
    class Meta:
        depth = 1
        model = DateQueryEvent
        fields = ('id', 'date', 'type', 'status', 'user')
     

class EmployeesSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    class Meta:
        depth = 1
        model = Employee
        fields = ('domainname','crm_id','portal_id','first_name','last_name','middle_name','job_title','image','head','mobile','phone','email','skype','users')
                

class NewsSerializer(serializers.ModelSerializer):    
    class Meta:
        depth = 1
        model = News
        fields = '__all__'
        

class NomenclatureSerializer(serializers.ModelSerializer):    
    class Meta:
        depth = 1
        model = Nomenclature
        fields = '__all__'        