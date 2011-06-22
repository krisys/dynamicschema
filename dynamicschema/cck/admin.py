from django.contrib import admin
from dynamicschema.cck.models import *



class AttributeInline(admin.TabularInline):
    model = Attribute

class ChoiceInline(admin.TabularInline):
    model = ChoiceList

class SchemaAdmin(admin.ModelAdmin):
    inlines = [AttributeInline]

admin.site.register(Schema, SchemaAdmin)

class AttributeAdmin(admin.ModelAdmin):
    list_display = ('schema', 'name', 'label', 'datatype')
    inlines = [ChoiceInline]

admin.site.register(Attribute, AttributeAdmin)

class KeyValueStoreInline(admin.TabularInline):
    model = KeyValueStore

class RecordAdmin(admin.ModelAdmin):
    inlines = [KeyValueStoreInline]

admin.site.register(Record, RecordAdmin)

class ChoiceListAdmin(admin.ModelAdmin):
    pass

admin.site.register(ChoiceList, ChoiceListAdmin)

class KeyValueStoreAdmin(admin.ModelAdmin):
    pass

admin.site.register(KeyValueStore, KeyValueStoreAdmin)
    

