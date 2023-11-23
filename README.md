# EvaDB_Customer_Churn_App

# Introduction:
The Customer Churn project is a combination of the power of data prediction models with a simple interface for people to interact with.  In our project, we want to give banks a prediction if a customer is going to stay with them, which we will define as churn. We used models like Ludwig, as the engine to create churn predictions from our CSV data, and streamlit to create our UI. We aimed to create an environment where potential users can find out the retention of bank customers, given some data about that particular customer.  We also give banks opportunity to use openAI models to analyze important factors affecting churn, personalized for each customer.  Adding on to this, banks can also inquire further/specific questions via the Churn Chatbot.

# Features:
```
Churn Prediction using Ludwig ML model trained on .csv file of that particular bank's customer data.
```
```
Summary Analysis using chatGPT to identify key factors impacting customer churn and recommend
retention strategies based on individual data.
```
```
Chatbot functionality powered by chatGPT for tailored inquiries, enabling banks to delve deeper
into customer behavior and reasons for churn.
```
# Quick start:
1. Clone the project
```
git clone https://github.com/kevinxu523/EvaDB_Customer_Churn_App.git
cd EvaDB_Customer_Churn_App
```
2. Install the requirements
```
pip install -r requirements.txt
```
.  Run the program and start your webapp
```
python3 run_evadb.py
streamlit run "run_evadb.py"
```
# 
