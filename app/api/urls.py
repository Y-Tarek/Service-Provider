from dynamic_rest.routers import DynamicRouter
from .viewsets import *
from rest_framework_simplejwt.views import TokenRefreshView

router = DynamicRouter()

router.register_resource(CountryViewSet)
router.register_resource(RegionViewSet)
router.register_resource(AddressViewSet)
router.register_resource(ProviderTechnicalViewSet)
router.register_resource(ProviderTechnicalTeamViewSet)
router.register_resource(ProviderTypeViewSet)
router.register_resource(ServiceFieldViewSet)
router.register_resource(ServiceProviderViewSet)
router.register_resource(ServiceViewSet)
router.register_resource(SubServiceViewSet)
router.register_resource(ServiceRequirementViewSet)
router.register_resource(ServiceRequirementChoicesViewSet)
router.register_resource(ClientViewSet)
router.register_resource(ServiceRequirementRequestViewSet)
router.register_resource(OfferViewSet)
router.register_resource(ClientOrderViewSet)
router.register_resource(OrderFeedBackViewSet)
router.register('profile',ProfileViewSet)

from django.urls import path
urlpatterns = [
    path('login',AuthLogin.as_view(),name='token'),
    path('token/refresh',TokenRefreshView.as_view(),name='token_refresh')
]


