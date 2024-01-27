from django.shortcuts import render,redirect
from .models import Case
from .forms import CaseForm,SuperuserEditForm  # Create a form for case creation if not already done
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail


@login_required
def case_list(request):
    if request.user.is_superuser:
        # If the logged-in user is a superuser, show all cases
        cases = Case.objects.all()
    else:
        # If the logged-in user is not a superuser, show cases associated with that user
        cases = Case.objects.filter(client=request.user.id)
    return render(request, 'case_management/case_list.html', {'cases': cases})

@login_required
def case_detail(request, case_id):
    case = Case.objects.get(pk=case_id)
    superuser_edit_form = None  # Initialize the form as None

    # Check if the user is a superuser
    if request.user.is_superuser:
        if request.method == 'POST':
            superuser_edit_form = SuperuserEditForm(request.POST, instance=case)
            if superuser_edit_form.is_valid():
                # case.previous_hearing = case.next_hearing
                # case.save()
                # Update the next_hearing date and previous_hearing date
                case.previous_hearing = case.next_hearing
                case.next_hearing = superuser_edit_form.cleaned_data['hearing_date']
                case.save()
        else:
            superuser_edit_form = SuperuserEditForm(instance=case)

    return render(request, 'case_management/case_details.html', {'case': case, 'superuser_edit_form': superuser_edit_form})

@login_required
def create_case(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            form.save()
            # new_case_created.send(sender=Case, instance=case)
            return redirect('case_list')
    else:
        form = CaseForm()

    return render(request, 'case_management/create_case.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("i am logged in right???")
            return redirect('case_list')  # Redirect to the case list view after login
        else:
            print("somethong wrng occrus")
    return render(request, 'case_management/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')  # Redirect to the login view after logout

@login_required
def search_cases(request):
    search_term = request.GET.get('search_term')
    if request.user.is_superuser:
        # Admin can search all cases
        cases = Case.objects.filter(case_number__icontains=search_term)
    else:
        # Normal users can only search their own cases
        cases = Case.objects.filter(client=request.user, case_number__icontains=search_term)

    return render(request, 'case_management/search_results.html', {'cases': cases})

# def index(request):
#     return render(request, 'case_management/index.html')

