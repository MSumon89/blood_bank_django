from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import DonorProfile, DonationHistory
from .forms import DonorProfileForm, DonationHistoryForm
from blood_requests.models import BloodRequest
from blood_banks.models import BloodInventory


@login_required
def donor_dashboard(request):
    """Donor dashboard view"""
    if request.user.user_type != 'donor':
        messages.error(request, 'Access denied. Donors only.')
        return redirect('home')
    
    # Get or create donor profile
    try:
        donor_profile = request.user.donor_profile
    except DonorProfile.DoesNotExist:
        messages.info(request, 'Please complete your donor profile first.')
        return redirect('donor_profile_create')
    
    # Get donation history
    donations = DonationHistory.objects.filter(donor=donor_profile).order_by('-donation_date')[:5]
    
    # Get blood requests made by this user
    my_requests = BloodRequest.objects.filter(requester=request.user).order_by('-requested_date')[:5]
    
    # Get available blood inventory
    blood_inventory = BloodInventory.objects.all().order_by('blood_group')
    
    context = {
        'donor_profile': donor_profile,
        'donations': donations,
        'my_requests': my_requests,
        'blood_inventory': blood_inventory,
        'total_donations': donations.count(),
    }
    
    return render(request, 'donors/dashboard.html', context)


@login_required
def donor_profile_create(request):
    """Create donor profile"""
    if request.user.user_type != 'donor':
        messages.error(request, 'Access denied. Donors only.')
        return redirect('home')
    
    # Check if profile already exists
    if hasattr(request.user, 'donor_profile'):
        messages.info(request, 'Profile already exists. You can update it.')
        return redirect('donor_profile_update')
    
    if request.method == 'POST':
        form = DonorProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Donor profile created successfully!')
            return redirect('donor_dashboard')
    else:
        form = DonorProfileForm()
    
    return render(request, 'donors/profile_form.html', {'form': form, 'action': 'Create'})


@login_required
def donor_profile_update(request):
    """Update donor profile"""
    if request.user.user_type != 'donor':
        messages.error(request, 'Access denied. Donors only.')
        return redirect('home')
    
    try:
        profile = request.user.donor_profile
    except DonorProfile.DoesNotExist:
        messages.error(request, 'Please create your profile first.')
        return redirect('donor_profile_create')
    
    if request.method == 'POST':
        form = DonorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('donor_dashboard')
    else:
        form = DonorProfileForm(instance=profile)
    
    return render(request, 'donors/profile_form.html', {'form': form, 'action': 'Update'})


@login_required
def donor_profile_view(request):
    """View donor profile"""
    if request.user.user_type != 'donor':
        messages.error(request, 'Access denied. Donors only.')
        return redirect('home')
    
    try:
        profile = request.user.donor_profile
    except DonorProfile.DoesNotExist:
        messages.error(request, 'Please create your profile first.')
        return redirect('donor_profile_create')
    
    return render(request, 'donors/profile_view.html', {'profile': profile})


@login_required
def donation_history_list(request):
    """List all donations for current donor"""
    if request.user.user_type != 'donor':
        messages.error(request, 'Access denied. Donors only.')
        return redirect('home')
    
    try:
        donor_profile = request.user.donor_profile
    except DonorProfile.DoesNotExist:
        messages.error(request, 'Please create your profile first.')
        return redirect('donor_profile_create')
    
    donations = DonationHistory.objects.filter(donor=donor_profile).order_by('-donation_date')
    
    return render(request, 'donors/donation_history.html', {'donations': donations})


@login_required
def donation_create(request):
    """Create new donation record"""
    if request.user.user_type != 'donor':
        messages.error(request, 'Access denied. Donors only.')
        return redirect('home')
    
    try:
        donor_profile = request.user.donor_profile
    except DonorProfile.DoesNotExist:
        messages.error(request, 'Please create your profile first.')
        return redirect('donor_profile_create')
    
    if request.method == 'POST':
        form = DonationHistoryForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = donor_profile
            donation.save()
            messages.success(request, 'Donation request submitted successfully! Waiting for approval.')
            return redirect('donation_history_list')
    else:
        form = DonationHistoryForm()
    
    return render(request, 'donors/donation_form.html', {'form': form})


def donor_search(request):
    """Search donors by blood group, city, and availability"""
    donors = DonorProfile.objects.filter(is_available=True)
    
    # Get filter parameters
    blood_group = request.GET.get('blood_group', '')
    city = request.GET.get('city', '')
    
    if blood_group:
        donors = donors.filter(blood_group=blood_group)
    
    if city:
        donors = donors.filter(city__icontains=city)
    
    # Get all blood groups for filter
    blood_groups = DonorProfile.BLOOD_GROUP_CHOICES
    
    # Get all cities for filter
    cities = DonorProfile.objects.values_list('city', flat=True).distinct().order_by('city')
    
    context = {
        'donors': donors,
        'blood_groups': blood_groups,
        'cities': cities,
        'selected_blood_group': blood_group,
        'selected_city': city,
    }
    
    return render(request, 'donors/donor_search.html', context)
