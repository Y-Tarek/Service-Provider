
class Riderct():
    str = ''
    id  = None
    name = ''
   
    class Meta:
        abstract = True

    def redirect_to_service(obj):
        # Logic of redirecting to either service or subservice or offer in admin
            pass

    def redirect_to_technical(obj):
     # Logic to redirect either to technical or team in admin
        pass



class OrderRiderct(Riderct):
    def redirect_to_service(obj):
        if obj.offer:
                str = 'admin:app_offer_change'
                id = obj.offer.id
                name = obj.offer.sub_service.name if obj.offer.sub_service else obj.offer.service.name

        elif obj.sub_service:
            str = 'admin:app_subservice_change'
            id = obj.sub_service.id
            name = obj.sub_service.name
        else:
            str = 'admin:app_service_change'
            id = obj.service.id
            name = obj.service.name

        return {
            'id':id,
            'str':str,
            'name':name
    }

    def redirect_to_technical(obj):
        if not obj.order.team_name:
              id = obj.order.technical_name.id
              str = 'admin:app_providertechnical_change'   
              name = obj.order.technical_name.technical_name
        else:
            id = obj.order.team_name.id
            str = 'admin:app_providertechnicalteam_change'   
            name = obj.order.team_name.team_name
        
        return {
            'id':id,
            'str':str,
            'name':name
       }

class OfferRiderct(Riderct):
    def redirect_to_service(obj):
        if obj.sub_service:
            str = 'admin:app_subservice_change'
            id = obj.sub_service.id
            name = obj.sub_service.name
        else:
            str = 'admin:app_service_change'
            id = obj.service.id
            name = obj.service.name

        return {
            'id':id,
            'str':str,
            'name':name
    }

def get_order_price(self):
    if self.offer:
        if self.offer.expired:
            return None
        self.price = self.offer.offer_price
    elif self.sub_service:
        self.price = self.sub_service.price
    else:
        self.price = self.service.price

    return self.price

def check_same_order(self):    
    from app.models import ClientOrder
    orders = ClientOrder.objects.filter(service=self.service,sub_service=self.sub_service,
                                        offer=self.offer,client=self.client,status__in=[2,3])
    return orders.count()
