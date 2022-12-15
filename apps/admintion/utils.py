from typing import Sequence, List
from django.forms.models import model_to_dict
from django.db.models import FileField, ImageField, ManyToManyField, ForeignKey, ManyToOneRel, ManyToManyRel

def convert_to_json(obj, fields):
    """ 
    Use like as: `convert_to_json(lead_obj, fields=('id', 'fio', 'phone', 'file', 'telegram'))`
    `fields` can be `"__all__"`
    """
    data = dict()
    
    if fields == '__all__':
        fields = list(obj._meta.get_fields(include_hidden=False))
        
    if type(fields) in (list, tuple, set):
        field_names, fields = fields, []
        for field in field_names:
            if type(field) is str:
                field = obj._meta.get_field(field)

            if type(field) not in [ManyToManyRel, ManyToOneRel]:
                fields.append(field)
    

    field_names = []
    for field_obj in fields:
        if type(field_obj) in [FileField, ImageField]:
            field_value = field_obj.value_from_object(obj)
            if field_value:
                data[field_obj.name] = {'name': field_value.name, 'url':field_value.url}
            else:
                data[field_obj.name] = None
            fields.remove(field_obj)
        elif type(field_obj) in [ManyToManyField]:
            data[field_obj.name] = list(getattr(obj, field_obj.name).all().values('id',))
        else:
            field_names.append(field_obj.name)
    
    data.update(model_to_dict(obj, field_names))

    return data