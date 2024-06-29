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
import pandas as pd
from .models import Penilaian, HasilPrediksi
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report

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


def process_data(request):
    # Load the labeled data from the database
    labeled_data = Penilaian.objects.all().values()
    labeled_df = pd.DataFrame(labeled_data)
    
    # Print labeled_df content for debugging
    print("Labeled Data Frame:")
    print(labeled_df.head())  # Print first few rows
    
    # Preprocess the labeled data
    penilaian_columns = ['nilai_absen', 'nilai_jurnal', 'nilai_kuisioner']
    for col in penilaian_columns:
        labeled_df[col] = pd.to_numeric(labeled_df[col], errors='coerce')

    # Encode the STATUS column
    label_encoder = LabelEncoder()
    labeled_df['status'] = label_encoder.fit_transform(labeled_df['status'])
    
    # Split data for training
    X = labeled_df[penilaian_columns]
    y = labeled_df['status']
    
    # Impute missing values
    imputer = SimpleImputer(strategy='mean')
    X = imputer.fit_transform(X)
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Define parameter grid for GridSearchCV
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 5, 10, 15],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    # Initialize RandomForestClassifier model
    model = RandomForestClassifier()
    
    # Perform GridSearchCV
    grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_

    # Load the new data for prediction from the database
    new_data = Penilaian.objects.all().values()
    new_df = pd.DataFrame(new_data)
    
    # Preprocess the new data for prediction
    for col in penilaian_columns:
        new_df[col] = pd.to_numeric(new_df[col], errors='coerce')
    
    # Impute missing values for prediction
    X_new = imputer.transform(new_df[penilaian_columns])

    # Predict using the best model
    y_pred = best_model.predict(X_new)
    new_df['predicted_status'] = label_encoder.inverse_transform(y_pred)

    # Save predictions to HasilPrediksi model
    HasilPrediksi.objects.all().delete()  # Clear previous predictions
    predictions_to_save = []
    for index, row in new_df.iterrows():
        prediction = HasilPrediksi(
            regu=row['regu'],
            penilaian=Penilaian.objects.get(regu=row['regu']),  # Ensure to fetch correct Penilaian instance
            predicted_status=row['predicted_status']
        )
        predictions_to_save.append(prediction)
    HasilPrediksi.objects.bulk_create(predictions_to_save)

    # Display results
    result_html = new_df.to_html()

    return render(request, 'results.html', {'result_html': result_html})
