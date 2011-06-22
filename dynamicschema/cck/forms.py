from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from models import Attribute, Schema
from django.forms.extras.widgets import SelectDateWidget


def get_field_from_type(field_type):
    text_area_widget = forms.Textarea(attrs={'rows': 4, 'cols': 70})

    fieldMap = {'String': forms.CharField(max_length=100),
                'Integer': forms.IntegerField(),
                'Decimal': forms.DecimalField(),
                'Text': forms.CharField(widget=text_area_widget),
                'Date': forms.DateField(widget=SelectDateWidget()),
                'Boolean': forms.BooleanField(),
                'Email': forms.EmailField()
                }
    return fieldMap[field_type]


def get_dynamic_form(schema_instance):
    fields = Attribute.objects.filter(schema=schema_instance)
    fields = fields.exclude(hidden_field=True)
    fields = fields.order_by('field_order')

    class _DynamicForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super(_DynamicForm, self).__init__(*args, **kwargs)
            for f in fields:
                self.fields[f.name] = get_field_from_type(f.datatype)
                self.fields[f.name].label = f.label
                self.fields[f.name].widget.attrs['class'] = 'text'
                self.fields[f.name].widget.attrs['help_text'] = f.description
    return _DynamicForm


class ConfigureSchemaForm(forms.ModelForm):
    class Meta:
        model = Attribute
        exclude = ('schema', 'name', 'datatype')

    def __init__(self, *args, **kwargs):
        super(ConfigureSchemaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'text'

ConfigureSchemaFormset = modelformset_factory(Attribute,
                                              ConfigureSchemaForm, extra=0)
