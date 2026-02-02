from rest_framework import viewsets, permissions, renderers, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    Unified ViewSet for User management.
    Handles both API endpoints (standard DRF) and the Signup UI.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    def get_permissions(self):
        if self.action in ['create', 'signup']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_renderers(self):
        if self.action == 'signup':
            return [renderers.TemplateHTMLRenderer()]
        return super().get_renderers()

    @action(detail=False, methods=['get', 'post'], renderer_classes=[renderers.TemplateHTMLRenderer])
    def signup(self, request):
        """
        Custom action to render the Signup HTML page.
        """
        if request.method == 'GET':
            form = UserCreationForm()
            return Response({'form': form}, template_name='registration/signup.html')
    
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        return Response({'form': form}, template_name='registration/signup.html')
