# Django Income Tracking Project Makefile
# 
# This Makefile provides commands for common Django development tasks.
# Run 'make help' to see available commands.

.PHONY: help install run shell collectstatic migrate makemigrations fake-data resetdb superuser test lint clean

# Variables
PYTHON = python
MANAGE = $(POETRY) run $(PYTHON) manage.py
POETRY = poetry

# Colors
BLUE = \033[0;34m
GREEN = \033[0;32m
RED = \033[0;31m
YELLOW = \033[0;33m
NC = \033[0m # No Color

# Help command
help:
	@echo "$(BLUE)Django Income Tracking Project Makefile$(NC)"
	@echo "$(BLUE)=====================================$(NC)"
	@echo "Available commands:"
	@echo "  $(GREEN)make help$(NC)          - Show this help message"
	@echo "  $(GREEN)make install$(NC)       - Install dependencies using Poetry"
	@echo "  $(GREEN)make run$(NC)           - Run the development server"
	@echo "  $(GREEN)make shell$(NC)         - Start Django shell"
	@echo "  $(GREEN)make collectstatic$(NC) - Collect static files"
	@echo "  $(GREEN)make migrate$(NC)       - Apply database migrations"
	@echo "  $(GREEN)make makemigrations$(NC)- Create new migrations"
	@echo "  $(GREEN)make fake-data$(NC)     - Generate fake data for testing"
	@echo "  $(GREEN)make resetdb$(NC)       - Reset the database (drop and recreate)"
	@echo "  $(GREEN)make superuser$(NC)     - Create a Django superuser"
	@echo "  $(GREEN)make test$(NC)          - Run tests"
	@echo "  $(GREEN)make lint$(NC)          - Run linting checks"
	@echo "  $(GREEN)make clean$(NC)         - Clean temporary files"
	@echo "  $(GREEN)make manage cmd=<command>$(NC) - Run a custom Django management command"
	@echo "  $(GREEN)make backfill-portfolio$(NC) - Backfill portfolio history data"
	@echo "  $(GREEN)make dev$(NC)           - Alias for 'make run' (start development server)"
	@echo "  $(GREEN)make setup$(NC)         - Install dependencies, apply migrations, and generate fake data"

# Environment setup
install:
	@echo "$(BLUE)Installing dependencies...$(NC)"
	$(POETRY) install
	@echo "$(GREEN)Dependencies installed successfully.$(NC)"

# Development commands
run:
	@echo "$(BLUE)Starting development server...$(NC)"
	$(MANAGE) runserver 0.0.0.0:8000

shell:
	@echo "$(BLUE)Starting Django shell...$(NC)"
	$(MANAGE) shell

collectstatic:
	@echo "$(BLUE)Collecting static files...$(NC)"
	$(MANAGE) collectstatic --noinput
	@echo "$(GREEN)Static files collected.$(NC)"

# Database commands
migrate:
	@echo "$(BLUE)Applying migrations...$(NC)"
	$(MANAGE) migrate
	@echo "$(GREEN)Migrations applied.$(NC)"

makemigrations:
	@echo "$(BLUE)Creating migrations...$(NC)"
	$(MANAGE) makemigrations
	@echo "$(GREEN)Migrations created.$(NC)"

fake-data:
	@echo "$(BLUE)Generating fake data...$(NC)"
	$(MANAGE) create_fake_data
	@echo "$(GREEN)Fake data generated.$(NC)"

resetdb:
	@echo "$(RED)WARNING: This will delete all data in the database.$(NC)"
	@echo "$(RED)Are you sure you want to continue? [y/N]$(NC)"
	@read -p " " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		echo "$(BLUE)Resetting database...$(NC)"; \
		rm -f db.sqlite3; \
		$(MANAGE) migrate; \
		echo "$(GREEN)Database reset complete.$(NC)"; \
	else \
		echo "$(YELLOW)Database reset aborted.$(NC)"; \
	fi

superuser:
	@echo "$(BLUE)Creating superuser...$(NC)"
	$(MANAGE) createsuperuser
	@echo "$(GREEN)Superuser created.$(NC)"

# Testing and maintenance
test:
	@echo "$(BLUE)Running tests...$(NC)"
	$(MANAGE) test

lint:
	@echo "$(BLUE)Running linting...$(NC)"
	$(POETRY) run ruff check .
	@echo "$(GREEN)Linting complete.$(NC)"

clean:
	@echo "$(BLUE)Cleaning temporary files...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".DS_Store" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".tox" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete
	@echo "$(GREEN)Cleanup complete.$(NC)"

# Custom management command
manage:
	@if [ -z "$(cmd)" ]; then \
		echo "$(RED)Error: No command specified. Usage: make manage cmd=<command>$(NC)"; \
		exit 1; \
	fi
	@echo "$(BLUE)Running management command: $(cmd)$(NC)"
	$(MANAGE) $(cmd)
	@echo "$(GREEN)Command completed.$(NC)"

# Shorthand aliases
dev: run
setup: install migrate fake-data

# Add backfill command for portfolio history
backfill-portfolio:
	@echo "$(BLUE)Backfilling portfolio history...$(NC)"
	$(MAKE) manage cmd=backfill_portfolio_history
	@echo "$(GREEN)Portfolio history backfilled.$(NC)"
