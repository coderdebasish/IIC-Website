# IIC-IEM Quick Start Script (Windows PowerShell)
# Run this once to set up and start the development server.

Write-Host "=== IIC-IEM Setup & Start ===" -ForegroundColor Cyan

# Step 1: Make and run Django migrations
Write-Host "`n[1] Generating and running database migrations..." -ForegroundColor Yellow
python manage.py makemigrations users core events certificates council achievements gallery announcements
python manage.py migrate

# Step 2: Create superuser
Write-Host "`n[2] Creating Super Admin account..." -ForegroundColor Yellow
Write-Host "You will be prompted for username, email, and password." -ForegroundColor Gray
python manage.py shell -c "
from apps.users.models import CustomUser
if not CustomUser.objects.filter(username='admin').exists():
    u = CustomUser.objects.create_superuser('admin', 'admin@iic-iem.local', 'Admin@123!')
    u.role = 'super_admin'
    u.first_name = 'IIC'
    u.last_name = 'Admin'
    u.is_staff = True
    u.save()
    print('Super Admin created: username=admin  password=Admin@123!')
    print('IMPORTANT: Change this password after first login!')
else:
    print('Admin user already exists.')
"

# Step 3: Collect static files
Write-Host "`n[3] Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

# Step 4: Start dev server
Write-Host "`n[4] Starting development server..." -ForegroundColor Green
Write-Host "Website: http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host "Admin Panel: http://127.0.0.1:8000/admin-panel/login/" -ForegroundColor Cyan
Write-Host "Login: username=admin  password=Admin@123!" -ForegroundColor Yellow
Write-Host "`nPress Ctrl+C to stop the server." -ForegroundColor Gray
python manage.py runserver
