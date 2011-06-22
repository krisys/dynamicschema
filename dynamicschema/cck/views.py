# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator

from models import Schema, Record , Attribute, KeyValueStore
from forms import *

def create_record(request, id):
    schema = Schema.objects.get(id = id)

    DynamicForm = get_dynamic_form(schema)
    form = DynamicForm(request.POST or None)

    if form.is_valid():
        record_instance = Record.objects.create(record_type = schema)
        attributes = Attribute.objects.filter(schema = schema).exclude(hidden_field = True)
        for attribute in attributes:
            if attribute.datatype in ( 'String', 'Text', 'Email'):
                KeyValueStore.objects.create(record = record_instance, 
                                             attribute = attribute, 
                                             value_text = form.cleaned_data[attribute.name] )
            if attribute.datatype in ('Integer', 'Decimal'):
                KeyValueStore.objects.create(record = record_instance, 
                                             attribute = attribute, 
                                             value_float = form.cleaned_data[attribute.name] )
            if attribute.datatype == 'Date' :
                KeyValueStore.objects.create(record = record_instance, 
                                             attribute = attribute, 
                                             value_date = form.cleaned_data[attribute.name])
            if attribute.datatype == 'Boolean' :
                KeyValueStore.objects.create(record = record_instance, 
                                             attribute = attribute, 
                                             value_bool = form.cleaned_data[attribute.name])

    t = get_template('cck/add_record.html')
    c = RequestContext(request, locals() )
    return HttpResponse(t.render(c))

def edit_record(request, id):
    record = Record.objects.get(id = id)
    attribs =  Attribute.objects.filter(schema = record.record_type)
    dataTypeMap = {'String': 'value_text',
                    'Text' : 'value_text',
                   'Email' : 'value_text',
                  'Integer': 'value_float',
                  'Decimal': 'value_float',
                     'Date': 'value_date',
                 'Boolean' : 'value_bool'}
    data = {}
    for attrib in attribs:
        attrib_value = KeyValueStore.objects.filter(record = record, attribute = attrib)
        if len(attrib_value) == 0:
            attrib_value = None
        else:
            attrib_value = getattr(attrib_value[0], dataTypeMap[attrib.datatype], None)
        data[attrib.name] =  attrib_value
    DynamicForm = get_dynamic_form(record.record_type)
    #form = DynamicForm(initial = data)

    form = DynamicForm(request.POST or None, initial = data)
    if form.is_valid():
        for attribute in attribs:
            keyvalue = KeyValueStore.objects.filter( record  = record, attribute = attribute)
            if attribute.datatype in ('String', 'Text', 'Email'):
                if len(keyvalue) == 0:
                    KeyValueStore.objects.create( record = record, 
                                                  attribute = attribute, 
                                                  value_text = form.cleaned_data[attribute.name])
                else:
                    keyvalue = keyvalue[0]
                    setattr(keyvalue, 'value_text', form.cleaned_data[attribute.name])
            if attribute.datatype in ( 'Integer', 'Decimal'):
                if len(keyvalue) == 0:
                    KeyValueStore.objects.create(record = record, 
                                                 attribute = attribute, 
                                                 value_float = form.cleaned_data[attribute.name])
                else:
                    keyvalue = keyvalue[0]
                    setattr(keyvalue, 'value_float', form.cleaned_data[attribute.name])

            if attribute.datatype == 'Date' :
                if len(keyvalue) == 0:
                    KeyValueStore.objects.create(record = record, 
                                                 attribute = attribute, 
                                                 value_date = form.cleaned_data[attribute.name])
                else:
                    keyvalue = keyvalue[0]
                    setattr(keyvalue, 'value_date', form.cleaned_data[attribute.name])


            if _attribute.datatype == 'Boolean' :
                if len(keyvalue) == 0:
                    KeyValueStore.objects.create(record = record,
                                                 attribute = attribute, 
                                                 value_bool = form.cleaned_data[attribute.name])
                else:
                    keyvalue = keyvalue[0]
                    setattr(_keyvalue, 'value_bool', form.cleaned_data[attribute.name])
            keyvalue.save()

    t = get_template('cck/edit_record.html')
    c = RequestContext(request, locals() )
    return HttpResponse(t.render(c))



def configure_schema(request, id):
    schema = Schema.objects.get(id = id)
    attributes = Attribute.objects.filter(schema = schema).order_by('field_order')
    formset = ConfigureSchemaFormset( request.POST or None, 
                                      queryset = attributes)
    if formset.is_valid():
        formset.save()
    t = get_template('cck/configure_schema.html')
    c = RequestContext(request, locals() )
    return HttpResponse(t.render(c))

def list_records(request,id):
    schema = Schema.objects.get(id = id)

    attribs = Attribute.objects.filter(schema = schema)
    attribs = attribs.exclude( display_in_table = False)
    attribs = attribs.filter(hidden_field = False)
    attribs = attribs.order_by('field_order')

    records = Record.objects.filter( record_type = schema)
    paginator = Paginator (records, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        records= paginator.page(page)
    except (EmptyPage, InvalidPage):
        records= paginator.page (paginator.num_pages)

    temp_list = []
    for record in records.object_list:
        attrib_values = []
        for attrib in attribs:
            attrib_value = KeyValueStore.objects.filter(record = record, 
                                                        attribute = attrib)
            if len(attrib_value) == 0:
                attrib_value = None
            else:
                attrib_value = attrib_value[0]
            attrib_values.append(attrib_value)
        temp_list.append( ( record ,attrib_values) )
    records.object_list = temp_list
    t = get_template('cck/list_records.html')
    c = RequestContext(request, locals() )
    return HttpResponse(t.render(c))


def view_record(request,id):
    record = Record.objects.get(id = id)

    attribs = Attribute.objects.filter(schema = record.record_type)
    attribs = attribs.exclude( display_in_table = False)
    attribs = attribs.filter(hidden_field = False).order_by('field_order')

    attrib_values = []
    for attrib in attribs:
        attrib_value = KeyValueStore.objects.filter(record = record, attribute = attrib)
        if len(attrib_value) == 0:
            attrib_value = None
        else:
            attrib_value = attrib_value[0]
        attrib_values.append(attrib_value)
    record = attrib_values

    t = get_template('cck/view_record.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))

def list_schemas(request):
    schema_list = Schema.objects.all()
    t = get_template('cck/list_schemas.html')
    c = RequestContext(request, locals() )
    return HttpResponse(t.render(c))
