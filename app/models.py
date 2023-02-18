from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator
from ckeditor.fields import RichTextField
from app.utils import get_order_price,check_same_order
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

class TimestampedModel(models.Model):
    """
    Abstract model to contain information about creation/update time.

    :created_at: date and time of record creation.
    :updated_at: date and time of any update happends for the record.
    """

    created_at = models.DateTimeField(
        verbose_name='وقت الانشاء', auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name='وقت التعديل', auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']

class Country(TimestampedModel):
    name = models.CharField(max_length=250,verbose_name='الدولة')
    postal_code = models.CharField(max_length=250,verbose_name='كود الدولة')
    currency = models.CharField(max_length=250,verbose_name='العملة',null=True,blank=True)

    class Meta:
       verbose_name = 'دولة'
       verbose_name_plural = 'الدول'

    def __str__(self):
        return f'{self.postal_code} | {self.name}'

class Region(TimestampedModel):
    city = models.CharField(max_length=250,verbose_name="المدينة")
    country = models.ForeignKey(Country,verbose_name='الدولة',on_delete=models.PROTECT,related_name='المدن')
    class Meta:
       verbose_name = 'منطقة الخدمة'
       verbose_name_plural = 'مناطق الخدمات'

    def __str__(self):
        return f'{self.city} | {self.country.name}'

class Address(TimestampedModel):
    region = models.ForeignKey(Region,on_delete=models.PROTECT,
                               verbose_name='المنطقة',related_name='addresses')
    neighborhood = models.CharField(max_length=250,verbose_name='الحى',null=True,blank=True)
    st_name = models.CharField(verbose_name='اسم الشارع',max_length=250)
    block_num = models.IntegerField(verbose_name='رقم المبنى')
    floor = models.IntegerField(verbose_name='الطابق')
    apartment_num = models.IntegerField(verbose_name='رقم الشقة')

    class Meta:
        verbose_name = 'عنوان'
        verbose_name_plural='العناوين'
    def __str__(self):
        return f' {self.region.city} | {self.st_name} | {self.block_num} | {self.floor} | {self.apartment_num} '
    

class ProviderType(TimestampedModel):
    name = models.CharField(max_length=60,verbose_name='الاسم')
    class Meta:
        verbose_name = 'نوع مزود خدمة'
        verbose_name_plural = 'أنواع مزودين الخدمات'

    def __str__(self):
        return self.name

class ServiceField(TimestampedModel):
    field_name = models.CharField(max_length=250,verbose_name='اسم المجال')
    class Meta:
        verbose_name = 'مجال خدمة'
        verbose_name_plural = 'مجالات الخدمات'
    def __str__(self):
        return self.field_name


class ServiceProvider(TimestampedModel):
    name = models.CharField(max_length=250,verbose_name='الاسم')
    commercial_name = models.CharField(max_length=250,verbose_name='الاسم التجارى',blank=True,null=True,unique=True)
    owner = models.CharField(max_length=250,verbose_name='اسم المالك')
    type = models.ForeignKey(ProviderType,on_delete=models.PROTECT,verbose_name='نوع مزود الخدمة',related_name='providers')
    commercial_record  = models.BooleanField(verbose_name='لدى سجل تجارى')
    phone_number = PhoneNumberField(verbose_name='رقم التواصل',unique=True)
    email = models.EmailField(verbose_name='البريد الالكترونى',
                              max_length=254, blank=True, null=True)

    class Meta:
        verbose_name = 'مزود خدمة'
        verbose_name_plural = 'مزودين الخدمات'
    def __str__(self):
        if self.commercial_name:
            return self.commercial_name
        return self.name

class ProviderTechnical(TimestampedModel):
    technical_name = models.CharField(max_length=200,verbose_name='اسم الفنى')
    mobile = PhoneNumberField(verbose_name='رقم التواصل')
    technical_field = models.ForeignKey(ServiceField,on_delete=models.PROTECT,
                                       verbose_name='المجال التابع له',null=True,blank=True,related_name='technicals')
    technical_region = models.ForeignKey(Region,on_delete=models.PROTECT,
                                         verbose_name='المكان التابع له',null=True,blank=True,related_name='technicals')
    provider = models.ForeignKey(ServiceProvider,on_delete=models.PROTECT,
                                verbose_name='مزود الخدمة التابع له',related_name='technicals')
    class Meta:
        verbose_name = 'فنى'
        verbose_name_plural = 'الفنين'

    def __str__(self):
        return self.technical_name

class ProviderTechnicalTeam(TimestampedModel):
    technicals = models.ManyToManyField(ProviderTechnical,verbose_name='الفنين')
    team_field = models.ForeignKey(ServiceField,on_delete=models.PROTECT,
                                  verbose_name='المجال التابع له',null=True,blank=True,related_name='teams')
    team_region = models.ForeignKey(Region,on_delete=models.PROTECT,
                                         verbose_name='المكان التابع له',null=True,blank=True,related_name='teams')
    provider = models.ForeignKey(ServiceProvider,on_delete=models.PROTECT,
                                verbose_name='مزود الخدمة التابع له',related_name='teams')
    @property
    def الاسم(self):
        return f' فريق {self.team_field}-{self.team_region.city}'


    class Meta:
        verbose_name = 'فريق من الفنين'
        verbose_name_plural = 'فرق من الفنين'

    def __str__(self):
        return f'{self.team_region} | {self.team_field}'

class ServiceData(models.Model):
    name = models.CharField(max_length=250,verbose_name='اسم الخدمة')
    price = models.DecimalField(max_digits=6, decimal_places=2,
                                verbose_name='السعر', default=0, validators=[MinValueValidator(0.0)],null=True,blank=True)
    description = models.TextField(blank=True, null=True, verbose_name='الوصف')
    content = RichTextField(verbose_name='المحتوى',null=True,blank=True)

    class Meta:
        abstract = True

class Service(TimestampedModel,ServiceData):
    service_field = models.ForeignKey(ServiceField,on_delete=models.PROTECT,verbose_name='مجال الخدمة',null=True,blank=True,related_name='services')
    region = models.ManyToManyField(Region,verbose_name='المناطق',related_name='الخدمات')
    provider = models.ForeignKey(ServiceProvider,on_delete=models.PROTECT,verbose_name='المزود',related_name='services')
    approaved = models.BooleanField(verbose_name='مفعلة',null=True,blank=True)
    class Meta:
        verbose_name = 'خدمة'
        verbose_name_plural = 'الخدمات'
    def __str__(self):
        if self.service_field:
            return f'{self.name} | {self.service_field.field_name}'
        return self.name

class SubService(TimestampedModel,ServiceData):
   service = models.ForeignKey(Service,on_delete=models.PROTECT,verbose_name='الخدمة',related_name='subservices')

   class Meta:
        verbose_name = 'خدمة فرعية' 
        verbose_name_plural = ' الخدمات الفرعية' 
        
   def clean(self):
         from django.core.exceptions import ValidationError
         if not self.service.approaved:
            raise ValidationError('لا يمكن انشاء خدمة فرعية و الخدمة الاساسية غير موافق عليها')
         return super(SubService,self).clean()

   def save(self, *args, **kwargs):
        if not self.service.approaved:
            self.full_clean()
        return super(SubService,self).save(*args,**kwargs)

   def __str__(self):
        return f'{self.name} | {self.service.name}'

class ServiceRequirement(TimestampedModel):
    service = models.ForeignKey(Service,on_delete=models.PROTECT,verbose_name="الخدمة",related_name='requirements',null=True,blank=True)
    reference = models.ForeignKey(SubService,on_delete=models.PROTECT,
                                  null=True,blank=True,verbose_name='خاص بالخدمة الفرعية',related_name='sub_requirements')
    name = models.CharField(verbose_name='اسم المتطلب',max_length=250)
    display_name = models.CharField(verbose_name='الاسم المعروض للعميل',max_length=255,null=True,blank=True)

    class Meta:
        verbose_name = 'متطلب خدمة'
        verbose_name_plural='متطلبات الخدمات'

    def __str__(self):
        if self.display_name:
            return f'{self.display_name}'
        return self.name


class ServiceRequirementChoices(TimestampedModel):
    requirement = models.ForeignKey(ServiceRequirement,
                         on_delete=models.PROTECT,verbose_name='المتطلب',related_name='choices',null=True,blank=True)
    choice = models.CharField(verbose_name='الاختيار المعروض للعميل',max_length=255)

    class Meta:  
        verbose_name = 'اجابة مسموحة للمتطلب'
        verbose_name_plural=' اجابات مسموحة للمتطلبات '
    def __str__(self):
         return self.requirement.display_name

class Client(AbstractUser,TimestampedModel):
    clinet_types = (
        (1,'client'),
        (2,'provider'),
        (3,'admin'),
    )
    name = models.CharField(verbose_name="الاسم",max_length=250,null=True,blank=True)
    mobile = PhoneNumberField(verbose_name='رقم الهاتف',unique=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    email = models.EmailField(verbose_name="البريد الالكترونى",null=True,blank=True,max_length=254)
    address = models.ForeignKey(Address,on_delete=models.PROTECT,verbose_name="العنوان",null=True,blank=True)
    type = models.IntegerField(choices=clinet_types,verbose_name="نوع العميل",default=1)
    class Meta:
        verbose_name = 'عميل'
        verbose_name_plural = 'العملاء'

    def __str__(self):
        if self.name:
            return f'{self.name} | {self.mobile}'
        return self.mobile
    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = ["name"]
    objects = CustomUserManager()

class Profile(models.Model):
    client = models.OneToOneField(Client,on_delete=models.PROTECT,verbose_name='العميل')

    def __str__(self):
        return self.client.name


class Offer(TimestampedModel):
    offer_price = models.DecimalField(max_digits=6, decimal_places=2,
                                verbose_name='السعر', default=0, validators=[MinValueValidator(0.0)],null=True,blank=True)
    service = models.ForeignKey(Service,on_delete=models.PROTECT,
                              verbose_name='الخدمة',null=True,blank=True,related_name='offers')

    sub_service = models.ForeignKey(SubService,on_delete=models.PROTECT,
                              verbose_name='خدمة فرعية',null=True,blank=True,related_name='offers')

    expiration_date = models.DateTimeField(verbose_name='وقت الانتهاء')

    @property
    def expired(self):
        from django.utils import timezone
        if timezone.now() >= self.expiration_date:
            return True
        return False

    class Meta:
        verbose_name = 'عرض' 
        verbose_name_plural =  'العروض'

    def __str__(self):
        if self.service:
          return f'{self.service.name} | {self.offer_price}'
        else:
            return f'{self.sub_service.name} | {self.offer_price}'

class ClientOrder(TimestampedModel):
    statusChoices = (
        (1,'تمت العملية بنجاح'),
        (2,'تمت الموافقة على الطلب '),
        (3,'تم ارسال الطلب و هو الان تحت المراجعة '),
        (4,'تم رفض الطلب'),
        (5,'تم الغاء الطلب بناءا على رغبة العميل '),
    )
    client = models.ForeignKey(Client,on_delete=models.PROTECT,verbose_name='العميل')
    service = models.ForeignKey(Service,on_delete=models.PROTECT,verbose_name='الخدمة المطلوبة',null=True,blank=True)
    sub_service = models.ForeignKey(SubService,on_delete=models.PROTECT,
                              verbose_name='الخدمة الفرعية المطلوية',related_name='orders',null=True,blank=True)
    offer = models.ForeignKey(Offer,on_delete=models.PROTECT,
                              verbose_name='العرض',related_name='orders',null=True,blank=True)
    status = models.IntegerField(verbose_name='حالة الطلب',choices=statusChoices,default=3)
    cancel_order = models.BooleanField(verbose_name='الغاء الطلب',null=True,blank=True)
    technical_name = models.ForeignKey(ProviderTechnical,on_delete=models.PROTECT,
                                      verbose_name=' الفنى ',max_length=250,blank=True,null=True,related_name='orders')
    team_name =  models.ForeignKey(ProviderTechnicalTeam,on_delete=models.PROTECT,
                                      verbose_name=' فريق الفنين ',max_length=250,blank=True,null=True,related_name='orders')
    contact_mobile = PhoneNumberField(verbose_name = 'رقم التواصل',null=True,blank=True)  
    address = models.ForeignKey(Address,verbose_name='العنوان',on_delete=models.PROTECT,related_name='addresses')
    price = models.DecimalField(max_digits=6, decimal_places=2,
                                verbose_name='السعر', default=0, validators=[MinValueValidator(0.0)],null=True,blank=True)
    notes = models.TextField(verbose_name='ملاحظات',null=True,blank=True)
    desired_date = models.DateTimeField(verbose_name= 'الميعاد',blank=True,null=True)
   
    @property
    def feedback_permission(self):
        if self.status == 1:
            return True
        else:
            return False

    @property
    def cancel_order_permission(self):
        if self.status in  [1,2,4]:
            return False
        return True

    
    class Meta:
         verbose_name = 'طلب العميل'
         verbose_name_plural = 'طلبات العملاء'
    
    def __str__(self):
        return f'{self.client.mobile}  | {self.status}'
    
    def save(self, *args,**kwargs):
        if self._state.adding:
            count = check_same_order(self)
            if count != 0:
                raise ValueError('تم طلب الخدمة مسبقا')
            self.price = get_order_price(self)
            if not self.price:
                raise ValueError('لا يمكن الاشتراك  هذا العرض منتهى')
        else: 
            if self.cancel_order:
                self.status = 5
                
            if  self.cancel_order and self.status == 2:
                raise ValueError('تم الغاء الطلب من العميل لا يمكن قبوله')

        return super(ClientOrder,self).save(*args,**kwargs)

class ServiceRequirementRequest(TimestampedModel):
    requirement = models.ForeignKey(ServiceRequirement,
                         on_delete=models.PROTECT,verbose_name='المتطلب',null=True,blank=True)
    answer = models.CharField(max_length=255,verbose_name='الاجابة')
    
    client = models.ForeignKey(Client,on_delete=models.PROTECT,verbose_name='العميل',related_name='requirments_requests')

    order = models.ForeignKey(ClientOrder,on_delete=models.PROTECT,
                              verbose_name="المتطلبات الخاصة بالطلب",null=True,blank=True,related_name="order_requirements_requests")

    class Meta:
        verbose_name = ' اجابة متطلب خدمة' 
        verbose_name_plural='اجابات متطلبات الخدمات'

    def __str__(self):
        return f'{self.answer} | {self.requirement.display_name} | {self.client.name}'

class FeedBack(TimestampedModel):
    rate_choices = (
        (1,'very bad'),
        (2,'Bad'),
        (3,'Good'),
        (4,'very good'),
        (5,'Exclent')
    )
    client = models.ForeignKey(Client,on_delete=models.PROTECT,verbose_name='العميل',related_name='feedbacks')
    comment = models.CharField(max_length=355,verbose_name='التعليق',null=True,blank=True)
    rate = models.IntegerField(verbose_name='التقييم',choices=rate_choices,null=True,blank=True)

    class Meta:
        abstract = True
        verbose_name = 'تقييم'
        verbose_name_plural = 'التقيمات'

    def __str__(self):
        if not self.comment:
          return f'{self.rate} | {self.client.name}' 

        return f'{self.rate} | {self.comment} | {self.client.name}' 


class OrderFeedBack(FeedBack):
    order = models.ForeignKey(ClientOrder,on_delete=models.PROTECT,
                                verbose_name='الطلب',related_name='feedbacks')
        

    class Meta:
        verbose_name = ' تقييم طلب العميل' 
        verbose_name_plural = 'تقييمات طلبات العملاء'

    def save(self,*args,**kwargs):
        if self._state.adding:
            if self.order.status != 1:
                raise ValueError('لا يمكن التقييم الا بعد انتهاء الخدمة')
        return super(OrderFeedBack,self).save(*args,**kwargs)

   
# Signals
@receiver(post_save, sender=Client)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(client=instance)

@receiver(post_save, sender=Client)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
