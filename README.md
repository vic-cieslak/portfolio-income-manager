# Django Income Tracking

A comprehensive financial management web application built with Django that helps you track income, manage cryptocurrencies, and monitor bank accounts.

![Dashboard Screenshot](generated-icon.png)

## Overview

Django Income Tracking is a personal finance management system that provides tools for tracking income sources, managing cryptocurrency investments, and monitoring bank accounts. The application features a modern, cyberpunk-themed UI with interactive charts and visualizations to help you understand your financial situation at a glance.

## Features

### Dashboard
- Overview of total net worth
- Monthly income summary
- Portfolio allocation visualization
- Income trends chart
- Recent income entries

### Income Management
- Track income from various sources
- Categorize income entries
- View detailed income history
- Monthly calendar view with daily income totals
- Income category breakdown

### Portfolio Management
- Cryptocurrency tracking with real-time price updates via CoinGecko API
- Bank account management
- Total portfolio value calculation
- Asset allocation visualization

### User Interface
- Modern cyberpunk-themed design
- Responsive layout for desktop and mobile
- Interactive charts and visualizations
- User authentication and security

## Technologies Used

- **Backend**: Django 5.0+, Python 3.10+
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (default)
- **Dependencies**:
  - django-crispy-forms
  - crispy-bootstrap4
  - django-bootstrap-datepicker-plus
  - requests (for API integration)
- **APIs**: CoinGecko API for cryptocurrency price data
- **Package Management**: Poetry

## Installation and Setup

### Prerequisites
- Python 3.10 or higher
- Poetry (for dependency management)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/django-income-tracking.git
   cd django-income-tracking
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Apply database migrations:
   ```bash
   poetry run python manage.py migrate
   ```

4. Create a superuser (admin account):
   ```bash
   poetry run python manage.py createsuperuser
   ```

5. (Optional) Generate sample data:
   ```bash
   poetry run python manage.py create_fake_data
   ```

6. Collect static files:
   ```bash
   poetry run python manage.py collectstatic
   ```

7. Run the development server:
   ```bash
   poetry run python manage.py runserver
   ```

8. Access the application at http://127.0.0.1:8000/

## Usage

### Income Tracking
1. Navigate to the Income section
2. Add new income entries with amount, date, category, and description
3. View income history and filter by category or date
4. Use the calendar view to see income distribution by day

### Portfolio Management
1. Add cryptocurrencies to your portfolio (prices update automatically)
2. Add bank accounts with current balances
3. View total portfolio value and asset allocation
4. Update cryptocurrency holdings or bank balances as needed

### Dashboard
- The dashboard provides an overview of your financial situation
- View monthly income trends
- See portfolio allocation
- Monitor recent income entries

## Project Structure

```
django_project/          # Main Django project settings
├── settings.py          # Project settings
├── urls.py              # Main URL routing
└── wsgi.py              # WSGI configuration

core/                    # Core app (dashboard, authentication)
├── views.py             # Dashboard and auth views
└── urls.py              # Core URL patterns

income/                  # Income tracking app
├── models.py            # Income and Category models
├── views.py             # Income views (list, detail, calendar)
├── forms.py             # Income forms
└── urls.py              # Income URL patterns

portfolio/               # Portfolio management app
├── models.py            # Cryptocurrency and Bank models
├── views.py             # Portfolio views
├── forms.py             # Portfolio forms
└── urls.py              # Portfolio URL patterns

templates/               # HTML templates
├── base/                # Base templates
├── core/                # Dashboard templates
├── income/              # Income templates
└── portfolio/           # Portfolio templates

static/                  # Static files (CSS, JS)
├── css/                 # CSS files
└── js/                  # JavaScript files
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Chart.js](https://www.chartjs.org/)
- [CoinGecko API](https://www.coingecko.com/en/api)
- [Font Awesome](https://fontawesome.com/)
