from django.core.files.base import ContentFile
import io
import qrcode 

def create_qrcode(data: str, lead_form):
    image = io.BytesIO()
    qr = qrcode.QRCode()
    qr.add_data(data)
    img = qr.make_image()
    img.save(image, format="PNG", quality=100)
    img_content = ContentFile(image.getvalue(), f'{lead_form.id}.png')
    lead_form.qrcode = img_content
    lead_form.link = data
    lead_form.save()

    return lead_form