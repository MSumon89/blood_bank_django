# Quick Start Guide - Blood Management System

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies
```bash
cd /Users/msumon87/www/PythonProject/blood-management
pip install -r requirements.txt
```

### Step 2: Create Sample Data
```bash
python manage.py create_sample_data
```

This command creates:
- 1 Admin user
- 5 Donor users with profiles
- 3 Blood banks with inventory
- 1 Sample blood request

### Step 3: Run the Server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

## 🔑 Test Credentials

### Admin Account
- **Username**: admin
- **Password**: admin123
- **Access**: Full system access, manage everything

### Donor Accounts
All donors have password: **donor123**

1. **john_doe** (A+) - Available donor in Dhaka
2. **sarah_smith** (O+) - Available donor in Dhaka
3. **mike_wilson** (B+) - Available donor in Dhaka
4. **emma_brown** (AB+) - Not available, has donation history
5. **alex_jones** (O-) - Universal donor, available

## 📱 Features to Test

### As a Donor (Login: john_doe / donor123)
1. **View Dashboard** - See your profile summary and statistics
2. **Update Profile** - Add/edit your information and photo
3. **Add Donation** - Record a blood donation (needs admin approval)
4. **Create Blood Request** - Request blood for a patient
5. **Search Donors** - Find donors by blood group and city
6. **View Donation History** - Check all your past donations

### As Admin (Login: admin / admin123)
1. **Admin Dashboard** - View statistics and system overview
2. **Manage Donors** - See all donors, filter by blood group
3. **Approve Donations** - Review pending donation submissions
4. **Manage Blood Requests** - Update request statuses
5. **Blood Banks** - Add/edit blood bank information
6. **Blood Inventory** - Manage blood units by blood group
7. **Django Admin** - Access at http://127.0.0.1:8000/admin/

## 🎯 Key Pages to Visit

### Public Pages (No Login Required)
- **Home**: http://127.0.0.1:8000/
- **Search Donors**: http://127.0.0.1:8000/donors/search/
- **Register**: http://127.0.0.1:8000/accounts/register/
- **Login**: http://127.0.0.1:8000/accounts/login/

### Donor Pages (Requires Donor Login)
- **Dashboard**: http://127.0.0.1:8000/donors/dashboard/
- **Profile**: http://127.0.0.1:8000/donors/profile/
- **My Donations**: http://127.0.0.1:8000/donors/donations/
- **Add Donation**: http://127.0.0.1:8000/donors/donations/create/
- **My Requests**: http://127.0.0.1:8000/requests/
- **Create Request**: http://127.0.0.1:8000/requests/create/

### Admin Pages (Requires Admin Login)
- **Admin Dashboard**: http://127.0.0.1:8000/admin/dashboard/
- **All Donors**: http://127.0.0.1:8000/admin/donors/
- **Pending Approvals**: http://127.0.0.1:8000/admin/donations/pending/
- **Blood Banks**: http://127.0.0.1:8000/blood-banks/
- **Blood Inventory**: http://127.0.0.1:8000/inventory/
- **Django Admin Panel**: http://127.0.0.1:8000/admin/

## 🧪 Testing Workflow

### Scenario 1: New Donor Registration
1. Click "Register" on homepage
2. Fill form, select "Donor" as user type
3. After registration, complete donor profile
4. Add blood group, date of birth, address, etc.
5. Set availability to "Yes"
6. View your dashboard

### Scenario 2: Blood Donation Process
1. Login as donor (john_doe/donor123)
2. Go to "Add Donation"
3. Select blood bank, date, units
4. Submit (Status: Pending)
5. Logout, login as admin
6. Go to "Pending Approvals"
7. Approve the donation
8. Email notification sent (console output)
9. Logout, login as donor again
10. See approved donation in history

### Scenario 3: Blood Request
1. Login as donor
2. Click "Create Request"
3. Fill patient details, blood group needed
4. Set urgency level and required date
5. Submit request
6. Admin can view and update status

### Scenario 4: Search Donors
1. Go to "Search Donors" (public)
2. Filter by blood group (e.g., O-)
3. Filter by city (e.g., Dhaka)
4. View matching donors with contact info

## 📊 Database Overview

The application uses SQLite database (db.sqlite3) with these main tables:
- **users** - User accounts (admin/donor)
- **donor_profiles** - Donor information
- **donation_history** - Donation records
- **blood_requests** - Blood request records
- **blood_banks** - Blood bank information
- **blood_inventory** - Blood units by group

## 🔧 Troubleshooting

### Issue: Can't login
- **Solution**: Use correct credentials from above
- Check if user exists in Django admin

### Issue: Profile error for donor
- **Solution**: Create profile at /donors/profile/create/

### Issue: Static files not loading
- **Solution**: Check STATIC_URL in settings.py
- Run: `python manage.py collectstatic` if needed

### Issue: Images not showing
- **Solution**: Ensure MEDIA_ROOT is configured
- Check file upload permissions

## 📱 Mobile Responsive

The application is fully responsive and works on:
- Desktop browsers (Chrome, Firefox, Safari)
- Tablets (iPad, Android tablets)
- Mobile phones (iPhone, Android)

## 🌟 Bonus Features Implemented

✅ Email notifications (console in development)
✅ Profile photo upload
✅ Blood request tracking with statuses
✅ Urgency levels for requests
✅ Location-based donor search
✅ Real-time inventory management
✅ Comprehensive statistics dashboard
✅ Medical conditions tracking
✅ Last donation date tracking
✅ Donor availability toggle

## 📚 Next Steps

1. **Customize**: Update branding, colors, logos
2. **Email**: Configure SMTP for real email notifications
3. **Deploy**: Host on Render, Railway, or PythonAnywhere
4. **Database**: Switch to PostgreSQL for production
5. **Features**: Add charts, SMS notifications, payment integration

## 💡 Tips

- Use Chrome DevTools to test responsive design
- Check console for email notifications in development
- Use Django admin for quick data management
- Take screenshots for documentation
- Test all user journeys before submission

## 🎓 Learning Outcomes

This project demonstrates:
- Django models and relationships
- User authentication and authorization
- Form handling and validation
- Template inheritance
- Bootstrap responsive design
- File uploads (images)
- Email integration
- Admin customization
- Database migrations
- URL routing
- View logic and permissions

---

**Ready to go! Start the server and begin testing.** 🚀
