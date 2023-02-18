from dynamic_rest.viewsets import DynamicModelViewSet
from .serializer import *
from app.models import *
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.views import ObtainAuthToken


Client = get_user_model()

class AuthLogin(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    def post(self,request,*args,**kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={"request": request})
            if serializer.is_valid():
                user = serializer.validated_data['user']
                refresh = RefreshToken.for_user(user)
                obj = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
                return Response(obj,status=status.HTTP_200_OK)
            else:
                print(serializer.errors,serializer.error_messages)
                return Response({"error":"خطأ برقم الهاتف أو كلمة المرور"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":f'تعذر تسجيل الدخول بسبب {e}'},status=status.HTTP_400_BAD_REQUEST)

class CountryViewSet(DynamicModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    http_method_names = ['get']

class RegionViewSet(DynamicModelViewSet):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
    http_method_names = ['get']

class AddressViewSet(DynamicModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    
   

class ProviderTypeViewSet(DynamicModelViewSet):
    serializer_class = ProviderTypeSerilaizer
    queryset = ProviderType.objects.all()
    http_method_names = ['get']


class ServiceFieldViewSet(DynamicModelViewSet):
    serializer_class = ServiceFieldSerializer
    queryset = ServiceField.objects.all()
    http_method_names = ['get']


class ServiceProviderViewSet(DynamicModelViewSet):
    serializer_class = ServiceProviderSerializer
    queryset = ServiceProvider.objects.all()



class ProviderTechnicalViewSet(DynamicModelViewSet):
    serializer_class = ProviderTechnicalSerializer
    queryset = ProviderTechnical.objects.all()
    permission_classes = [IsAuthenticated]


class ProviderTechnicalTeamViewSet(DynamicModelViewSet):
    serializer_class = ProviderTechnicalTeamSerializer
    queryset = ProviderTechnicalTeam.objects.all()
    permission_classes = [IsAuthenticated]

class ServiceViewSet(DynamicModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


class SubServiceViewSet(DynamicModelViewSet):
    serializer_class = SubServiceSerializer
    queryset = SubService.objects.all()
    
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = SubServiceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({"error":"يوجد خطأ بالبيانات"},status=status.HTTP_400_BAD_REQUEST)
            instance = super().create(request, *args, **kwargs)
            return Response(instance,status=status.HTTP_201_CREATED)
        except Exception as e:
             return Response({"error": f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


class ServiceRequirementViewSet(DynamicModelViewSet):
    serializer_class = ServiceRequirementSerializer
    queryset = ServiceRequirement.objects.all()


class ServiceRequirementChoicesViewSet(DynamicModelViewSet):
    serializer_class = ServiceRequirementChoicesSerializer
    queryset = ServiceRequirementChoices.objects.all()


class ClientViewSet(DynamicModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            data['password'] = make_password(data['password'])
            if not 'type' in data.keys():
                data['type'] = 1
            serializer = UserClientSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                instance = serializer.instance
                return Response(ClientSerializer(instance=instance).data,status=status.HTTP_201_CREATED)
            else:
                print(serializer.error_messages)
                return Response({"error":"يوجد خطأ بالبيانات "},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
           return Response({"error":f'تعذر انشاء حساب بسبب {e}'},status=status.HTTP_400_BAD_REQUEST)

class ServiceRequirementRequestViewSet(DynamicModelViewSet):
    serializer_class = ServiceRequirementRequestSerializer
    queryset = ServiceRequirementRequest.objects.all()
    permission_classes = [IsAuthenticated]


class OfferViewSet(DynamicModelViewSet):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()


class ClientOrderViewSet(DynamicModelViewSet):
    serializer_class = ClientOrderSerializer
    queryset = ClientOrder.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = ClientOrderSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({"error":"يوجد خطأ بالبيانات"},status=status.HTTP_400_BAD_REQUEST)
            instance = super().create(request, *args, **kwargs)
            return Response(instance,status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


class OrderFeedBackViewSet(DynamicModelViewSet):
    serializer_class = OrderFeedBackSerializer
    queryset = OrderFeedBack.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = OrderFeedBackSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({"error":"يوجد خطأ بالبيانات"},status=status.HTTP_400_BAD_REQUEST)
            instance = super().create(request, *args, **kwargs)
            return Response(instance,status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileViewSet(DynamicModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    http_method_names = ['get','put']
    permission_classes = [IsAuthenticated]
    

    def list(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            data  = Profile.objects.all()
            return Response(ProfileSerializer(instance=data,many=True).data,status=status.HTTP_200_OK)
        id = self.request.user.id
        profile =  Profile.objects.filter(client__id=id).first()
        return Response(ProfileSerializer(instance=profile).data,status=status.HTTP_200_OK)
      