from django.shortcuts import get_object_or_404, redirect
from django.db.models import F
from rest_framework import viewsets, permissions, renderers, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ShortURL
from .serializers import ShortURLSerializer

class ShortURLViewSet(viewsets.ModelViewSet):
    """
    Main ViewSet for the Shortener app. 
    This handles EVERYTHING: standard API operations (CRUD), plus the specific 
    UI views like Home, Dashboard, and Redirects using custom actions.
    """
    serializer_class = ShortURLSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return ShortURL.objects.filter(created_by=self.request.user).order_by('-created_at')
        return ShortURL.objects.none()

    def get_permissions(self):
        if self.action in ['redirect_view', 'home']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_renderers(self):
        if self.action in ['home', 'dashboard', 'edit_view', 'delete_view']:
            return [renderers.TemplateHTMLRenderer()]
        return super().get_renderers()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get', 'post'], renderer_classes=[renderers.TemplateHTMLRenderer], permission_classes=[permissions.IsAuthenticated])
    def home(self, request):
        if request.method == 'POST':
            original_url = request.POST.get('original_url')
            custom_code = request.POST.get('short_code')
            expires_in = request.POST.get('expires_in')  # minutes
            
            expires_at = None
            if expires_in:
                from django.utils import timezone
                from datetime import timedelta
                expires_at = timezone.now() + timedelta(minutes=int(expires_in))

            if original_url:
                if custom_code:
                    if ShortURL.objects.filter(short_code=custom_code).exists():
                        return Response({'error': 'This short code is already taken. Please choose another.'}, template_name='shortener/home.html')
                    short_url = ShortURL.objects.create(original_url=original_url, short_code=custom_code, created_by=request.user, expires_at=expires_at)
                else:
                    short_url = ShortURL.objects.create(original_url=original_url, created_by=request.user, expires_at=expires_at)
                
                return Response({'short_url': short_url}, template_name='shortener/home.html')
            return Response({'error': 'Please provide a URL'}, template_name='shortener/home.html')
        return Response({}, template_name='shortener/home.html')

    @action(detail=False, methods=['get'], renderer_classes=[renderers.TemplateHTMLRenderer])
    def dashboard(self, request):
        urls = self.get_queryset()
        return Response({'urls': urls}, template_name='shortener/dashboard.html')

    @action(detail=True, methods=['get', 'post'], renderer_classes=[renderers.TemplateHTMLRenderer])
    def edit_view(self, request, pk=None):
        instance = self.get_object()
        if request.method == 'POST':
            instance.original_url = request.POST.get('original_url')
            instance.save()
            return redirect('dashboard')
        return Response({'object': instance}, template_name='shortener/edit_url.html')

    @action(detail=True, methods=['get', 'post'], renderer_classes=[renderers.TemplateHTMLRenderer])
    def delete_view(self, request, pk=None):
        instance = self.get_object()
        if request.method == 'POST':
            instance.delete()
            return redirect('dashboard')
        return Response({'object': instance}, template_name='shortener/confirm_delete.html')

    @action(detail=False, methods=['get'], url_path='r/(?P<short_code>\w+)', permission_classes=[permissions.AllowAny])
    def redirect_view(self, request, short_code=None):
        """
        Handles the actual redirection. 
        """
        short_url = get_object_or_404(ShortURL, short_code=short_code)
        
        # Check Expiration
        if short_url.expires_at:
            from django.utils import timezone
            if timezone.now() > short_url.expires_at:
                return Response({'error': 'This link has expired.'}, status=status.HTTP_410_GONE, template_name='shortener/home.html')

        ShortURL.objects.filter(pk=short_url.pk).update(clicks=F('clicks') + 1)
        return redirect(short_url.original_url)
