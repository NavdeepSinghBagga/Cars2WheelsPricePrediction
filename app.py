# Importing essential libraries
from flask import Flask, render_template, request
from flask import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
from flask import Flask, make_response
from flask_mongoengine import MongoEngine


app = Flask(__name__)

model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
# Load the Random Forest CLassifier model


database_name = "feedbak"
DB_URI = "mongodb+srv://tryuser:tryuser@cluster0.fwuun.mongodb.net/feedbak?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)

class respo(db.Document):
    user_id = db.IntField()
    name = db.StringField()
    resp = db.StringField()

    def to_json(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "resp": self.resp
        }
class cont(db.Document):
    user_id = db.IntField()
    name = db.StringField()
    email = db.StringField()
    subject = db.StringField()
    message = db.StringField()

    def to_json(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "subject": self.subject,
            "message": self.message
        }


@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route('/feedback',methods=['GET'])
def index():
    return render_template('feedback.html')
@app.route('/contact',methods=['GET'])
def index1():
    return render_template('contact.html')

standard_to = StandardScaler()

@app.route('/predict', methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        Year=2020-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0	
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {} Lakhs".format(output))
    else:
        return render_template('index.html')


@app.route('/feed_uploaded',methods = ['POST'])
def uploaded():
    Name = request.form['Name']
    FBK = request.form['Feed_Back']
    fb1 = respo(name=Name,resp=FBK)
    # fb1 = respo(user_id=1,name="Maya",resp="Well tried")
    fb1.save()
    return render_template('index.html')
@app.route('/contact_uploaded',methods = ['POST'])
def uploadedcont():
    Name = request.form['Name']
    Email = request.form['Email']
    Subject = request.form['Subject']
    Message = request.form['Message']
    cont1 = cont(name=Name,email=Email,subject=Subject,message=Message)
    
    if(Name == "" or Email == "" or Subject == "" or Message == "" ):
        return render_template('contact.html')
    else:
        cont1.save()
    return render_template('index.html')


if __name__ == '__main__':
	app.run(debug=True)