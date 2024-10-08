from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Support

class SupportPageView(View):
    def get(self, request):
        return render(request, 'pages/support.html') 

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Lưu thông tin vào database
        support_entry = Support(name=name, email=email, message=message)
        support_entry.save()

        # Nội dung email phản hồi tự động
        subject = 'Cảm ơn bạn đã liên hệ với chúng tôi'
        body = f'Chào {name},\n\nCảm ơn bạn đã gửi yêu cầu hỗ trợ. Chúng tôi sẽ phản hồi bạn sớm nhất có thể.\n\nThông tin của bạn:\n\n- Tên: {name}\n- Email: {email}\n- Lời nhắn: {message}\n\nTrân trọng,\nĐội ngũ hỗ trợ'
        from_email = settings.DEFAULT_FROM_EMAIL

        # Gửi email
        send_mail(
            subject,
            body,
            from_email,  # Email gửi đi
            [email],  # Email khách hàng
            fail_silently=False,
        )

        return redirect('support_page')  # Redirect về trang hỗ trợ

class SupportAPIView(APIView):
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        message = request.data.get('message')

        if not name or not email or not message:
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Lưu thông tin vào database
        support_entry = Support(name=name, email=email, message=message)
        support_entry.save()

        # Nội dung email phản hồi tự động
        subject = 'Cảm ơn bạn đã liên hệ với chúng tôi'
        body = f'Chào {name},\n\nCảm ơn bạn đã gửi yêu cầu hỗ trợ. Chúng tôi sẽ phản hồi bạn sớm nhất có thể.\n\nThông tin của bạn:\n\n- Tên: {name}\n- Email: {email}\n- Lời nhắn: {message}\n\nTrân trọng,\nĐội ngũ hỗ trợ'
        from_email = settings.DEFAULT_FROM_EMAIL

        # Gửi email
        send_mail(
            subject,
            body,
            from_email,  # Email gửi đi
            [email],  # Email khách hàng
            fail_silently=False,
        )
        
        return Response({'message': 'Support request submitted successfully'}, status=status.HTTP_201_CREATED)
