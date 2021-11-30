Untouched Web Trading – Trade As a Service
The Untouched Web Trading Service runs serverless computing to manage investment portfolios of any size. The serverless system allows for rapid scaling to meet the demands needed to make trades efficiently. The application manages market data and monitors user investments through cloud computing and Brokerage API’s. The trade service imports, aggregates, and stores data as needed, performs machine learning, and submits orders through dedicated brokerage API’s. The web interface for Untouched is currently a dashboard to view the users portfolio along with Untouched Trading’s top ranked equities. As trade service executes trade, the user portfolio can be seen through the web user interface. 
Deployment to Azure Web Environment
1. Create an Azure Account
2. Create an Alpaca Market Account
3. Create an IEX Account to retrieve stock data and quotes
4. Clone GitHub Repositories for the Dash Web App and Serverless Functions
* https://github.com/andrejhicks/UntouchedTradingApp.git
* https://github.com/andrejhicks/AlgoTrading_Function.git
5. Create Azure App Service 
a. Configure the deployment of the App source as GitHub through the “Deployment Center” in the App Services Deployment Settings. This will create automatic CI/CD updates through GitHub changes.
b. Use UntouchedTradingApp as the source code for the App Service
6. Create Azure Function App Instance
a. This should include a blob storage account
b. Configure the deployment of the Function App through the “Deployment Center” in the Azure Functions Deployment Settings
c. Use the AlgoTrading_Function repo as the source code for the Function App
7. Create an Azure SQL Server
a. Run the SQL file “TradingDatabase.sql” to construct the SQL Database
8. I’ve attached the keys used to deploy the applications to my azure account, and a new account within azure should use the same configuration, with the exception of the Uri addresses to functions, apps, and the blob storage.  Algowebtradingappconfig.json, FunctionAppsConfig.json
9. The function runs on a timer, and executes the data request, model and trade execution. 
Software Needs
* VSCode
* GitHub
* Azure Account
o Azure App Service
o Azure Function Apps
o Azure SQL Server
o Azure Storage
* IEX
* Alpaca Markets Brokerage Account
