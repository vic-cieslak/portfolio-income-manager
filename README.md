# Django Income Tracking

A comprehensive financial management web application built with Django that helps you track income and expenses, manage cryptocurrencies, and monitor bank accounts.

Click on the image below to see the demo.

[![Check the video](https://img.youtube.com/vi/piMv2jAwbo8/maxresdefault.jpg)](https://www.youtube.com/watch?v=piMv2jAwbo8)


## Overview

Django Income Tracking is a personal finance management system that provides tools for tracking income sources, managing expenses, monitoring cryptocurrency investments, and overseeing bank accounts. The application features a modern, cyberpunk-themed UI with interactive charts and visualizations to help you understand your financial situation at a glance.

## Features

### Dashboard
- Overview of total net worth
- Monthly income and expense summary
- Portfolio allocation visualization
- Income and expense trends chart
- Recent income and expense entries

### Income Management
- Track income from various sources
- Categorize income entries
- Calculate income based on rate and hours worked
- View detailed income history
- Monthly calendar view with daily income totals
- Income category breakdown

### Expense Management
- Track expenses across various categories
- Categorize expense entries
- View detailed expense history
- Monthly calendar view with daily expense totals
- Expense category breakdown

### Portfolio Management
- Cryptocurrency tracking with real-time price updates via CoinGecko API
- Bank account management
- Total portfolio value calculation
- Asset allocation visualization

### User Settings
- Manage user-specific preferences (e.g., default currency - *feature in progress*)
- Customize site appearance (e.g., site name - *feature in progress*)

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

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/django-income-tracking.git
    cd django-income-tracking
    ```

2.  Run the setup command (installs dependencies, applies migrations, and generates sample data):
    ```bash
    make setup
    ```
    *Note: This command uses Poetry for dependency management and will also generate fake data.*

3.  Create a superuser (admin account):
    ```bash
    make superuser
    ```

4.  Collect static files:
    ```bash
    make collectstatic
    ```

5.  Run the development server:
    ```bash
    make run
    ```

6.  Access the application at http://127.0.0.1:8000/ (or the address shown in the `make run` output).

For more available commands, you can run `make help`.

## Usage

### Income Tracking
1. Navigate to the Income section.
2. Add new income entries with amount, date, category, description, and optionally rate/hours.
3. View income history and filter by category or date.
4. Use the calendar view to see income distribution by day.

### Expense Tracking
1. Navigate to the Expenses section.
2. Add new expense entries with amount, date, category, and description.
3. View expense history and filter by category or date.
4. Use the calendar view to see expense distribution by day.

### Portfolio Management
1. Add cryptocurrencies to your portfolio (prices update automatically).
2. Add bank accounts with current balances.
3. View total portfolio value and asset allocation.
4. Update cryptocurrency holdings or bank balances as needed.

### Dashboard
- The dashboard provides an overview of your financial situation.
- View monthly income and expense trends.
- See portfolio allocation.
- Monitor recent income and expense entries.

## Project Structure

```
django_project/          # Main Django project settings
├── settings.py          # Project settings
├── urls.py              # Main URL routing
└── wsgi.py              # WSGI configuration

core/                    # Core app (dashboard, authentication, user settings)
├── views.py             # Dashboard, auth, and settings views
└── urls.py              # Core URL patterns

income/                  # Income tracking app
├── models.py            # Income and Category models
├── views.py             # Income views (list, detail, calendar)
├── forms.py             # Income forms
└── urls.py              # Income URL patterns

expenses/                # Expense tracking app
├── models.py            # Expense and Category models
├── views.py             # Expense views (list, detail, calendar)
├── forms.py             # Expense forms
└── urls.py              # Expense URL patterns

portfolio/               # Portfolio management app
├── models.py            # Cryptocurrency and Bank models
├── views.py             # Portfolio views
├── forms.py             # Portfolio forms
└── urls.py              # Portfolio URL patterns

templates/               # HTML templates
├── base/                # Base templates
├── core/                # Dashboard and settings templates
├── income/              # Income templates
├── expenses/            # Expense templates
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
