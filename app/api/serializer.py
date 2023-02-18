from app.models import *
from rest_framework import serializers
from dynamic_rest.serializers import DynamicModelSerializer,DynamicRelationField
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class AuthTokenSerializer(serializers.Serializer):
    mobile = serializers.CharField(label=_("Mobile"))
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        mobile = attrs.get("mobile")
        password = attrs.get("password")

        if mobile and password:
            user = authenticate(
                request=self.context.get("request"), username=mobile, password=password
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "mobile" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
        
class CountrySerializer(DynamicModelSerializer):
    class Meta:
        model = Country
        exclude = ['created_at','updated_at']

class RegionSerializer(DynamicModelSerializer):
  country = DynamicRelationField(CountrySerializer,embed=True)
  class Meta:
    model = Region
    exclude = ['created_at','updated_at']

class AddressSerializer(DynamicModelSerializer):
    region = DynamicRelationField(RegionSerializer,embed=True)
    class Meta:
        model = Address
        fields = '__all__'

class ProviderTypeSerilaizer(DynamicModelSerializer):
    class Meta:
        model = ProviderType
        exclude = ['created_at','updated_at']

class ServiceFieldSerializer(DynamicModelSerializer):
    class Meta:
        model = ServiceField
        exclude = ['created_at','updated_at']

class ServiceProviderSerializer(DynamicModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = '__all__'

class ProviderTechnicalSerializer(DynamicModelSerializer):
    technical_region = DynamicRelationField(RegionSerializer,embed=True)
    provider = DynamicRelationField(ServiceProviderSerializer,embed=True)
    class Meta:
        model=ProviderTechnical
        fields = '__all__'

class ProviderTechnicalTeamSerializer(DynamicModelSerializer):
    team_region = DynamicRelationField(RegionSerializer,embed=True)
    provider = DynamicRelationField(ServiceProviderSerializer,embed=True)
    class Meta:
        model=ProviderTechnicalTeam
        fields = '__all__'


class ServiceSerializer(DynamicModelSerializer):
    region= DynamicRelationField("RegionSerializer",embed=True,many=True)
    service_field = DynamicRelationField("ServiceFieldSerializer",embed=True)
    provider = DynamicRelationField("ServiceProviderSerializer",embed=True)

    class Meta:
        model = Service
        fields = '__all__'

class SubServiceSerializer(DynamicModelSerializer):
    service = DynamicRelationField(ServiceSerializer,embed=True)
    class Meta:
        model = SubService
        fields = '__all__'

class ServiceRequirementSerializer(DynamicModelSerializer):
    service = DynamicRelationField(ServiceSerializer,embed=True)
    reference = DynamicRelationField(SubServiceSerializer,embed=True)
    class Meta:
        model = ServiceRequirement
        fields = '__all__'

class ServiceRequirementChoicesSerializer(DynamicModelSerializer):
    class Meta:
        model = ServiceRequirementChoices
        fields = '__all__'

class ClientSerializer(DynamicModelSerializer):
    address = DynamicRelationField(AddressSerializer,embed=True)
    type = serializers.CharField(source="get_type_display") 
    class Meta:
        model = Client
        fields = ['id','type','name','mobile','email','address',"groups",
            "is_superuser"]

class UserClientSerializer(DynamicModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ServiceRequirementRequestSerializer(DynamicModelSerializer):
    class Meta:
        model = ServiceRequirementRequest
        fields = '__all__'

class OfferSerializer(DynamicModelSerializer):
      service = DynamicRelationField(ServiceSerializer,embed=True)
      sub_service = DynamicRelationField(SubServiceSerializer,embed=True)

      class Meta:
        model = Offer
        fields = '__all__'

class ClientOrderSerializer(DynamicModelSerializer):
    client = DynamicRelationField(ClientSerializer,embed=True)
    service = DynamicRelationField(ServiceSerializer,embed=True)
    sub_service = DynamicRelationField(SubServiceSerializer,embed=True)
    offer = DynamicRelationField(OfferSerializer,embed=True)
    status = serializers.CharField(source="get_status_display")
    class Meta:
        model = ClientOrder
        fields = ['id','status','cancel_order_permission',
         'feedback_permission','service','client','sub_service',
         'offer','cancel_order','technical_name','team_name','contact_mobile',
         'address','price','notes','desired_date','order_requirements_requests']

class OrderFeedBackSerializer(DynamicModelSerializer):
    order = DynamicRelationField(ClientOrderSerializer,embed=True)
    class Meta:
        model = OrderFeedBack
        fields = '__all__'

class ProfileSerializer(DynamicModelSerializer):
    client = DynamicRelationField(ClientSerializer,embed=True)
    class Meta:
        model = Profile
        fields = '__all__'