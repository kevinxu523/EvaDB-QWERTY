# Import the EvaDB package
import evadb
import streamlit as st

# Connect to EvaDB and get a database cursor for running queries
cursor = evadb.connect().cursor()


st.title("QWERTY Churn Predictor")
st.subheader("A Machine Learning App that predicts which customers are likely to stop using a bank")
st.subheader("Enter the Following Details")

# Retrieving Input from user
credit_score = st.sidebar.slider("Credit Score", min_value=350, max_value=850)
country = st.sidebar.radio("Country of Residence", options=["France", "Spain", "Germany"], horizontal=True)
gender = st.sidebar.radio("Gender", options= ["Male", "Female"], horizontal=True)
age = st.sidebar.slider("Age", min_value=18, max_value=100)
tenure = st.sidebar.slider("From how many years he/she is having bank acc in ABC Bank", min_value=0, max_value=10)
balance = st.sidebar.slider("Account Balance", min_value=0, max_value=250000)
products_number = st.sidebar.slider("Number of Products", min_value=1, max_value=4)
credit_card = st.sidebar.slider("Does the customer have a credit card? 0 for no, 1 for yes", min_value=0, max_value=1)
active_member = st.sidebar.slider("Is the customer an active member? 0 for no, 1 for yes", min_value=0, max_value=1)

# Create a dictionary to store value
prediction_params = {
    "credit_score": credit_score,
    "country": country,
    "gender": gender,
    "age": age,
    "tenure": tenure,
    "balance": balance,
    "products_number": products_number,
    "credit_card": credit_card,
    "active_member": active_member,
}

new_data = {
    "credit_score": 700,
    "country": "France",
    "gender": "Male",
    "age": 35,
    "tenure": 5,
    "balance": 10000.0,  # Replace with the actual balance
    "products_number": 2,
    "credit_card": 1,
    "active_member": 1
}

if st.button("Load csv"):
    cursor.query("""CREATE TABLE IF NOT EXISTS 
    customers_data 
    (customer_id INTEGER NOT NULL, 
    credit_score INTEGER NOT NULL, 
    country TEXT(40) NOT NULL,
    gender TEXT(40) NOT NULL,
    age INTEGER NOT NULL,
    tenure INTEGER NOT NULL, 
    balance NDARRAY FLOAT64(1) NOT NULL, 
    products_number INTEGER NOT NULL, 
    credit_card INTEGER NOT NULL, 
    active_member INTEGER NOT NULL, 
    estimated_salary NDARRAY FLOAT64(1) NOT NULL,   
    churn INTEGER); """
    ).execute()
    cursor.query('LOAD CSV "bank_customer.csv" INTO customers_data;').execute()




if st.button("Predict"):

    #input_data will be reset if it exists
    cursor.query("DROP TABLE IF EXISTS input_data;").execute()

    #ML function
    cursor.query(
    """
    CREATE FUNCTION IF NOT EXISTS PredictChurn FROM
    ( SELECT credit_score,
    country,
    gender,
    age,
    tenure,
    balance,
    products_number,
    credit_card,
    active_member, churn FROM  customers_data)
    TYPE Ludwig
    PREDICT 'churn'
    TIME_LIMIT 120;
    """
    ).execute()

    #create input_data, will only have 1 tuple
    cursor.query("""CREATE TABLE IF NOT EXISTS input_data 
    (credit_score INTEGER NOT NULL, 
    country TEXT(40) NOT NULL,
    gender TEXT(40) NOT NULL,
    age INTEGER NOT NULL,
    tenure INTEGER NOT NULL, 
    balance NDARRAY FLOAT64(1) NOT NULL, 
    products_number INTEGER NOT NULL, 
    credit_card INTEGER NOT NULL, 
    active_member INTEGER NOT NULL, 
    churn INTEGER); """
    ).execute()

    #insert to input_data from frontend parameters
    insert_query = f"""
    INSERT INTO input_data 
    (credit_score, country, gender, age, tenure, balance, products_number, credit_card, active_member, churn)
    VALUES 
    ({prediction_params['credit_score']}, '{prediction_params['country']}', '{prediction_params['gender']}', {prediction_params['age']},
    {prediction_params['tenure']}, {prediction_params['balance']}, {prediction_params['products_number']}, {prediction_params['credit_card']}, 
    {prediction_params['active_member']}, 1);"""
    cursor.query(insert_query).execute()

    data = cursor.query("SELECT PredictChurn(*) FROM input_data LIMIT 1;").df()

    tf = data['predictchurn.churn_predictions'][0]
    if tf == False:
        st.write(f"This customer is likely to stop using the bank. Please contact them to discuss their account and how they feel about the bank.")
    else:
        st.success(f"This customer is not likely to stop using the bank!")

