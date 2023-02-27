from django.contrib import admin,messages
from .models import *
import nested_admin
from rangefilter.filters import DateRangeFilter
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from app.utils import *

############## Inlines ###################
class RegionInline(admin.TabularInline):
    model = Region
    extra = 0

class SubServiceInline(nested_admin.NestedStackedInline):
    model = SubService
    extra = 0

class ServiceRequirementChoicesInline(nested_admin.NestedTabularInline):
    model = ServiceRequirementChoices
    extra = 0

class ServiceRequirementInline(nested_admin.NestedStackedInline):
    model = ServiceRequirement
    inlines = [ServiceRequirementChoicesInline]
    extra = 0

class ServiceInline(nested_admin.NestedStackedInline):
    model = Service
    inlines = [ServiceRequirementInline,SubServiceInline]
    extra = 0

class OfferInline(nested_admin.NestedStackedInline):
    model = Offer
    extra = 0
########### End of Inlines ##############

############ forms #####################

class ClientChangeForm(UserChangeForm):
    class Meta:
        model = Client
        fields = '__all__'

######## end of forms ###################


########### Admin Classes ###############

class RegionAdmin(admin.ModelAdmin):
    search_fields = ['city','country__name']
    list_filter=['country__name']
    @admin.display(description="الكود الدولى")
    def get_postal_code(self):
        return self.country.postal_code

    def link_country(self,obj):
        if obj.country:
            link = reverse("admin:app_country_change",args=[obj.country.id])
            return format_html('<a href="{}" style="font-weight:bold;">{}</a>', link, obj.country.name)
        else:
            return None
    link_country.allow_tags = True
    link_country.short_description = "الدولة"
    list_display = ['city','link_country',get_postal_code]

class CountryAdmin(admin.ModelAdmin):
    search_fields = ['postal_code','name']
    inlines = [RegionInline]
    list_display = ['postal_code','name','currency']

class ServiceProviderAdmin(nested_admin.NestedModelAdmin):
    list_display = ['name','commercial_name','owner','type','commercial_record','phone_number','email']
    list_filter = ['type__name']
    search_fields = ['name','commercial_name']
    inlines = [ServiceInline]

class ServiceProviderTechnichalAdmin(admin.ModelAdmin):
    def get_provider_name(self,obj):
        if obj.provider:
            link = reverse("admin:app_serviceprovider_change",args=[obj.provider.id])
            return format_html('<a href="{}" style="font-weight:bold;">{}</a>', link, obj.provider.commercial_name)
        else:
          return None
    get_provider_name.allow_tags = True
    get_provider_name.short_description = 'مزود الخدمة'

    @admin.display(description="مجال الخدمة")
    def get_tech_field(self):
        if self.technical_field.field_name:
           return self.technical_field.field_name
        return None

    list_display = ['technical_name','get_provider_name','mobile',get_tech_field]
    list_filter = ['provider','technical_field']
    autocomplete_fields = ['provider','technical_field']
    search_fields = ['technical_name']

class ServiceProviderTeamAdmin(admin.ModelAdmin):
    @admin.display(description="اسم مزود الخدمة")
    def get_provider_name(self):
        if self.provider.commercial_name:
           return self.provider.commercial_name
        return self.provider.name

    def link_field(self,obj):
        if obj.team_field:
            link = reverse("admin:app_servicefield_change",args=[obj.team_field.id])
            return format_html('<a href="{}" style="font-weight:bold;">{}</a>', link, obj.team_field.field_name)
        else:
            return None
    link_field.allow_tags = True
    link_field.short_description = "مجال الخدمة"

    list_display = [get_provider_name,'link_field','الاسم']
    list_filter = ['provider','team_field']
    filter_horizontal = ['technicals']
    autocomplete_fields = ['team_field','provider','team_region']

class ServiceFieldAdmin(nested_admin.NestedModelAdmin):
    search_fields = ['field_name']
    inlines = [ServiceInline]
    list_display =['field_name']
    

class ServiceAdmin(nested_admin.NestedModelAdmin):
    inlines = [ServiceRequirementInline,OfferInline,SubServiceInline]
    list_per_page = 10
    filter_horizontal = ('region',)
    autocomplete_fields = ['service_field','provider']
    list_filter = ['approaved','service_field__field_name','region']
    search_fields = ['name']
    def link_provider(self,obj):
        if obj.provider:
            link = reverse("admin:app_serviceprovider_change",args=[obj.provider.id])
            return format_html('<a href="{}" style="font-weight:bold;">{}</a>', link, obj.provider.commercial_name)
        else:
            return None
    link_provider.allow_tags = True
    link_provider.short_description = "مزود الخدمة"

    list_display = ['name','link_provider','price','approaved']

class SubServiceAdmin(nested_admin.NestedModelAdmin):
    search_fields = ['name']
    @admin.display(description="الخدمة")
    def get_service(self):
        return self.service.name
    
    @admin.display(description="مزود الخدمة")
    def get_provider(self):
        return self.service.provider.commercial_name

    list_display = ['name','price',get_service,get_provider]
    list_filter = ['service__service_field']
    autocomplete_fields = ['service']
    inlines = [OfferInline]
            

