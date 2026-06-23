# FitX - Comprehensive Fitness Platform

A full-stack Django web application for fitness training, nutrition planning, workout management, and online store functionality.

## Features

- **User Accounts**: Member registration and authentication
- **Workout Programs**: Browse trainers, exercises, and create custom routines
- **Nutrition Planning**: Diet plans and meal tracking
- **Store**: E-commerce for fitness products and memberships
- **REST API**: Complete API endpoints for mobile apps
- **Progress Tracking**: Monitor user fitness progress
- **Membership Plans**: Subscription-based memberships with Razorpay integration

## Project Structure

```
fitness/                    # Main Django project
├── account/               # User authentication and profiles
├── core/                  # Homepage, blog, FAQs, testimonials
├── diet/                  # Nutrition and meal plans
├── store/                 # E-commerce and memberships
├── workout/               # Exercises, trainers, routines
├── manage.py              # Django management script
└── static/                # CSS, JS, images
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fitness
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files** (production)
   ```bash
   python manage.py collectstatic
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

   Access the app at `http://localhost:8000`

## Important Configuration

### Razorpay Integration
1. Add your Razorpay API keys to `.env`:
   ```
   RAZORPAY_KEY_ID=your_key_id
   RAZORPAY_KEY_SECRET=your_key_secret
   ```

### JWT Secret Key
Generate a secure SECRET_KEY for production:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Database
- Development uses SQLite (db.sqlite3)
- For production, configure PostgreSQL in `.env`

## API Endpoints

- `GET /api/workouts/` - List all workouts
- `GET /api/exercises/` - List all exercises
- `GET /api/diet/` - List meal plans
- `GET /api/memberships/` - List membership plans
- `GET /api/progress/` - User progress tracking
- `POST /api/diet/` - Create meal plan (authenticated)

## Admin Panel

Access Django admin at `/admin/` with superuser credentials.

## Development Commands

```bash
# Run tests
python manage.py test

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Load sample data
python manage.py seed_exercises
python manage.py seed_diet

# Shell access
python manage.py shell
```

## Deploying to Production

1. Update `DEBUG = False` in `.env`
2. Add your domain to `ALLOWED_HOSTS`
3. Set secure cookie flags in `.env`
4. Use environment variables for all secrets
5. Use PostgreSQL database instead of SQLite
6. Configure static files with WhiteNoise or CDN
7. Use Gunicorn as WSGI server:
   ```bash
   gunicorn fitness.wsgi:application
   ```

## Troubleshooting

- **Static files not loading**: Run `python manage.py collectstatic`
- **Database errors**: Check migrations with `python manage.py showmigrations`
- **Razorpay errors**: Verify keys in `.env` and check payment status in Razorpay dashboard

## License

MIT License - See LICENSE file for details

## Support

For issues or questions, contact the development team.
