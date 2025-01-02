from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
import os
from reportlab.pdfgen import canvas
 


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def generate_pdf_task(self, order_details, total_sum, username, order_id,user_email):
    try:
        # create the name of the file from the name and the order_id
        pdf_filename = f"{username}_order_{order_id}_shop_list.pdf"
        # create a path where the file will be saved
        pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_filename) 
        c = canvas.Canvas(pdf_path)
        c.drawString(100, 800, "Order Details")
        y_position = 750
        for item in order_details:
            c.drawString(100, y_position, f"Item: {item['item']}, Quantity: {item['number_of_items']}, Price: {item['price']}")
            y_position -= 20
        c.drawString(100, y_position - 20, f"Total Amount: {total_sum}")
        c.save()
        
        return {
            'pdf_path': pdf_path,
            'subject': 'Details of your order',
            'message': 'Your order has been placed successfully. Here are the details of your purchase.',
            'address': user_email,
            }
    except Exception as e:
        self.retry(exc=e)


"""
# the first task returns a dictionary that is unpacked and used as 
arguments to the second task

"""


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_client_email_with_pdf(self,task_data):
    try:
        # unpack the data to be used to send the email
        subject = task_data.get('subject')
        message = task_data.get('message')
        address = task_data.get('address')
        path = task_data.get('pdf_path')

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[address],
        )
        # Attach the PDF document
        email.attach_file(path)
        email.send()
        return "Email with PDF sent successfully"
    except Exception as e:
        return f"Error sending email: {e}"












 