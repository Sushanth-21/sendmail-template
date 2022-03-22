from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.permissions import AllowAny

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@api_view(['POST'])
@permission_classes([AllowAny])
def mail(request):
    try:
        to = request.data["send_to"]
        username = request.data["username"]
        html_content = render_to_string(
            "mail/mail.html", {"username": username})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            "Welcome",
            text_content,
            settings.EMAIL_HOST_USER,
            [to]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        return Response({"message": "mail sent"}, status=HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)}, status=HTTP_403_FORBIDDEN)
