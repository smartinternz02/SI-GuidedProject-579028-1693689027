from flask import Flask,render_template,request
import joblib
import pandas as pd
import os
model = joblib.load('./Flask app/rf_ model.joblib')

app = Flask(__name__)

app.static_folder = 'static'

def mapping(response):
    if response.lower() == 'spain':
        return 0,0,1
    elif response.lower()=='france':
        return 1,0,0
    else:return 0,1,0
        
@app.route('/')
def hello():
    return render_template('./index.html')

@app.route('/predict', methods=['POST'])
def process_form():
    CreditScore = request.form['CreditScore']
    Gender = request.form['Gender']
    Age = request.form['Age']
    Tenure = request.form['Tenure']
    Balance = request.form['Balance']
    NumOfProducts = request.form['NumOfProducts']
    HasCrCard = request.form['HasCrCard']
    IsActiveMember = request.form['IsActiveMember']
    EstimatedSalary = request.form['EstimatedSalary']
    country = request.form['Country']
    # data = pd.DataFrame({
    #     'CreditScore':CreditScore,
    #     'Gender':Gender,
    #     'Age':Age,
    #     'Tenure':Tenure,
    #     'Balance':Balance,
    #     'NumOfProducts':NumOfProducts,
    #     'HasCrCard':HasCrCard,
    #     'IsActiveMember':IsActiveMember,
    #     'EstimatedSalary':EstimatedSalary,
    #     'France':France,
    #     'Germany':Germany,
    #     'Spain':Spain,
    #     })
    
    France,Germany,Spain = mapping(country)
    IsActiveMember = 0 if IsActiveMember == 'Active' else 1
    Gender = 0 if Gender =='Male' else 1
    HasCrCard = 0 if HasCrCard == 'No' else 1
    NumOfProducts = int(NumOfProducts)
    data = [
        CreditScore,
        Gender,
        Age,
        Tenure,
        Balance,
        NumOfProducts,
        HasCrCard,
        IsActiveMember,
        EstimatedSalary,France,Germany,Spain
        
]
    prediction = model.predict([data])
    model_response = 'NO' if prediction[0] == 0 else 'YES'
    return render_template('successfull.html',prediction=model_response)
if __name__ == '__main__':
    app.run(debug=True)