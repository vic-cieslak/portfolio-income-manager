# Next Steps for Django Income Tracking Project

## 1. Track portfolio value over time
- Implement in the portfolio app
- Create a new model (e.g., PortfolioHistory) to store historical data
- Modify portfolio views to record daily portfolio values
- Add a new view and template to display historical data (possibly using charts.js)

## 2. Prognose income / portfolio value
- Create a new 'forecasting' app
- Implement simple linear regression model for basic predictions
- Add views and forms for users to input variables affecting predictions
- Create templates to display forecasts (possibly using charts.js)


## 4. Track expenses
- Create a new 'expenses' app (similar structure to the income app)
- Implement models for Expense and ExpenseCategory
- Create views for CRUD operations on expenses
- Add templates for expense management
- Integrate expense data into existing dashboards and reports

## 5. Improve cryptocurrency fetching
- Modify portfolio/services.py to optimize API calls to CoinGecko
- Implement caching mechanism to reduce API calls and improve performance
- Add support for more cryptocurrencies and detailed market data
- Consider alternative data sources if CoinGecko continues to be unreliable

## 6. Add settings page [in progress]
- Add new views and templates in the core app for settings management
- Create a UserSettings model to store user-specific settings
- Implement functionality to change currency, set API tokens, and customize site name
- Ensure settings are applied consistently across the application


## 9. Fix currency breakdown in calendar
- Debug income/views.py and templates/income/income_calendar.html
- Identify the source of the currency mismatch
- Correct the logic for currency conversion or display
- Ensure the fix is applied consistently across all relevant parts of the application

## 10. Client management
- Create a new 'clients' app
- Implement Client model
- Create views for CRUD operations on clients
- Add templates for client management
- Modify existing apps (income, expenses, portfolio) to associate data with specific clients
- Implement a client selection mechanism in the UI

## 11. recalculation of currnecy USD -> PLN, PLN -> GBP, etc



## Priority Order
1. Fix currency breakdown in calendar (critical bug fix)
2. Improve cryptocurrency fetching (enhance existing core functionality)
3. Track portfolio value over time (significant value add)
4. Add settings page (improves customization, prepares for future features)
5. Improve portfolio allocation pie chart (enhances existing visualization)
6. Click-to-edit income in calendar (improves user interaction)
7. Remove line effect (UI/UX improvement)
8. Track expenses (expands core functionality)
9. Prognose income / portfolio value (advanced feature)
10. Client management (major feature expansion)