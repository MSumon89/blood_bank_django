from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import BloodRequest
from .forms import BloodRequestForm, BloodRequestUpdateForm
from django.core.mail import send_mail
from django.conf import settings


@login_required
def blood_request_create(request):
    """Create new blood request"""
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.requester = request.user
            blood_request.save()
            messages.success(request, 'Blood request submitted successfully! You will be notified once it is reviewed.')
            
            # Send email notification to admins (bonus feature)
            # This will print to console in development
            try:
                send_mail(
                    'New Blood Request',
                    f'A new blood request for {blood_request.blood_group} has been submitted by {request.user.username}.',
                    settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@bloodbank.com',
                    [settings.ADMIN_EMAIL if hasattr(settings, 'ADMIN_EMAIL') else 'admin@bloodbank.com'],
                    fail_silently=True,
                )
            except:
                pass
            
            return redirect('blood_request_list')
    else:
        form = BloodRequestForm()
    
    return render(request, 'blood_requests/request_form.html', {'form': form})


@login_required
def blood_request_list(request):
    """List blood requests"""
    if request.user.user_type == 'admin':
        # Admin sees all requests
        requests = BloodRequest.objects.all().order_by('-requested_date')
    else:
        # Donors see only their requests
        requests = BloodRequest.objects.filter(requester=request.user).order_by('-requested_date')
    
    return render(request, 'blood_requests/request_list.html', {'requests': requests})


@login_required
def blood_request_detail(request, pk):
    """View blood request details"""
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    
    # Check permissions
    if request.user.user_type != 'admin' and blood_request.requester != request.user:
        messages.error(request, 'You do not have permission to view this request.')
        return redirect('blood_request_list')
    
    return render(request, 'blood_requests/request_detail.html', {'blood_request': blood_request})


@login_required
def blood_request_update(request, pk):
    """Update blood request status (Admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Admins only.')
        return redirect('home')
    
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    
    if request.method == 'POST':
        form = BloodRequestUpdateForm(request.POST, instance=blood_request)
        if form.is_valid():
            updated_request = form.save(commit=False)
            if updated_request.status in ['approved', 'rejected']:
                updated_request.approved_by = request.user
                updated_request.approved_date = timezone.now()
            updated_request.save()
            
            messages.success(request, f'Blood request status updated to {updated_request.get_status_display()}.')
            
            # Send email notification to requester (bonus feature)
            try:
                send_mail(
                    f'Blood Request {updated_request.get_status_display()}',
                    f'Your blood request for {blood_request.blood_group} has been {updated_request.get_status_display().lower()}.',
                    settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@bloodbank.com',
                    [blood_request.requester.email],
                    fail_silently=True,
                )
            except:
                pass
            
            return redirect('blood_request_detail', pk=pk)
    else:
        form = BloodRequestUpdateForm(instance=blood_request)
    
    return render(request, 'blood_requests/request_update.html', {'form': form, 'blood_request': blood_request})


@login_required
def blood_request_delete(request, pk):
    """Delete blood request"""
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    
    # Check permissions
    if request.user.user_type != 'admin' and blood_request.requester != request.user:
        messages.error(request, 'You do not have permission to delete this request.')
        return redirect('blood_request_list')
    
    if request.method == 'POST':
        blood_request.delete()
        messages.success(request, 'Blood request deleted successfully.')
        return redirect('blood_request_list')
    
    return render(request, 'blood_requests/request_confirm_delete.html', {'blood_request': blood_request})
