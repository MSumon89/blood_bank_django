from django.core.management.base import BaseCommand
from accounts.models import User
from donors.models import DonorProfile, DonationHistory
from blood_banks.models import BloodBank, BloodInventory
from blood_requests.models import BloodRequest
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Creates sample data for testing the Blood Management System'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@bloodbank.com',
                password='admin123',
                first_name='System',
                last_name='Administrator',
                user_type='admin',
                phone_number='01712345678'
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Created admin user: admin/admin123'))
        else:
            admin = User.objects.get(username='admin')
            self.stdout.write(self.style.WARNING('Admin user already exists'))
        
        # Create blood banks
        blood_banks_data = [
            {
                'name': 'Dhaka Medical College Blood Bank',
                'address': 'Shahbagh, Dhaka',
                'city': 'Dhaka',
                'phone_number': '02-9661063',
                'email': 'dmch@bloodbank.com'
            },
            {
                'name': 'Chittagong Medical College Blood Bank',
                'address': 'Panchlaish, Chittagong',
                'city': 'Chittagong',
                'phone_number': '031-2503650',
                'email': 'cmch@bloodbank.com'
            },
            {
                'name': 'Square Hospital Blood Bank',
                'address': '18/F, Bir Uttam Qazi Nuruzzaman Sarak',
                'city': 'Dhaka',
                'phone_number': '02-8159457',
                'email': 'square@bloodbank.com'
            }
        ]
        
        blood_banks = []
        for bank_data in blood_banks_data:
            bank, created = BloodBank.objects.get_or_create(
                name=bank_data['name'],
                defaults=bank_data
            )
            blood_banks.append(bank)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created blood bank: {bank.name}'))
        
        # Create blood inventory for each bank
        blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        for bank in blood_banks:
            for blood_group in blood_groups:
                inventory, created = BloodInventory.objects.get_or_create(
                    blood_bank=bank,
                    blood_group=blood_group,
                    defaults={'units_available': 25.00}
                )
                if created:
                    self.stdout.write(f'  Added {blood_group} inventory to {bank.name}')
        
        # Create donor users and profiles
        donors_data = [
            {
                'username': 'john_doe',
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone_number': '01712345679',
                'profile': {
                    'blood_group': 'A+',
                    'date_of_birth': date(1995, 5, 15),
                    'gender': 'male',
                    'address': '12 Green Road',
                    'city': 'Dhaka',
                    'state': 'Dhaka Division',
                    'zip_code': '1205',
                    'is_available': True
                }
            },
            {
                'username': 'sarah_smith',
                'email': 'sarah@example.com',
                'first_name': 'Sarah',
                'last_name': 'Smith',
                'phone_number': '01812345680',
                'profile': {
                    'blood_group': 'O+',
                    'date_of_birth': date(1992, 8, 20),
                    'gender': 'female',
                    'address': '45 Gulshan Avenue',
                    'city': 'Dhaka',
                    'state': 'Dhaka Division',
                    'zip_code': '1212',
                    'is_available': True
                }
            },
            {
                'username': 'mike_wilson',
                'email': 'mike@example.com',
                'first_name': 'Mike',
                'last_name': 'Wilson',
                'phone_number': '01912345681',
                'profile': {
                    'blood_group': 'B+',
                    'date_of_birth': date(1990, 3, 10),
                    'gender': 'male',
                    'address': '78 Banani Road',
                    'city': 'Dhaka',
                    'state': 'Dhaka Division',
                    'zip_code': '1213',
                    'is_available': True
                }
            },
            {
                'username': 'emma_brown',
                'email': 'emma@example.com',
                'first_name': 'Emma',
                'last_name': 'Brown',
                'phone_number': '01612345682',
                'profile': {
                    'blood_group': 'AB+',
                    'date_of_birth': date(1988, 12, 5),
                    'gender': 'female',
                    'address': '23 Dhanmondi Road',
                    'city': 'Dhaka',
                    'state': 'Dhaka Division',
                    'zip_code': '1209',
                    'is_available': False,
                    'last_donation_date': date.today() - timedelta(days=30)
                }
            },
            {
                'username': 'alex_jones',
                'email': 'alex@example.com',
                'first_name': 'Alex',
                'last_name': 'Jones',
                'phone_number': '01512345683',
                'profile': {
                    'blood_group': 'O-',
                    'date_of_birth': date(1993, 7, 25),
                    'gender': 'male',
                    'address': '56 Uttara Sector 7',
                    'city': 'Dhaka',
                    'state': 'Dhaka Division',
                    'zip_code': '1230',
                    'is_available': True
                }
            }
        ]
        
        for donor_data in donors_data:
            profile_data = donor_data.pop('profile')
            if not User.objects.filter(username=donor_data['username']).exists():
                user = User.objects.create_user(
                    password='donor123',
                    user_type='donor',
                    **donor_data
                )
                profile = DonorProfile.objects.create(user=user, **profile_data)
                self.stdout.write(self.style.SUCCESS(f'✓ Created donor: {user.username}/donor123 ({profile.blood_group})'))
                
                # Create some donation history
                if profile_data.get('last_donation_date'):
                    donation = DonationHistory.objects.create(
                        donor=profile,
                        blood_bank=blood_banks[0],
                        donation_date=profile_data['last_donation_date'],
                        units=1.00,
                        status='approved',
                        approved_by=admin
                    )
                    self.stdout.write(f'  Added donation history for {user.username}')
        
        # Create some blood requests
        donor_user = User.objects.filter(user_type='donor').first()
        if donor_user:
            request_data = {
                'requester': donor_user,
                'patient_name': 'Jane Doe',
                'blood_group': 'A+',
                'units_required': 2.00,
                'urgency': 'high',
                'hospital_name': 'Dhaka Medical College Hospital',
                'hospital_address': 'Shahbagh, Dhaka',
                'city': 'Dhaka',
                'contact_number': '01712345684',
                'reason': 'Emergency surgery required',
                'required_by_date': date.today() + timedelta(days=2),
                'status': 'pending'
            }
            
            if not BloodRequest.objects.filter(patient_name='Jane Doe').exists():
                blood_request = BloodRequest.objects.create(**request_data)
                self.stdout.write(self.style.SUCCESS(f'✓ Created blood request for {blood_request.patient_name}'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Sample data created successfully!'))
        self.stdout.write('\nTest Credentials:')
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  Donors: john_doe, sarah_smith, mike_wilson, emma_brown, alex_jones')
        self.stdout.write('  Password for all donors: donor123')
