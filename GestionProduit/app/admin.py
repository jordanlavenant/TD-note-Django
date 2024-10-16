from decimal import Decimal
from django.contrib import admin
from .models import Product, ProductItem, Provider, Stock, Command, Status

class ProductItemAdmin(admin.TabularInline):
    model = ProductItem
    filter_vertical = ('attributes',)

class ProductFilter(admin.SimpleListFilter):
    title = 'filtre produit'
    parameter_name = 'custom_status'

    def lookups(self) :
        return (
            ('online', 'En ligne'),
            ('offline', 'Hors ligne'),
        )
    
    def queryset(self, queryset):
        if self.value() == 'online':
            return queryset.filter(status=1)
        if self.value() == 'offline':
            return queryset.filter(status=0)
        
def set_product_online(queryset):
    queryset.update(status=1)
    set_product_online.short_description = "Mettre en ligne"

def set_product_offline(queryset):
    queryset.update(status=0)
    set_product_offline.short_description = "Mettre hors ligne"

def set_product_out_of_stock(queryset):
    queryset.update(status=2)
    set_product_offline.short_description = "Mettre en rupture de stock"

class StatusAdmin(admin.ModelAdmin):
    list_display = ('numero', 'libelle')
    search_fields = ('libelle',)

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_filter = (ProductFilter,)
    inlines = [ProductItemAdmin,]
    date_hierarchy = 'date_creation'
    actions = [set_product_online, set_product_offline, set_product_out_of_stock]
    search_fields = ('name',)
    list_display = ["name", "price_ht", "tax", "status"]
    list_display_links = ["name"]
    list_editable = ["price_ht"]
    
    def tax(self, instance):
        return (instance.price_ht * Decimal('0.2'))
    tax.short_description = "Taxes (€)"
    tax.admin_order_field = "price_ht"

class StatusAdmin(admin.ModelAdmin):
    list_display = ('numero', 'libelle')
    search_fields = ('libelle',)

class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email')
    search_fields = ('name', 'address', 'phone', 'email')

class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'provider', 'quantity', 'rate')
    search_fields = ('product__name', 'provider__name')
    list_filter = ('provider',)

class CommandAdmin(admin.ModelAdmin):
    list_display = ('product', 'provider', 'quantity', 'date', 'status')
    search_fields = ('product__name', 'provider__name')
    list_filter = ('status', 'date')

# Register your models here with the custom admin classes.
admin.site.register(Status, StatusAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Command, CommandAdmin)

# Register your models here.
admin.site.register(ProductItem)