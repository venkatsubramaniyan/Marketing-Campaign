#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template, request

#import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
app = Flask(__name__)
model = pickle.load(open('classifier.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
scaler = MinMaxScaler()
@app.route("/predict", methods=['POST'])
def predict():
    
    if request.method == 'POST':
        Daily_Time_Spent_on_Site = float(request.form['Daily Time Spent on Site'])
        Age=int(request.form['Age'])
        log_age=np.log(Age)
        Area_Income=float(request.form['Area Income'])
        Daily_Internet_Usage=float(request.form['Daily Internet Usage'])
        Gender=request.form['Gender']
        if(Gender=='Male'):
            Male=1
                
        if(Gender=='Female'):
            Male=0
        values=np.array([Daily_Time_Spent_on_Site,Area_Income,Daily_Internet_Usage,Male,log_age]) 
        values=values.reshape(1,-1)
        values_transformed=scaler.fit_transform(values)
           
      
        prediction=model.predict(values_transformed)
        output=round(prediction[0])
        if output==0:
            return render_template('index.html',prediction_texts="Not Going to Click on Ad")
        else:
            return render_template('index.html',prediction_text="Going to Click on Ad")
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

