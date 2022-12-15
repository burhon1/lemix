from django.core.exceptions import ValidationError

def validate_file_size(value):
    filesize = value.size
    
    if filesize > 5242880:
        raise ValidationError("Fayl hajmiga qo'yilgan cheklov 5Mb")
    else:
        return value