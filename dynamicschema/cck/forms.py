from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from models import Attribute, Schema
from django.forms.extras.widgets import SelectDateWidget

def get_field_from_type(field_type):
    fieldMap = {'String': forms.CharField(max_length = 100),
                'Integer' : forms.IntegerField(),
                'Decimal' : forms.DecimalField(),
                'Text': forms.CharField(widget = forms.Textarea( attrs= {'rows': 4, 'cols':70})),
                'Date' : forms.DateField(widget = SelectDateWidget()),
                'Boolean' : forms.BooleanField(),
                'Email' : forms.EmailField()
                }
    return fieldMap[field_type]

def get_dynamic_form(schema_instance):
    attribs = Attribute.objects.filter(schema = schema_instance)
    attribs = attribs.exclude(hidden_field=True)
    attribs = attribs.order_by('field_order')

    class _DynamicForm(forms.Form):
        def __init__(self,  *args, **kwargs):
            super(_DynamicForm, self).__init__(*args, **kwargs)
            for field in attribs:
                self.fields[field.name] = get_field_from_type(field.datatype)
                self.fields[field.name].label = field.label
                self.fields[field.name].widget.attrs['class'] = 'text'
                self.fields[field.name].widget.attrs['help_text'] = field.description
    return _DynamicForm


class ConfigureSchemaForm(forms.ModelForm):
    class Meta:
        model = Attribute
        exclude = ('schema', 'name', 'datatype')
    def __init__(self, *args, **kwargs):
        super(ConfigureSchemaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'text'

ConfigureSchemaFormset = modelformset_factory(Attribute, ConfigureSchemaForm, extra = 0)


