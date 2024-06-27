from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout, login
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from dashboard.forms import CustomAdminLoginForm
from django.contrib.auth.decorators import login_required

# Custom 403 Forbidden view
def custom_permission_denied_view(request, exception=None):
    message = "Anda tidak memiliki izin untuk mengakses halaman ini."
    return HttpResponseForbidden(render(request, '403.html', {'message': message}))

# Custom Admin Login View
class CustomAdminLoginView(auth_views.LoginView):
    success_url = reverse_lazy('dashboard')  
    def form_valid(self, form):
        response = super().form_valid(form)
        
        if self.request.session.get('admin_login_next'):
            next_url = self.request.session.pop('admin_login_next')
            return HttpResponseRedirect(next_url)
        return response

@login_required 
def dashboard(request):
    
    messages.success(request, 'welcome, admin!')
    return render(request, 'dashboard.html')

@never_cache
def user_logout(request):
    logout(request)
    return redirect(reverse('admin'))  

def admin_login(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('dashboard')  

    # Handle login form submission
    if request.method == 'POST':
        form = CustomAdminLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  
    else:
        form = CustomAdminLoginForm()

    return render(request, 'admin.html', {'form': form})
