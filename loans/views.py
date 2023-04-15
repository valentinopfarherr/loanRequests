from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

import requests
import os

from loans.forms import LoanForm
from loans.models import Loan

def index(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)

        if form.is_valid():
            loan = form.save(commit=False)

            if evaluate_request(loan.dni):
                loan.approved = True
                message = 'Your loan application has been approved'
            else:
                loan.approved = False
                message = 'Sorry, your loan application has been rejected'
            
            loan.save()
            return render(request, 'response.html', {'message': message})
        else:
            return render(request, 'loan_form.html', {'form': form})
    else:
        form = LoanForm()
    return render(request, 'loan_form.html', {'form': form})

def evaluate_request(dni):
    headers = {'credential': os.environ.get('CREDENTIAL')}
    url = f'https://api.moni.com.ar/api/v4/scoring/pre-score/{dni}'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return False

    estado = response.json()['status']
    return estado == 'approve'

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin(request):
    if not request.user.is_superuser:
        return redirect('index')
    loans = Loan.objects.all()
    return render(request, 'admin.html', {'loans': loans})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_loan(request, id):
    if not request.user.is_superuser:
        return redirect('index')
    loan = get_object_or_404(Loan, id=id)
    if request.method == 'POST':
        form = LoanForm(request.POST, instance=loan)
        if form.is_valid():
            form.save()
            return redirect('admin')
    else:
        form = LoanForm(instance=loan)
    return render(request, 'edit_loan.html', {'form': form, 'loan': loan})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_loan(request, id):
    if not request.user.is_superuser:
        return redirect('index')
    loan = get_object_or_404(Loan, id=id)
    if request.method == 'POST':
        loan.delete()
        return redirect('admin')
    return render(request, 'delete_loan.html', {'loan': loan})
