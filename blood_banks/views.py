from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from .models import BloodBank, BloodInventory
from .forms import BloodBankForm, BloodInventoryForm
from donors.models import DonorProfile, DonationHistory
from blood_requests.models import BloodRequest
from accounts.models import User


@login_required
def admin_dashboard(request):
    """Admin dashboard view"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    # Get statistics
    total_donors = DonorProfile.objects.count()
    available_donors = DonorProfile.objects.filter(is_available=True).count()
    total_blood_banks = BloodBank.objects.filter(is_active=True).count()
    pending_requests = BloodRequest.objects.filter(status='pending').count()
    pending_donations = DonationHistory.objects.filter(status='pending').count()
    
    # Blood inventory by group
    blood_inventory = BloodInventory.objects.values('blood_group').annotate(
        total_units=Sum('units_available')
    ).order_by('blood_group')
    
    # Recent blood requests
    recent_requests = BloodRequest.objects.all().order_by('-requested_date')[:5]
    
    # Recent donations
    recent_donations = DonationHistory.objects.all().order_by('-created_at')[:5]
    
    # Donor statistics by blood group
    donors_by_blood_group = DonorProfile.objects.values('blood_group').annotate(
        count=Count('id')
    ).order_by('blood_group')
    
    context = {
        'total_donors': total_donors,
        'available_donors': available_donors,
        'total_blood_banks': total_blood_banks,
        'pending_requests': pending_requests,
        'pending_donations': pending_donations,
        'blood_inventory': blood_inventory,
        'recent_requests': recent_requests,
        'recent_donations': recent_donations,
        'donors_by_blood_group': donors_by_blood_group,
    }
    
    return render(request, 'blood_banks/admin_dashboard.html', context)


@login_required
def blood_bank_list(request):
    """List all blood banks"""
    if request.user.user_type != 'admin':
        # Show all active blood banks to donors
        blood_banks = BloodBank.objects.filter(is_active=True)
    else:
        # Show all blood banks to admin
        blood_banks = BloodBank.objects.all()
    
    return render(request, 'blood_banks/blood_bank_list.html', {'blood_banks': blood_banks})


@login_required
def blood_bank_create(request):
    """Create new blood bank (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    if request.method == 'POST':
        form = BloodBankForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blood bank created successfully!')
            return redirect('blood_bank_list')
    else:
        form = BloodBankForm()
    
    return render(request, 'blood_banks/blood_bank_form.html', {'form': form, 'action': 'Create'})


@login_required
def blood_bank_update(request, pk):
    """Update blood bank (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    blood_bank = get_object_or_404(BloodBank, pk=pk)
    
    if request.method == 'POST':
        form = BloodBankForm(request.POST, instance=blood_bank)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blood bank updated successfully!')
            return redirect('blood_bank_list')
    else:
        form = BloodBankForm(instance=blood_bank)
    
    return render(request, 'blood_banks/blood_bank_form.html', {'form': form, 'action': 'Update'})


@login_required
def blood_bank_delete(request, pk):
    """Delete blood bank (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    blood_bank = get_object_or_404(BloodBank, pk=pk)
    
    if request.method == 'POST':
        blood_bank.delete()
        messages.success(request, 'Blood bank deleted successfully.')
        return redirect('blood_bank_list')
    
    return render(request, 'blood_banks/blood_bank_confirm_delete.html', {'blood_bank': blood_bank})


@login_required
def blood_inventory_list(request):
    """List blood inventory"""
    inventory = BloodInventory.objects.all().order_by('blood_bank', 'blood_group')
    
    return render(request, 'blood_banks/inventory_list.html', {'inventory': inventory})


@login_required
def blood_inventory_create(request):
    """Create blood inventory (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    if request.method == 'POST':
        form = BloodInventoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blood inventory added successfully!')
            return redirect('blood_inventory_list')
    else:
        form = BloodInventoryForm()
    
    return render(request, 'blood_banks/inventory_form.html', {'form': form, 'action': 'Create'})


@login_required
def blood_inventory_update(request, pk):
    """Update blood inventory (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    inventory = get_object_or_404(BloodInventory, pk=pk)
    
    if request.method == 'POST':
        form = BloodInventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blood inventory updated successfully!')
            return redirect('blood_inventory_list')
    else:
        form = BloodInventoryForm(instance=inventory)
    
    return render(request, 'blood_banks/inventory_form.html', {'form': form, 'action': 'Update'})


@login_required
def donors_list(request):
    """List all donors (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    donors = DonorProfile.objects.all().order_by('-created_at')
    
    # Filter by blood group and availability
    blood_group = request.GET.get('blood_group', '')
    is_available = request.GET.get('is_available', '')
    
    if blood_group:
        donors = donors.filter(blood_group=blood_group)
    
    if is_available:
        donors = donors.filter(is_available=(is_available == 'true'))
    
    blood_groups = DonorProfile.BLOOD_GROUP_CHOICES
    
    context = {
        'donors': donors,
        'blood_groups': blood_groups,
        'selected_blood_group': blood_group,
        'selected_is_available': is_available,
    }
    
    return render(request, 'blood_banks/donors_list.html', context)


@login_required
def donation_approval_list(request):
    """List donations pending approval (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    donations = DonationHistory.objects.filter(status='pending').order_by('-created_at')
    
    return render(request, 'blood_banks/donation_approval_list.html', {'donations': donations})


@login_required
def donation_approve(request, pk):
    """Approve donation (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    donation = get_object_or_404(DonationHistory, pk=pk)
    
    if request.method == 'POST':
        donation.status = 'approved'
        donation.approved_by = request.user
        donation.save()
        
        # Update donor's last donation date
        donation.donor.last_donation_date = donation.donation_date
        donation.donor.save()
        
        messages.success(request, 'Donation approved successfully!')
        
        # Send email notification (bonus feature)
        try:
            from django.core.mail import send_mail
            from django.conf import settings
            send_mail(
                'Donation Approved',
                f'Your donation on {donation.donation_date} has been approved.',
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@bloodbank.com',
                [donation.donor.user.email],
                fail_silently=True,
            )
        except:
            pass
        
        return redirect('donation_approval_list')
    
    return render(request, 'blood_banks/donation_approve.html', {'donation': donation})


@login_required
def donation_reject(request, pk):
    """Reject donation (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    donation = get_object_or_404(DonationHistory, pk=pk)
    
    if request.method == 'POST':
        donation.status = 'rejected'
        donation.approved_by = request.user
        donation.notes = request.POST.get('notes', '')
        donation.save()
        
        messages.success(request, 'Donation rejected.')
        
        # Send email notification (bonus feature)
        try:
            from django.core.mail import send_mail
            from django.conf import settings
            send_mail(
                'Donation Rejected',
                f'Your donation on {donation.donation_date} has been rejected. Reason: {donation.notes}',
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@bloodbank.com',
                [donation.donor.user.email],
                fail_silently=True,
            )
        except:
            pass
        
        return redirect('donation_approval_list')
    
    return render(request, 'blood_banks/donation_reject.html', {'donation': donation})
