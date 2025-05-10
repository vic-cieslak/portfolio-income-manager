
You will be working on implementing new features to this project. You are a rockstar engineer. Check the required task and plan the implementation:

- update titles of pages in browser (we dont know what page when looking at the tabs in the browser)
(HTML TITLES are not configured)



# Next Steps for Django Income Tracking Project

## need fast
claculator in income input for
type ( number of hours ) muliplty by current USD exchange rate

### NEW

- add ability to export/import data 
- add ability to have different potfolios? [not needed]
- add tracking token usage for expenses for AI, create pie chart (open router, claude3.7, gemini, chatgpt, replit)
- built in XMR wallet / ETH wallet / BTC wallet ??
- sync or deploy as web app?


## 2. Prognose income / portfolio value
- Create a new 'forecasting' app
- Implement simple linear regression model for basic predictions
- Add views and forms for users to input variables affecting predictions
- Create templates to display forecasts (possibly using charts.js)

## 3. sometimes income wont be paid. we need an ability to mark it as such so its not included into the portfolio, OR it should be marked 'not-paid' as default and after I mark it as paid its included in the portfolio.


## 5. Improve cryptocurrency fetching - DONE ? There are some issue at startup sometimes 
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
- add place to add note/list features delivered within given period, asses how much value / work was delivered.
- add place to add what features were promised to delivered for given price / time
- add place to add what was promised to deliver.

- Create views for CRUD operations on clients
- Add templates for client management
- Modify existing apps (income, expenses, portfolio) to associate data with specific clients
- Implement a client selection mechanism in the UI


### Liablities management, what is owed to whom, or who owes me something.

## 11. recalculation of currnecy USD -> PLN, PLN -> GBP, etc

## 12. income view is not listing all incomes, some better table should be better.

# 13. income entry should allow to input RATE: XX and hours: XX and then calculate total income for that day.
## ???? should i save those?

### 14. more basic theme because its slow on some devices. create theme selector feature.

### 15. show total income for current week.

add to djano admin

## Priority Order
2. Improve cryptocurrency fetching (enhance existing core functionality)


4. Add settings page (improves customization, prepares for future features)
7. Remove line effect (UI/UX improvement)
9. Prognose income / portfolio value (advanced feature)
10. Client management (major feature expansion)


