from app.home import blueprint
from flask import render_template,request,escape
from flask_login import login_required
from app.base.models import User,SentM,ReceiveM
from app import db

from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse
import requests

# put your own credentials here
account_sid = "ACffe02b6e6f367781b36d4251bc962952"
auth_token = "dfa6787ca8be1a3884f7736ff5557d03"

subscription_key = "56bdc3a1166c49c89304c1c9e2f8cfae"
assert subscription_key


@blueprint.route('/index',methods=['GET', 'POST'])
@login_required
def index():
    first_message = "Hi <firstName>, I saw that your <productType> was delivered. How are you enjoying it so far?"
    positive = "Great, can you describe what you love most about <productType> ? "
    negative = "I'm sorry to hear that, what do you dislike about <productType> ?"
    if request.method == 'POST':
        #Get everything from the form
        number = request.form['number']
        prodType = request.form['prodType'] 
        name = request.form['fullname']
        firstname = name.split()
        firstname = firstname[0]
        first_message = first_message.replace("<firstName>",firstname)
        first_message = first_message.replace("<productType>",prodType)
        positive = positive.replace("<productType>",prodType)
        negative = negative.replace("<productType>",prodType)
        
        #Twilio message send
        client = Client(account_sid, auth_token)
        client.messages.create(
          to=number,
          from_="+13092710302",
          body=first_message)
        
        #DB storage
        sentM = SentM(phoneNum=number,name=name,text=first_message,prodtype=prodType)
        db.session.add(sentM)
        db.session.commit()
        
        
        render_template('index.html',first_message=escape(first_message),positive=escape(positive),negative=escape(negative))   
    return render_template('index.html',first_message=first_message,positive=positive,negative=negative)  


@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')


@blueprint.route("/reply", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""
    number = request.form['From']
    message_body = request.form['Body']
    
    
    text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
    sentiment_api_url = text_analytics_base_url + "sentiment"
    
    #message_body1 = "Hi, they're great, thanks for asking"
    #message_body2 = "Hi, I don't like it that much unfortunately"
    
    documents = {'documents' : 
                [
                    {'id': '1', 'language': 'en', 'text': message_body},
                ]
                }
    headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
    response  = requests.post(sentiment_api_url, headers=headers, json=documents)
    sentiments = response.json()
    print(sentiments)
    
    senti_score = sentiments['documents'][0]['score']
    
    #Connect to DB to get product type
    sentM = SentM.query.filter_by(phoneNum=number).first()
    prodType = sentM.prodtype
    
    resp = MessagingResponse()
    
    if senti_score > 0.5:
        #positive
        response_text = "Great,can you describe what you love most about "+str(prodType)
        resp.message(response_text)
    else:
        #negative
        response_text = "I'm sorry to hear that,what do you dislike about "+str(prodType)
        resp.message(response_text)
        

    return str(resp)
