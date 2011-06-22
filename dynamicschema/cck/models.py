from django.db import models

attribute_types =  ( ('String','String'), 
                     ('Integer','Integer'), 
                     ('Decimal', 'Decimal') , 
                     ('Text','Text') , 
                     ('Date', 'Date') , 
                     ('Boolean', 'Boolean') , 
                     ('Email','Email') )

class Schema(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Attribute(models.Model):
    schema           = models.ForeignKey(Schema)
    name             = models.SlugField(max_length = 20)
    label            = models.CharField(max_length = 40)
    datatype         = models.CharField(max_length = 20 ,choices = attribute_types)
    description      = models.TextField()
    field_order      = models.IntegerField()
    hidden_field     = models.BooleanField()
    display_in_table = models.BooleanField()

    def __str__(self):
        return self.label

    class Meta:
        unique_together = ("schema", "name")

class ChoiceList(models.Model):
    attrib  = models.ForeignKey(Attribute) 
    name    = models.CharField(max_length = 30)
    value   = models.CharField(max_length = 30)

    class Meta:
        unique_together = ("attrib", "name", "value")


class Record(models.Model):
    record_type = models.ForeignKey(Schema)

    def __str__(self):
        return str(self.id)


class KeyValueStore(models.Model):
    record      = models.ForeignKey(Record)
    attribute   = models.ForeignKey(Attribute)
    value_text  = models.TextField(blank=True, null=True)
    value_float = models.FloatField(blank=True, null=True)
    value_date  = models.DateField(blank=True, null=True)
    value_bool  = models.NullBooleanField(blank=True)

    class Meta:
        unique_together = ("record", "attribute")

