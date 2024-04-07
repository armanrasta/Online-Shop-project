from django.core.mail import send_mail
from django.http import HttpResponse

def send_welcome_email(request):
    subject = 'Welcome to My Site'
    message = 'Thank you for creating an account!'
    from_email = 'armanrostami1000@gmail.com'
    recipient_list = [request.user.email]
    send_mail(subject, message, from_email, recipient_list)
    return HttpResponse("Welcome email sent successfully!")