class ServiceRequirementAdmin(admin.ModelAdmin):
    search_fields = ['name','display_name']
    autocomplete_fields = ['service','reference']
    inlines = [ServiceRequirementChoicesInline]

    @admin.display(description="الخدمة الخاصة بها")
    def get_service_name(self):
      return self.service.name

    @admin.display(description="الخدمة الفرعية الخاصة بها")
    def get_sub_service_name(self):
      return self.reference.name

    @admin.display(description="مزود الخدمة")
    def get_provider_name(self):
      if not self.service:
        return self.reference.provider.name
      else:
        return self.service.provider.name

    list_display = ['name','display_name',get_service_name,get_sub_service_name,get_provider_name]

class ServiceRequirementChoicesAdmin(admin.ModelAdmin):
    @admin.display(description="اسم المتطلب")
    def get_requirement_name(self):
        if self.requirement.display_name:
           return self.requirement.display_name
        return self.requirement.name

    @admin.display(description="الخدمة")
    def get_service(self):
        return self.requirement.service.name

    autocomplete_fields = ['requirement']
    list_display = [get_requirement_name,'choice',get_service]
    list_filter = ['requirement__service__name']



class ClientAdmin(UserAdmin):
    list_display = ['name','mobile','email','address']
    search_fields = ['name']
    form = ClientChangeForm
    fieldsets = (
        (None, {"fields": ("mobile", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "name",
                    "username",
                    "email",
                    "address",
                    "type",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = ("last_login", "date_joined")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("mobile", "name", "password1", "password2"),
            },
        ),
    )

class ClientOrderAdmin(admin.ModelAdmin):
    @admin.display(description="رقم هاتف العميل")
    def get_client_phone(self):
        if self.client.mobile:
           return self.client.mobile
        return None

    def get_service(self,obj):
        redirect = OrderRiderct.redirect_to_service(obj)
        link = reverse(redirect['str'],args=[redirect['id']])
        return format_html('<a href="{}" style="font-weight:bold;">{}</a>', link, redirect['name'])
    get_service.allow_tags = True
    get_service.short_description = 'الخدمة'
    date_hierarchy = 'desired_date'

    def link_client(self,obj):
        if obj.client:
            link = reverse("admin:app_client_change",args=[obj.client.id])
            return format_html('<a href="{}" style="font-weight:bold;">{}</a>', link, obj.client.name)
        else:
            return None
    link_client.allow_tags = True
    link_client.short_description = "العميل"

    list_display = ['id','link_client',get_client_phone,'get_service','status','price','desired_date']
    autocomplete_fields = ['client','service','technical_name']
    list_filter = [('desired_date',DateRangeFilter)]
    def get_rangefilter_desired_date_default(self, request):
        return ("التوقيت من", "حتى")
    
class OrderFeedBackAdmin(admin.ModelAdmin):
    autocomplete_fields = ['client']

    @admin.display(description="العميل")
    def get_client_name(self):
        return self.client.name
    

    list_display = [get_client_name,'comment','rate','order']

class ServiceRequirementRequestAdmin(admin.ModelAdmin):
    @admin.display(description="المتطلب")
    def get_requirement(self):
        if  self.requirement.display_name:
            return self.requirement.display_name
        return self.requirement.name

    @admin.display(description="العميل")
    def get_client(self):
        if  self.client.name:
            return self.client.name
        return None

    list_display = [get_requirement,get_client,'answer']
    list_filter = ['requirement__service__name']
    autocomplete_fields = ['client']

class OfferAdmin(nested_admin.NestedModelAdmin):
    def link_service(self,obj):
            redirect = OfferRiderct.redirect_to_service(obj)
            link = reverse(redirect['str'],args=[redirect['id']])
            return format_html('<a href="{}" style="font-weight:bold;">{}</a>', link, redirect['name'])
        
    link_service.allow_tags = True
    link_service.short_description = "الخدمة"
    
    def expired_offer(self,obj):
        return obj.expired

    expired_offer.boolean = True
    expired_offer.short_description = "منتهى"

    list_display = ['created_at','link_service','offer_price','expiration_date','expired_offer']
    list_filter = [('created_at', DateRangeFilter),('expiration_date', DateRangeFilter),'service','sub_service',]
    autocomplete_fields = ['service','sub_service']

    def get_rangefilter_created_at_default(self, request):
        return ("التوقيت من", "حتى")

    def get_rangefilter_expiration_date_default(self, request):
        return ("التوقيت من", "حتى")


class AddressAdmin(admin.ModelAdmin):
    @admin.display(description="المدينة")
    def get_city(self):
        if self.region:
           return self.region.city
        return None
    list_display = [get_city,'st_name','block_num','floor','apartment_num']

########## End Of Admin Classes ################



admin.site.register(Country,CountryAdmin)
admin.site.register(Region,RegionAdmin)
admin.site.register(ProviderType)
admin.site.register(ServiceField,ServiceFieldAdmin)
admin.site.register(ServiceProvider,ServiceProviderAdmin)
admin.site.register(ProviderTechnical,ServiceProviderTechnichalAdmin)
admin.site.register(ProviderTechnicalTeam,ServiceProviderTeamAdmin)
admin.site.register(Service,ServiceAdmin)
admin.site.register(Client,ClientAdmin)
admin.site.register(ClientOrder,ClientOrderAdmin)
admin.site.register(OrderFeedBack,OrderFeedBackAdmin)
admin.site.register(ServiceRequirementRequest,ServiceRequirementRequestAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Offer,OfferAdmin)
admin.site.register(SubService,SubServiceAdmin)
# admin.site.register(ServiceRequirement,ServiceRequirementAdmin)
# admin.site.register(ServiceRequirementChoices,ServiceRequirementChoicesAdmin)




# Register your models here.
