from flask import Flask, render_template, redirect, url_for,request,send_from_directory,jsonify,session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy import and_, or_, not_,any_
from datetime import datetime, timedelta
from ast import literal_eval
import pytz
import requests
import json
import os
import re
from backtesting import Backtest, Strategy
import pandas as pd
#Data Source
import yfinance as yf
from datetime import datetime
import time
import os
from scipy import stats

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,PostbackEvent, TextMessage,StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage, TextSendMessage, FlexSendMessage,QuickReply,QuickReplyButton,MessageAction,PostbackAction,URIAction,VideoSendMessage
)

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
app.secret_key = b'aU?T2c@gxkE5n!&]MyS~'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
Session(app)
line_bot_api = LineBotApi('PCoy6drFTi7IJPBaBfB7aUmVQDBxnbNHpd7XZh5xCEX7ufPg62KKK7vO0HO2zN9U/u4dcvXvR3b3UsUsbGQNYMlObLM7rR/J0Rpq1z8KGPKrH2u7ZRXqBkB7xFnIK/0bNKWULMDEitKJcp+KvZQXCgdB04t89/1O/w1cDnyilFU=')



# Google Cloud SQL (change this accordingly)
PASSWORD =os.environ.get('PASSWORD')
USERNAME =os.environ.get('USERNAME')
DBNAME =os.environ.get('DBNAME')
PROJECT_ID =os.environ.get('PROJECT_ID')
INSTANCE_NAME =os.environ.get('INSTANCE_NAME') 
# configuration
app.config["SECRET_KEY"] = "7rFz5RsN12d3YnuKcnD4EWDmy1yxFWnu"
app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+pymysql://{USERNAME}:{PASSWORD}@/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True


db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text)
    alert1 = db.Column(db.Text)
    label1 = db.Column(db.Text)
    color1 = db.Column(db.Text)
    cryptocurrency1 = db.Column(db.Text)
    federalcurrency1 = db.Column(db.Text)
    candlestick1 = db.Column(db.Text)
    category1 = db.Column(db.Text)
    trend1 = db.Column(db.Text)
    timeframe1 = db.Column(db.Text)
    alert2 = db.Column(db.Text)
    label2 = db.Column(db.Text)
    color2 = db.Column(db.Text)
    cryptocurrency2 = db.Column(db.Text)
    federalcurrency2 = db.Column(db.Text)
    candlestick2 = db.Column(db.Text)
    category2 = db.Column(db.Text)
    trend2 = db.Column(db.Text)
    timeframe2 = db.Column(db.Text)
    alert3 = db.Column(db.Text)
    label3 = db.Column(db.Text)
    color3 = db.Column(db.Text)
    cryptocurrency3 = db.Column(db.Text)
    federalcurrency3 = db.Column(db.Text)
    candlestick3 = db.Column(db.Text)
    category3 = db.Column(db.Text)
    trend3 = db.Column(db.Text)
    timeframe3 = db.Column(db.Text)
    exp = db.Column(db.TIMESTAMP)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

class alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Symbol = db.Column(db.Text)
    Timeframe = db.Column(db.Text)
    Trend = db.Column(db.Text)
    Status = db.Column(db.Text)
    TEXT = db.Column(db.Text)
    Close = db.Column(db.Float)
    RSI = db.Column(db.Text)
    STO = db.Column(db.Text)
    ts = db.Column(db.TIMESTAMP)

class federal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Symbol = db.Column(db.Text)
    Timeframe = db.Column(db.Text)
    Trend = db.Column(db.Text)
    Status = db.Column(db.Text)
    TEXT = db.Column(db.Text)
    Close = db.Column(db.Float)
    RSI = db.Column(db.Text)
    STO = db.Column(db.Text)
    ts = db.Column(db.TIMESTAMP)

def addusers(uuid,exp):
    with app.app_context():
        check = users.query.filter(users.uuid == uuid).all()
        if not check:
            data = users(uuid=uuid,exp=exp)
            db.session.add(data)
            db.session.commit()

def addalert(Symbol,Timeframe,Trend,Status,TEXT,Close,RSI,STO,TS):
    with app.app_context():
        data = alert(Symbol=Symbol,Timeframe=Timeframe,Trend=Trend,Status=Status,TEXT=TEXT,Close=Close,RSI=RSI,STO=STO,ts=TS)
        db.session.add(data)
        db.session.commit()

def addfederal(Symbol,Timeframe,Trend,Status,TEXT,Close,RSI,STO,TS):
    with app.app_context():
        data = federal(Symbol=Symbol,Timeframe=Timeframe,Trend=Trend,Status=Status,TEXT=TEXT,Close=Close,RSI=RSI,STO=STO,ts=TS)
        db.session.add(data)
        db.session.commit()
@app.route('/login', methods=['POST'])
def login():
    session["isLoggedIn"] = request.form['LoggedIn']
    return 'checklogin'

def config(alert1,alert2,alert3):
        category = []

@app.route('/setting', methods=['GET','POST'])
def setting():
    try:
        if session["isLoggedIn"] == 'true':
            uuid = session["uuid"]
            config = users.query.filter(users.uuid == uuid).first()

            crypto = alert.query.with_entities(alert.Symbol).group_by(alert.Symbol).all()
            forex = alert.query.with_entities(federal.Symbol).group_by(federal.Symbol).all()

            if request.method == "GET":
                return render_template('setting.html',config=config,crypto=crypto,forex=forex,alert=[{'title':'alert1'},{'title':'alert2'},{'title':'alert3'}])
            elif request.method == "POST":
                config.alert1 = str(request.form.getlist('alert1_ON'))
                config.label1 = str(request.form.getlist('alert1_name'))
                config.color1 = str(request.form.getlist('alert1_color'))
                config.cryptocurrency1 = str(request.form.getlist('alert1_cryptocurrency'))
                config.federalcurrency1 = str(request.form.getlist('alert1_federalcurrency'))
                config.candlestick1 = str(request.form.getlist('alert1_candlestick'))
                config.category1 = str(request.form.getlist('alert1_Category'))
                config.trend1 = str(request.form.getlist('alert1_Trend'))
                config.timeframe1 = str(request.form.getlist('alert1_Timeframe'))

                config.alert2 = str(request.form.getlist('alert2_ON'))
                config.label2 = str(request.form.getlist('alert2_name'))
                config.color2 = str(request.form.getlist('alert2_color'))
                config.cryptocurrency2 = str(request.form.getlist('alert2_cryptocurrency'))
                config.federalcurrency2 = str(request.form.getlist('alert2_federalcurrency'))
                config.candlestick2 = str(request.form.getlist('alert2_candlestick'))
                config.category2 = str(request.form.getlist('alert2_Category'))
                config.trend2 = str(request.form.getlist('alert2_Trend'))
                config.timeframe2 = str(request.form.getlist('alert2_Timeframe'))

                config.alert3 = str(request.form.getlist('alert3_ON'))
                config.label3 = str(request.form.getlist('alert3_name'))
                config.color3 = str(request.form.getlist('alert3_color'))
                config.cryptocurrency3 = str(request.form.getlist('alert3_cryptocurrency'))
                config.federalcurrency3 = str(request.form.getlist('alert3_federalcurrency'))
                config.candlestick3 = str(request.form.getlist('alert3_candlestick'))
                config.category3 = str(request.form.getlist('alert3_Category'))
                config.trend3 = str(request.form.getlist('alert3_Trend'))
                config.timeframe3 = str(request.form.getlist('alert3_Timeframe'))

                db.session.commit()
                
                config = users.query.filter(users.uuid == uuid).first()
                print(config.timeframe3)
                exp_alert='บันทึกสำเร็จ'
                return render_template('setting.html',exp_alert=exp_alert,crypto=crypto,forex=forex,config=config,alert=[{'title':'alert1'},{'title':'alert2'},{'title':'alert3'}])
        else:
            return render_template('index.html')
    except:
        exp_alert='เซสชั่นหมดอายุ'
        return render_template('index.html',exp_alert=exp_alert)

@app.route('/register', methods=['POST'])
def register():
    if request.method == "POST":
        token = request.form['idtoken']
        access_token = request.form['AccessToken']
        
        url = f"https://api.line.me/oauth2/v2.1/verify?access_token={access_token}"
        h = {
        "Content-Type":"application/x-www-form-urlencoded"
        }
        params = {
            "id_token":token,
            "client_id":"1661115732"
        }
        r = requests.post(url, headers=h, params=params)
        data = r.json()
        uuid = data.get('sub')
        session["uuid"] = uuid
        exp = datetime(2023, 1, 1)
        addusers(uuid,exp)
        return 'register'

@app.route('/', methods=['GET'])
def index():
        
    return render_template('index.html')

@app.route('/divergence', methods=['GET'])
def divergence():
        
    return render_template('divergence.html')

@app.route('/keylevels', methods=['GET'])
def keylevels():
        
    return render_template('keylevels.html')

@app.route('/breakout', methods=['GET'])
def breakout():
        
    return render_template('breakout.html')

@app.route('/trailingstop', methods=['GET'])
def trailingstop():
        
    return render_template('trailingstop.html')

@app.route('/candlestick', methods=['GET'])
def candlestick():
        
    return render_template('candlestick.html')

@app.route('/strategy', methods=['GET'])
def strategy():
        
    return render_template('strategy.html')

@app.route('/howto', methods=['GET'])
def howto():
        
    return render_template('howto.html')

@app.route('/quiz', methods=['GET','POST'])
def quiz():
        
    return render_template('quiz.html')

@app.route('/Cryptocurrency', methods=['GET','POST'])
def Cryptocurrency():
    if request.method == "GET":
        search = request.args.get('symbol')
        category = request.args.get('category')
        if not category:
            if search:
                data = alert.query.filter(alert.Symbol == search).order_by(alert.id.desc()).limit(50).all()   
            else:
                data = alert.query.order_by(alert.id.desc()).limit(50).all()
        else:
            if category == "Support-Resistance":
                category = category.split('-')
                Support = category[0]
                Resistance = category[1]
                Support = "{}%".format(Support)
                Resistance = "{}%".format(Resistance)
                if search:
                    data = alert.query.filter(and_(alert.Symbol == search),or_(alert.Status.like(Support),alert.Status.like(Resistance))).order_by(alert.id.desc()).limit(50).all()
                else:
                    data = alert.query.filter(or_(alert.Status.like(Support),alert.Status.like(Resistance))).order_by(alert.id.desc()).limit(50).all()
            else:
                if category == "Candlestick":
                    category = "Candle"
                category = "%{}%".format(category)
                if search:
                    data = alert.query.filter(and_(alert.Symbol == search),or_(alert.Status.like(category))).order_by(alert.id.desc()).limit(50).all()
                else:
                    data = alert.query.filter(alert.Status.like(category)).order_by(alert.id.desc()).limit(50).all()
        now = datetime.now()
        for i in range(len(data)):
            try:
                data[i].Close = format(data[i].Close,'f')
            except:
                pass
            try:
                text =  data[i].TEXT.replace('-','').replace('?','').replace('!','').split('See')[0].split('อารมณ์ : ')[1]
            except:
                text = data[i].TEXT.replace('-','').replace('?','').replace('!','')
            data[i].TEXT = text
            try:
                Timeframe = data[i].Timeframe.split('M')[0].split(' ')[0].strip()
            except:
                Timeframe = data[i].Timeframe
            data[i].Symbol = data[i].Symbol+' ('+Timeframe+' Minutes)'
            data[i].id = data[i].ts + timedelta(hours=7)
            try:
                try:
                    time_status = now - data[i].ts
                    time_status = str(time_status).split('.')[0]
                    time_status_split = str(time_status).split(',')
                    time_status_split_second = time_status_split[1].split(':')
                    
                    if time_status_split[0] == "1 day":
                        data[i].ts = time_status_split[0] + ' ago'
                    elif time_status_split[0] != "1" and time_status_split[0] != "0":
                        data[i].ts = time_status_split[0] + ' ago'

                except:
                    time_status = now - data[i].ts
                    time_status_split = str(time_status).split('.')[0]
                    time_status_split_second = time_status_split.split(':')
                    if time_status_split_second[0] == "1":
                        data[i].ts = time_status_split_second[0] + ' Hour ago'
                    elif time_status_split_second[0] != "1" and time_status_split_second[0] != "0":
                        data[i].ts = time_status_split_second[0] + ' Hours ago'
                    elif time_status_split_second[1] == "01":
                        data[i].ts = time_status_split_second[1] + ' minute ago'
                    elif time_status_split_second[1] != "01" and time_status_split_second[1] != "00":
                        data[i].ts = time_status_split_second[1] + ' minutes ago'
            except:
                data[i].ts = 'now'
                pass
        return render_template('Cryptocurrency.html',table_data=data)

    elif request.method == "POST":
        category = []
        timeframe = []
        Trend = []
        try:
            symbol = request.form['symbol']
            
            symbol = "%{}%".format(symbol)
        except:
            symbol = "%{}%".format('USDT')
        try:
            Candlestick = request.form['Candlestick']
            Candlestick = "Candle"
            Candlestick = "%{}%".format(Candlestick)
            category.append(Candlestick)
        except:
            Candlestick = None

        try:
            Bullish_Divergence = request.form['Bullish-Divergence']
            Bullish_Divergence = "Bullish Divergence"
            Bullish_Divergence = "%{}%".format(Bullish_Divergence)
            category.append(Bullish_Divergence)
        except:
            Bullish_Divergence = None
        try:
            Bearish_Divergence = request.form['Bearish-Divergence']
            Bearish_Divergence = "Bearish Divergence"
            Bearish_Divergence = "%{}%".format(Bearish_Divergence)
            category.append(Bearish_Divergence)
        except:
            Bullish_Divergence = None
        try:
            Breakout = request.form['Breakout']
            Breakout = "Breakout"
            Breakout = "%{}%".format(Breakout)
            category.append(Breakout)
        except:
            Breakout = None
        try:
            Support = request.form['Support']
            Support = "Support"
            Support = "{}%".format(Support)
            category.append(Support)
        except:
            Support = None
        try:
            Resistance = request.form['Resistance']
            Resistance = "Resistance"
            Resistance = "{}%".format(Resistance)
            category.append(Resistance)
        except:
            Resistance = None
        try:
            Bullish = request.form['Bullish']
            Bullish = "Bullish"
            Bullish = "%{}%".format(Bullish)
            Trend.append(Bullish)
        except:
            Bullish = None
        try:
            Bearish = request.form['Bearish']
            Bearish = "Bearish"
            Bearish = "%{}%".format(Bearish)
            Trend.append(Bearish)
        except:
            Bearish = None
        try:
            timeframe15 = request.form['15mn']
            timeframe15 = "%{}%".format("15")
            timeframe.append(timeframe15)
        except:
            timeframe15 = None
        try:
            timeframe30 = request.form['30mn']
            timeframe30 = "%{}%".format("30")
            timeframe.append(timeframe30)
        except:
            timeframe30 = None
        try:
            timeframe1hr = request.form['60mn']
            timeframe1hr = "%{}%".format("60")
            timeframe.append(timeframe1hr)
        except:
            timeframe1hr = None

        try:
            timeframe4hr = request.form['240mn']
            timeframe4hr = "%{}%".format("240")
            timeframe.append(timeframe4hr)
        except:
            timeframe4hr = None
        if category:
            category = [alert.Status.like(elem) for elem in category]
        if timeframe:
            timeframe = [alert.Timeframe.like(elem) for elem in timeframe]
        if Trend:
            Trend = [alert.Trend.like(elem) for elem in Trend]

        if symbol and not category and not timeframe and not Trend:
            data = alert.query.filter(alert.Symbol.like(symbol)).order_by(alert.id.desc()).limit(50).all()
        elif symbol and category and timeframe and not Trend:
            data = alert.query.filter(and_(alert.Symbol.like(symbol),or_(*category),or_(*timeframe))).order_by(alert.id.desc()).limit(50).all() 
        elif symbol and category and not timeframe and not Trend:
            data = alert.query.filter(and_(alert.Symbol.like(symbol),or_(*category))).order_by(alert.id.desc()).limit(50).all()
        elif symbol and category and not timeframe and Trend:
            data = alert.query.filter(and_(alert.Symbol.like(symbol),or_(*category),or_(*Trend))).order_by(alert.id.desc()).limit(50).all()
        elif symbol and not category and timeframe  and not Trend:
            data = alert.query.filter(and_(alert.Symbol.like(symbol),or_(*timeframe))).order_by(alert.id.desc()).limit(50).all()
        elif symbol and not category and timeframe  and Trend:
            data = alert.query.filter(and_(alert.Symbol.like(symbol),or_(*timeframe),or_(*Trend))).order_by(alert.id.desc()).limit(50).all()
        elif symbol and not category and not timeframe and Trend:
            data = alert.query.filter(and_(alert.Symbol.like(symbol),or_(*Trend))).order_by(alert.id.desc()).limit(50).all()
        elif symbol and category and timeframe and Trend:
            data = alert.query.filter(and_(alert.Symbol.like(symbol),or_(*category),or_(*timeframe),or_(*Trend))).order_by(alert.id.desc()).limit(50).all() 
        else:
            data = alert.query.order_by(alert.id.desc()).limit(50).all()
        
        try:
            now = datetime.now()
            for i in range(len(data)):
                try:
                    data[i].Close = format(data[i].Close,'f')
                except:
                    pass
                try:
                    text =  data[i].TEXT.replace('-','').replace('?','').replace('!','').split('See')[0].split('อารมณ์ : ')[1]
                except:
                    text = data[i].TEXT.replace('-','').replace('?','').replace('!','')
                data[i].TEXT = text
                try:
                    Timeframe = data[i].Timeframe.split('M')[0].split(' ')[0].strip()
                except:
                    Timeframe = data[i].Timeframe
                data[i].TEXT = text
                data[i].Symbol = data[i].Symbol+' ('+Timeframe+' Minutes)'
                data[i].id = data[i].ts + timedelta(hours=7)
                try:
                    try:
                        time_status = now - data[i].ts
                        time_status = str(time_status).split('.')[0]
                        time_status_split = time_status.split(',')
                        time_status_split_second = time_status_split[1].split(':')
                        
                        if time_status_split[0] == "1 day":
                            data[i].ts = time_status_split[0] + ' ago'
                        elif time_status_split[0] != "1" and time_status_split[0] != "0":
                            data[i].ts = time_status_split[0] + ' ago'
                        
                    except:
                        time_status = now - data[i].ts
                        time_status_split = str(time_status).split('.')[0]
                        time_status_split_second = str(time_status_split).split(':')
                        if time_status_split_second[0] == "1":
                            data[i].ts = time_status_split_second[0] + ' Hour ago'
                        elif time_status_split_second[0] != "1" and time_status_split_second[0] != "0":
                            data[i].ts = time_status_split_second[0] + ' Hours ago'
                        elif time_status_split_second[1] == "01":
                            data[i].ts = time_status_split_second[1] + ' minute ago'
                        elif time_status_split_second[1] != "01" and time_status_split_second[1] != "00":
                            data[i].ts = time_status_split_second[1] + ' minutes ago'
                except:
                    data[i].ts = 'now'
                    pass
        except:
            return render_template('Cryptocurrency.html')
    return render_template('Cryptocurrency.html',table_data=data)

@app.route('/Federalcurrency', methods=['GET','POST'])
def Federalcurrency():
    if request.method == "GET":
        search = request.args.get('symbol')
        category = request.args.get('category')
        if not category:
            if search:
                data = federal.query.filter(federal.Symbol == search).order_by(federal.id.desc()).limit(50).all()
            else:
                data = federal.query.filter().order_by(federal.id.desc()).limit(50).all()
        else:               
            if category == "Support-Resistance":
                category = category.split('-')
                Support = category[0]
                Resistance = category[1]
                Support = "{}%".format(Support)
                Resistance = "{}%".format(Resistance)
                if search:
                    data = federal.query.filter(and_(alert.Symbol == search),or_(federal.Status.like(Support),federal.Status.like(Resistance))).order_by(federal.id.desc()).limit(50).all()
                else:
                    data = federal.query.filter(or_(federal.Status.like(Support),federal.Status.like(Resistance))).order_by(federal.id.desc()).limit(50).all()
            else:
                if category == "Candlestick":
                    category = "Candle"
                category = "%{}%".format(category)
                if search:
                    data = federal.query.filter(and_(alert.Symbol == search),or_(federal.Status.like(category))).order_by(federal.id.desc()).limit(50).all()
                else:
                    data = federal.query.filter(federal.Status.like(category)).order_by(federal.id.desc()).limit(50).all()
        now = datetime.now()
        for i in range(len(data)):
            try:
                data[i].Close = format(data[i].Close,'f')
            except:
                pass
            try:
                text =  data[i].TEXT.replace('-','').replace('?','').replace('!','').split('See')[0].split('อารมณ์ : ')[1]
            except:
                text = data[i].TEXT.replace('-','').replace('?','').replace('!','')
                data[i].TEXT = text
            try:
                Timeframe = data[i].Timeframe.split('M')[0].split(' ')[0].strip()
            except:
                Timeframe = data[i].Timeframe
            data[i].TEXT = text
            data[i].Symbol = data[i].Symbol+' ('+Timeframe+' Minutes)'
            data[i].id = data[i].ts + timedelta(hours=7)
            
            try:
                try:
                    time_status = now - data[i].ts
                    time_status = str(time_status).split('.')[0]
                    time_status_split = time_status.split(',')
                    time_status_split_second = time_status_split[1].split(':')

                    if time_status_split[0] == "1 day":
                        data[i].ts = time_status_split[0] + ' ago'
                    elif time_status_split[0] != "1" and time_status_split[0] != "0":
                        data[i].ts = time_status_split[0] + ' ago'

                except:
                    time_status = now - data[i].ts
                    time_status_split = str(time_status).split('.')[0]
                    time_status_split_second = time_status_split.split(':')

                    if time_status_split_second[0] == "1":
                        data[i].ts = time_status_split_second[0] + ' Hour ago'
                    elif time_status_split_second[0] != "1" and time_status_split_second[0] != "0":
                        data[i].ts = time_status_split_second[0] + ' Hours ago'
                    elif time_status_split_second[1] == "01":
                        data[i].ts = time_status_split_second[1] + ' minute ago'
                    elif time_status_split_second[1] != "01" and time_status_split_second[1] != "00":
                        data[i].ts = time_status_split_second[1] + ' minutes ago'
            except:
                data[i].ts = 'now'
                pass
            
           
        return render_template('Federalcurrency.html',table_data=data)

    elif request.method == "POST":
        category = []
        timeframe = []
        Trend = []
        try:
            symbol = request.form['symbol']
            
            symbol = "%{}%".format(symbol)
        except:
            symbol = "%{}%".format('USDT')
        try:
            Candlestick = request.form['Candlestick']
            Candlestick = "Candle"
            Candlestick = "%{}%".format(Candlestick)
            category.append(Candlestick)
        except:
            Candlestick = None
        try:
            Bullish_Divergence = request.form['Bullish-Divergence']
            Bullish_Divergence = "Bullish Divergence"
            Bullish_Divergence = "%{}%".format(Bullish_Divergence)
            category.append(Bullish_Divergence)
        except:
            Bullish_Divergence = None
        try:
            Bearish_Divergence = request.form['Bearish-Divergence']
            Bearish_Divergence = "Bearish Divergence"
            Bearish_Divergence = "%{}%".format(Bearish_Divergence)
            category.append(Bearish_Divergence)
        except:
            Bullish_Divergence = None
        try:
            Breakout = request.form['Breakout']
            Breakout = "Breakout"
            Breakout = "%{}%".format(Breakout)
            category.append(Breakout)
        except:
            Breakout = None
        try:
            Support = request.form['Support']
            Support = "Support"
            Support = "{}%".format(Support)
            category.append(Support)
        except:
            Support = None
        try:
            Resistance = request.form['Resistance']
            Resistance = "Resistance"
            Resistance = "{}%".format(Resistance)
            category.append(Resistance)
        except:
            Resistance = None
        try:
            Bullish = request.form['Bullish']
            Bullish = "Bullish"
            Bullish = "%{}%".format(Bullish)
            Trend.append(Bullish)
        except:
            Bullish = None
        try:
            Bearish = request.form['Bearish']
            Bearish = "Bearish"
            Bearish = "%{}%".format(Bearish)
            Trend.append(Bearish)
        except:
            Bearish = None
        try:
            timeframe15 = request.form['15mn']
            timeframe15 = "%{}%".format("15")
            timeframe.append(timeframe15)
        except:
            timeframe15 = None
        try:
            timeframe30 = request.form['30mn']
            timeframe30 = "%{}%".format("30")
            timeframe.append(timeframe30)
        except:
            timeframe30 = None
        try:
            timeframe1hr = request.form['60mn']
            timeframe1hr = "%{}%".format("60")
            timeframe.append(timeframe1hr)
        except:
            timeframe1hr = None

        try:
            timeframe4hr = request.form['240mn']
            timeframe4hr = "%{}%".format("240")
            timeframe.append(timeframe4hr)
        except:
            timeframe4hr = None
        if category:
            category = [federal.Status.like(elem) for elem in category]
        if timeframe:
            timeframe = [federal.Timeframe.like(elem) for elem in timeframe]
        if Trend:
            Trend = [federal.Trend.like(elem) for elem in Trend]

        if symbol and not category and not timeframe and not Trend:
            data = federal.query.filter(federal.Symbol.like(symbol)).order_by(federal.id.desc()).limit(50).all()
        elif symbol and category and timeframe and not Trend:
            data = federal.query.filter(and_(federal.Symbol.like(symbol),or_(*category),or_(*timeframe))).order_by(federal.id.desc()).limit(50).all() 
        elif symbol and category and not timeframe and not Trend:
            data = federal.query.filter(and_(federal.Symbol.like(symbol),or_(*category))).order_by(federal.id.desc()).limit(50).all()
        elif symbol and category and not timeframe and Trend:
            data = federal.query.filter(and_(federal.Symbol.like(symbol),or_(*category),or_(*Trend))).order_by(federal.id.desc()).limit(50).all()
        elif symbol and not category and timeframe  and not Trend:
            data = federal.query.filter(and_(federal.Symbol.like(symbol),or_(*timeframe))).order_by(federal.id.desc()).limit(50).all()
        elif symbol and not category and timeframe  and Trend:
            data = federal.query.filter(and_(federal.Symbol.like(symbol),or_(*timeframe),or_(*Trend))).order_by(federal.id.desc()).limit(50).all()
        elif symbol and not category and not timeframe and Trend:
            data = federal.query.filter(and_(federal.Symbol.like(symbol),or_(*Trend))).order_by(federal.id.desc()).limit(50).all()
        elif symbol and category and timeframe and Trend:
            data = federal.query.filter(and_(federal.Symbol.like(symbol),or_(*category),or_(*timeframe),or_(*Trend))).order_by(federal.id.desc()).limit(50).all() 
        else:
            data = federal.query.order_by(federal.id.desc()).limit(50).all()
        now = datetime.now()
        try:
            for i in range(len(data)):
                try:
                    data[i].Close = format(data[i].Close,'f')
                except:
                    pass
                try:
                    text =  data[i].TEXT.replace('-','').replace('?','').replace('!','').split('See')[0].split('อารมณ์ : ')[1]
                except:
                    text = data[i].TEXT.replace('-','').replace('?','').replace('!','')
                data[i].TEXT = text
                try:
                    Timeframe = data[i].Timeframe.split('M')[0].split(' ')[0].strip()
                except:
                    Timeframe = data[i].Timeframe
                data[i].TEXT = text
                data[i].Symbol = data[i].Symbol+' ('+Timeframe+' Minutes)'
                data[i].id = data[i].ts + timedelta(hours=7)
                try:
                    try:
                        time_status = now - data[i].ts
                        time_status = str(time_status).split('.')[0]
                        time_status_split = time_status.split(',')
                        time_status_split_second = time_status_split[1].split(':')
                        
                        if time_status_split[0] == "1 day":
                            data[i].ts = time_status_split[0] + ' ago'
                        elif time_status_split[0] != "1" and time_status_split[0] != "0":
                            data[i].ts = time_status_split[0] + ' ago'

                    except:
                        time_status = now - data[i].ts
                        time_status_split = str(time_status).split('.')[0]
                        time_status_split_second = time_status_split.split(':')

                        if time_status_split_second[0] == "1":
                            data[i].ts = time_status_split_second[0] + ' Hour ago'
                        elif time_status_split_second[0] != "1" and time_status_split_second[0] != "0":
                            data[i].ts = time_status_split_second[0] + ' Hours ago'
                        elif time_status_split_second[1] == "01":
                            data[i].ts = time_status_split_second[1] + ' minute ago'
                        elif time_status_split_second[1] != "01" and time_status_split_second[1] != "00":
                            data[i].ts = time_status_split_second[1] + ' minutes ago'
                except:
                    data[i].ts = 'now'
                    pass
        except:
            return render_template('Federalcurrency.html')
    return render_template('Federalcurrency.html',table_data=data)
def read_json(type,SYMBOL,RSI,CLOSE,STATUS,COLOR,TEXT,TREND,TIMEFRAME,TS,STO,label,color):
    with open("static/flex.json", "r", encoding="utf8") as jsonFile:
        data = json.load(jsonFile)
    #SYMBOL
    data["header"]["contents"][0]["contents"][0]["text"] = SYMBOL+'   '+'#'+label
    #label color
    data["header"]["contents"][0]["contents"][0]["color"] = color
    #RSI
    data["header"]["contents"][1]["contents"][0]["text"] = "RSI: "+RSI
    #STO
    data["header"]["contents"][1]["contents"][1]["text"] = "STO: "+STO
    #CLOSE
    data["header"]["contents"][1]["contents"][2]["text"] = "CLOSE: "+CLOSE+"$"
    #tradingview-uri
    data["header"]["action"]["uri"] = "https://mytradepro-6z6rwazrna-uc.a.run.app/"+type+"?symbol="+SYMBOL+"&category="+STATUS.split(":")[0].replace(" ","")
    #tradingview-altUri-desktop
    data["header"]["action"]["altUri"]["desktop"] = "https://mytradepro-6z6rwazrna-uc.a.run.app/"+type+"?symbol="+SYMBOL+"&category="+STATUS.split(":")[0].replace(" ","")
    #STATUS
    data["body"]["contents"][0]["contents"][0]["text"] = STATUS
    #STATUS-COLOR
    data["body"]["contents"][0]["backgroundColor"] = COLOR
    #TEXT
    data["body"]["contents"][1]["contents"][0]['contents'][0]['text'] = TEXT
    #TREND-text
    data["body"]["contents"][1]["contents"][1]['contents'][1]['text'] = TREND
    #TREND-text-color
    data["body"]["contents"][1]["contents"][1]['contents'][1]['color'] = COLOR
    #TIMEFRAME
    data["footer"]["contents"][0]["contents"][0]["text"] = "TIMEFRAME: "+TIMEFRAME
    #TS
    data["footer"]["contents"][1]["contents"][0]["text"] = TS
    #tradingview-sm-footer
    data["footer"]["contents"][1]["contents"][1]["action"]["uri"] = "https://www.tradingview.com/chart/?symbol="+SYMBOL
    return data

@app.route('/webhook', methods=['POST'])
def webhook():

        data = json.loads(request.data.decode("utf-8"))
        data_split = data.get('Status')
        Status = data_split.split(',')[0]
        Text = data_split.split(',')[1].replace('TEXT','').replace(':','')

        SYMBOL = data.get('Symbol')
        TIMEFRAME = data.get('Timeframe').replace("Munites","Minutes")
        RSI = data.get('RSI')
        CLOSE = data.get('Close')
        STO = data.get('STO')
        STATUS = Status
        TREND = data.get('Trend')
        if TREND == "Bullish":
            arrow = '🔺'
            COLOR = "#34c86d"
        elif TREND == "Bearish":
            arrow = '🔻'
            COLOR = "#c52c2a"
        else:
            arrow = '◼️'
            COLOR = "#000000"
        TEXT = Text
        now = datetime.now()
        TS = now + timedelta(hours=7)
        TS = TS.strftime("%d/%m/%Y %H:%M:%S")
        ts = now
        #Insert data
        addalert(SYMBOL,TIMEFRAME.replace('Munites',''),TREND,STATUS,TEXT,CLOSE.replace('$',''),RSI.replace('%',''),STO.replace('%',''),ts)

        noti = '🔔'+SYMBOL+'🔔❗️ '+arrow+STATUS+arrow+' '+TEXT
        users_all = users.query.all()
        type = "Cryptocurrency"
        for i in range(len(users_all)):
            try:
                to = users_all[i].uuid
                if users_all[i].alert1 is not None and "on" in literal_eval(users_all[i].alert1):
                    if users_all[i].cryptocurrency1 is not None and SYMBOL in literal_eval(users_all[i].cryptocurrency1):
                        if (users_all[i].candlestick1 is not None or users_all[i].category1 is not None) and (STATUS.split(':')[1].strip() in literal_eval(users_all[i].candlestick1) or STATUS.split(':')[0].strip().replace('Divergence','') in literal_eval(users_all[i].category1) or STATUS.split(':')[1].strip() in literal_eval(users_all[i].category1)):
                            if users_all[i].trend1 is not None and TREND in literal_eval(users_all[i].trend1):
                                if users_all[i].timeframe1 is not None and TIMEFRAME.replace('Minutes','').strip() in literal_eval(users_all[i].timeframe1):
                                    flex_contents  =read_json(type,SYMBOL,RSI,CLOSE,STATUS,COLOR,TEXT,TREND,TIMEFRAME,TS,STO,literal_eval(users_all[i].label1)[0],literal_eval(users_all[i].color1)[0])
                                    flex_message = FlexSendMessage(alt_text=noti+' #'+literal_eval(users_all[i].label1)[0],contents=flex_contents)
                                    line_bot_api.push_message(
                                    to,
                                    flex_message
                                    )
                if users_all[i].alert2 is not None and  "on" in literal_eval(users_all[i].alert2):
                    if users_all[i].cryptocurrency2 is not None and SYMBOL in literal_eval(users_all[i].cryptocurrency2):
                        if (users_all[i].candlestick2 is not None or users_all[i].category2 is not None) and (STATUS.split(':')[1].strip() in literal_eval(users_all[i].candlestick2) or STATUS.split(':')[0].strip().replace('Divergence','') in literal_eval(users_all[i].category2) or STATUS.split(':')[1].strip() in literal_eval(users_all[i].category2)):
                            if users_all[i].trend2 is not None and TREND in literal_eval(users_all[i].trend2):
                                if users_all[i].timeframe2 is not None and TIMEFRAME.replace('Minutes','').strip() in literal_eval(users_all[i].timeframe2):
                                    flex_contents  =read_json(type,SYMBOL,RSI,CLOSE,STATUS,COLOR,TEXT,TREND,TIMEFRAME,TS,STO,literal_eval(users_all[i].label2)[0],literal_eval(users_all[i].color2)[0])
                                    flex_message = FlexSendMessage(alt_text=noti+' #'+literal_eval(users_all[i].label2)[0],contents=flex_contents)
                                    line_bot_api.push_message(
                                    to,
                                    flex_message
                                    )
                if users_all[i].alert3 is not None and "on" in literal_eval(users_all[i].alert3):
                    if users_all[i].cryptocurrency3 is not None and SYMBOL in literal_eval(users_all[i].cryptocurrency3):
                        if (users_all[i].candlestick3 is not None or users_all[i].category3 is not None) and (STATUS.split(':')[1].strip() in literal_eval(users_all[i].candlestick3) or STATUS.split(':')[0].replace('Divergence','').strip() in literal_eval(users_all[i].category3) or STATUS.split(':')[1].strip() in literal_eval(users_all[i].category3)):
                            if users_all[i].trend3 is not None and TREND in literal_eval(users_all[i].trend3):
                                if users_all[i].timeframe3 is not None and TIMEFRAME.replace('Minutes','').strip() in literal_eval(users_all[i].timeframe3):
                                    flex_contents  =read_json(type,SYMBOL,RSI,CLOSE,STATUS,COLOR,TEXT,TREND,TIMEFRAME,TS,STO,literal_eval(users_all[i].label3)[0],literal_eval(users_all[i].color3)[0])
                                    flex_message = FlexSendMessage(alt_text=noti+' #'+literal_eval(users_all[i].label3)[0],contents=flex_contents)
                                    line_bot_api.push_message(
                                    to,
                                    flex_message
                                    )
            except Exception as e:
                print(e)
                pass
    
        return { "message": "done" }, 201

    
@app.route('/webhook2', methods=['POST'])
def webhook2():

        data = json.loads(request.data.decode("utf-8"))
        data_split = data.get('Status')
        Status = data_split.split(',')[0]
        Text = data_split.split(',')[1].replace('TEXT','').replace(':','')

        SYMBOL = data.get('Symbol')
        TIMEFRAME = data.get('Timeframe').replace("Munites","Minutes")
        RSI = data.get('RSI')
        CLOSE = data.get('Close')
        STO = data.get('STO')
        STATUS = Status
        TREND = data.get('Trend')
        if TREND == "Bullish":
            arrow = '🔺'
            COLOR = "#34c86d"
        elif TREND == "Bearish":
            arrow = '🔻'
            COLOR = "#c52c2a"
        else:
            arrow = '◼️'
            COLOR = "#000000"
        TEXT = Text
        now = datetime.now()
        TS = now + timedelta(hours=7)
        TS = TS.strftime("%d/%m/%Y %H:%M:%S")
        ts = now
        #Insert data
        addfederal(SYMBOL,TIMEFRAME.replace('Munites',''),TREND,STATUS,TEXT,CLOSE.replace('$',''),RSI.replace('%',''),STO.replace('%',''),ts)

        noti = '🔔'+SYMBOL+'🔔❗️ '+arrow+STATUS+arrow+' '+TEXT
        uuid = users.query.with_entities(users.uuid).all()
        users_all = users.query.all()
        type = "Federalcurrency"
        for i in range(len(users_all)):
            try:
                to = users_all[i].uuid
                if users_all[i].alert1 is not None and "on" in literal_eval(users_all[i].alert1):
                    if users_all[i].federalcurrency1 is not None and SYMBOL in literal_eval(users_all[i].federalcurrency1):
                        if (users_all[i].candlestick1 is not None or users_all[i].category1 is not None) and (STATUS.split(':')[1].strip() in literal_eval(users_all[i].candlestick1) or STATUS.split(':')[0].strip().replace('Divergence','') in literal_eval(users_all[i].category1) or STATUS.split(':')[1].strip() in literal_eval(users_all[i].category1)):
                            if users_all[i].trend1 is not None and TREND in literal_eval(users_all[i].trend1):
                                if users_all[i].timeframe1 is not None and TIMEFRAME.replace('Minutes','').stirp() in literal_eval(users_all[i].timeframe1):
                                    flex_contents  =read_json(type,SYMBOL,RSI,CLOSE,STATUS,COLOR,TEXT,TREND,TIMEFRAME,TS,STO,literal_eval(users_all[i].label1)[0],literal_eval(users_all[i].color1)[0])
                                    flex_message = FlexSendMessage(alt_text=noti+' #'+literal_eval(users_all[i].label1)[0],contents=flex_contents)
                                    line_bot_api.push_message(
                                    to,
                                    flex_message
                                    )
                if users_all[i].alert2 is not None and  "on" in literal_eval(users_all[i].alert2):
                    if users_all[i].federalcurrency2 is not None and SYMBOL in literal_eval(users_all[i].federalcurrency2):
                        if (users_all[i].candlestick2 is not None or users_all[i].category2 is not None) and (STATUS.split(':')[1].strip() in literal_eval(users_all[i].candlestick2) or STATUS.split(':')[0].strip().replace('Divergence','') in literal_eval(users_all[i].category2) or STATUS.split(':')[1].strip() in literal_eval(users_all[i].category2)):
                            if users_all[i].trend2 is not None and TREND in literal_eval(users_all[i].trend2):
                                if users_all[i].timeframe2 is not None and TIMEFRAME.replace('Minutes','').strip() in literal_eval(users_all[i].timeframe2):
                                    flex_contents  =read_json(type,SYMBOL,RSI,CLOSE,STATUS,COLOR,TEXT,TREND,TIMEFRAME,TS,STO,literal_eval(users_all[i].label2)[0],literal_eval(users_all[i].color2)[0])
                                    flex_message = FlexSendMessage(alt_text=noti+' #'+literal_eval(users_all[i].label2)[0],contents=flex_contents)
                                    line_bot_api.push_message(
                                    to,
                                    flex_message
                                    )
                if users_all[i].alert3 is not None and "on" in literal_eval(users_all[i].alert3):
                    if users_all[i].federalcurrency3 is not None and SYMBOL in literal_eval(users_all[i].federalcurrency3):
                        if (users_all[i].candlestick3 is not None or users_all[i].category3 is not None) and (STATUS.split(':')[1].strip() in literal_eval(users_all[i].candlestick3) or STATUS.split(':')[0].strip().replace('Divergence','') in literal_eval(users_all[i].category3) or STATUS.split(':')[1].strip() in literal_eval(users_all[i].category3)):
                            if users_all[i].trend3 is not None and TREND in literal_eval(users_all[i].trend3):
                                if users_all[i].timeframe3 is not None and TIMEFRAME.replace('Minutes','').strip() in literal_eval(users_all[i].timeframe3):
                                    flex_contents  =read_json(type,SYMBOL,RSI,CLOSE,STATUS,COLOR,TEXT,TREND,TIMEFRAME,TS,STO,literal_eval(users_all[i].label3)[0],literal_eval(users_all[i].color3)[0])
                                    flex_message = FlexSendMessage(alt_text=noti+' #'+literal_eval(users_all[i].label3)[0],contents=flex_contents)
                                    line_bot_api.push_message(
                                    to,
                                    flex_message
                                    )
            except Exception as e:
                print(e)
                pass
        return { "message": "done" }, 201

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html')


def RSI(arr: pd.Series, n: int):
    """Relative strength index"""
    gain = pd.Series(arr).diff()
    loss = gain.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    rs = gain.ewm(n).mean() / loss.abs().ewm(n).mean()
    return 100 - 100 / (1 + rs)


def DIVERGENCE_POINT(arr,datetime_arr):
    
    #RSI Divegence
    timestamp = datetime_arr.timestamp()
    for i in range(len(arr)):
        timestamp_alert = (arr[i].ts).timestamp()
        #10 min is 600

        if (timestamp_alert-600) <= timestamp and timestamp <= (timestamp_alert+000):
            return arr[i].Status
    return ''


def BREAKOUT_POINT(arr,datetime_arr):
    
    #RSI Divegence
    timestamp = datetime_arr.timestamp()
    for i in range(len(arr)):
        timestamp_alert = (arr[i].ts).timestamp()
        #10 min is 600

        if (timestamp_alert-600) <= timestamp and timestamp <= (timestamp_alert+000):
            return arr[i].Status
    return ''



class Divergence(Strategy):
    d_rsi = 30  # Daily RSI lookback periods
    w_rsi = 30  # Weekly
    level = 70
    query = ''
    tp = 20
    sl = 30
    size = 0.75
    def init(self):
        self.daily_rsi = self.I(RSI, self.data.Close, self.d_rsi,name=" RSI วัน")
        self.weekly_rsi = self.I(RSI, self.data.Close, self.w_rsi,name=" RSI อาทิตย์")
        


    def next(self):
        Price = self.data.Close[-1]
        Datetime = self.data.index[-1]
        result = DIVERGENCE_POINT(self.query , Datetime)
        result_break = BREAKOUT_POINT(self.query , Datetime)

        if (not self.position and
            self.daily_rsi[-1] > self.level and
            self.weekly_rsi[-1] > self.level and
            self.weekly_rsi[-1] > self.daily_rsi[-1]):
            
            takeprofit = (self.tp/100)*Price
            takeprofit = Price + takeprofit

            stoploss = (self.sl/100)*Price
            stoploss = Price - stoploss

            self.buy(tp=takeprofit,sl=stoploss,size=self.size)

        if "Bullish" in result:
            takeprofit = (self.tp/100)*Price
            takeprofit = Price + takeprofit

            stoploss = (self.sl/100)*Price
            stoploss = Price - stoploss

            self.buy(tp=takeprofit,sl=stoploss,size=self.size)
        elif "Bearish" in result:
            takeprofit = (self.tp/100)*Price
            takeprofit = Price - takeprofit

            stoploss = (self.sl/100)*Price
            stoploss = Price + stoploss

            self.sell(tp=takeprofit,sl=stoploss,size=self.size)

        
        if "Resistance" in result_break:
            takeprofit = (self.tp/100)*Price
            takeprofit = Price + takeprofit

            stoploss = (self.sl/100)*Price
            stoploss = Price - stoploss

            self.buy(tp=takeprofit,sl=stoploss,size=self.size)
        elif "Support" in result_break:
            takeprofit = (self.tp/100)*Price
            takeprofit = Price - takeprofit

            stoploss = (self.sl/100)*Price
            stoploss = Price + stoploss

            self.sell(tp=takeprofit,sl=stoploss,size=self.size)


class Breakout(Strategy):
    d_rsi = 30
    query = ''
    tp = 20
    sl = 30
    size = 0.1
    def init(self):
        self.daily_rsi = self.I(RSI, self.data.Close, self.d_rsi)
        


    def next(self):
        Price = self.data.Close[-1]
        Datetime = self.data.index[-1]
        if DIVERGENCE_POINT(self.query , Datetime):
            takeprofit = (self.tp/100)*Price
            takeprofit = Price + takeprofit

            stoploss = (self.sl/100)*Price
            stoploss = Price - stoploss

            self.buy(tp=takeprofit,sl=stoploss)

def isPivot(candle, window,df):
    """
    function that detects if a candle is a pivot/fractal point
    args: candle index, window before and after candle to test if pivot
    returns: 1 if pivot high, 2 if pivot low, 3 if both and 0 default
    """
    if candle-window < 0 or candle+window >= len(df):
        return 0
    
    pivotHigh = 1
    pivotLow = 2
    for i in range(candle-window, candle+window+1):
        if df.iloc[candle].Low > df.iloc[i].Low:
            pivotLow=0
        if df.iloc[candle].High < df.iloc[i].High:
            pivotHigh=0
    if (pivotHigh and pivotLow):
        return 3
    elif pivotHigh:
        return pivotHigh
    elif pivotLow:
        return pivotLow
    else:
        return 0


def collect_channel(candle, backcandles, window,df):
    localdf = df[candle-backcandles-window:candle-window]
    #localdf['isPivot'] = localdf.apply(lambda x: isPivot(x.name,window), axis=1)
    highs = localdf[localdf['isPivot']==1].High.values
    idxhighs = localdf[localdf['isPivot']==1].High.index
    lows = localdf[localdf['isPivot']==2].Low.values
    idxlows = localdf[localdf['isPivot']==2].Low.index
    
    if len(lows)>=3 and len(highs)>=3:
        sl_lows, interc_lows, r_value_l, _, _ = stats.linregress(idxlows,lows)
        sl_highs, interc_highs, r_value_h, _, _ = stats.linregress(idxhighs,highs)
    
        return(sl_lows, interc_lows, sl_highs, interc_highs, r_value_l**2, r_value_h**2)
    else:
        return(0,0,0,0,0,0)
    

def isBreakOut(candle, backcandles, window,df):
    if (candle-backcandles-window)<0:
        return 0
    
    sl_lows, interc_lows, sl_highs, interc_highs, r_sq_l, r_sq_h = df.iloc[candle].Channel
    
    prev_idx = candle-1
    prev_high = df.iloc[candle-1].High
    prev_low = df.iloc[candle-1].Low
    prev_close = df.iloc[candle-1].Close
    
    curr_idx = candle
    curr_high = df.iloc[candle].High
    curr_low = df.iloc[candle].Low
    curr_close = df.iloc[candle].Close
    curr_open = df.iloc[candle].Open

    if ( prev_high > (sl_lows*prev_idx + interc_lows) and
        prev_close < (sl_lows*prev_idx + interc_lows) and
        curr_open < (sl_lows*curr_idx + interc_lows) and
        curr_close < (sl_lows*prev_idx + interc_lows)): #and r_sq_l > 0.9
        return 1
    
    elif ( prev_low < (sl_highs*prev_idx + interc_highs) and
        prev_close > (sl_highs*prev_idx + interc_highs) and
        curr_open > (sl_highs*curr_idx + interc_highs) and
        curr_close > (sl_highs*prev_idx + interc_highs)): #and r_sq_h > 0.9
        return 2
    
    else:
        return 0
    
def SIGNAL(df):
    return df.isBreakOut


class BreakOut(Strategy):
    d_rsi = 30
    initsize = 0.1
    mysize = initsize
    def init(self):
        super().init()
        self.signal1 = self.I(SIGNAL,self.data)
        self.daily_rsi = self.I(RSI, self.data.Close, self.d_rsi,name="RSI")

    def next(self):
        super().next()
        TPSLRatio = 1.2

        if self.signal1==2 and len(self.trades)==0:   
            sl1 = self.data.Low[-2]
            tp1 = self.data.Close[-1] + abs(self.data.Close[-1]-sl1)*TPSLRatio
            #tp2 = self.data.Close[-1] + abs(self.data.Close[-1]-sl1)*TPSLRatio/3
            self.buy(sl=sl1, tp=tp1, size=self.mysize)
            #self.buy(sl=sl1, tp=tp2, size=self.mysize)
        
        elif self.signal1==1 and len(self.trades)==0:         
            sl1 = self.data.High[-2]
            tp1 = self.data.Close[-1] - abs(sl1-self.data.Close[-1])*TPSLRatio
            #tp2 = self.data.Close[-1] - abs(sl1-self.data.Close[-1])*TPSLRatio/3
            self.sell(sl=sl1, tp=tp1, size=self.mysize)
            #self.sell(sl=sl1, tp=tp2, size=self.mysize)

@app.route('/backtest', methods=['GET','POST'])
def backtest():
    try:
        if session["isLoggedIn"] == 'true':

            crypto = alert.query.with_entities(alert.Symbol).group_by(alert.Symbol).all()

            if request.method == "GET":
                uuid = 'U6432e9e99f722746d67b3cc1e5abbc14'
                return render_template('backtest.html',crypto=crypto,uuid=uuid,stats='')
            
            if request.method == "POST":
                uuid = 'U6432e9e99f722746d67b3cc1e5abbc14'
                symbol = request.form['symbol']
                commissions = float(request.form['commission'])
                tp = float(request.form['takeprofit'])
                sl = float(request.form['stoploss'])
                cashs = float(request.form['cash'])

                timeframe = request.form['timeframe']
                periods = request.form['periods']
                
                raw_symbol = symbol
                symbol = symbol.split('USD')[0]

                symbol = symbol+'-USD'



                
                data = yf.download(tickers=symbol, period = periods, interval = timeframe)
                data.reset_index(inplace = True, drop = True)


                window=3
                data['isPivot'] = data.apply(lambda x: isPivot((x.name),window, data), axis=1)
                
                backcandles = 45
                data['Channel'] = [collect_channel(candle, backcandles, window, data) for candle in data.index]


                data["isBreakOut"] = [isBreakOut(candle, backcandles, window, data) for candle in data.index]



                #Bearish_Divergence = "Bearish Divergence"
                #Bearish_Divergence = "%{}%".format(Bearish_Divergence)
                #Bullish_Divergence = "Bullish Divergence"
                #Bullish_Divergence = "%{}%".format(Bullish_Divergence)
                #category = [Bullish_Divergence,Bearish_Divergence]
                #category = [alert.Status.like(elem) for elem in category]
                #
                #timeframe_filter = str(timeframe.replace('m','').replace('hr',''))
                #timeframe_filter = "%{}%".format(str(timeframe_filter))
                #timeframe_filter = [timeframe_filter]
                #timeframe_filter = [alert.Timeframe.like(elem) for elem in timeframe_filter]
                #query = alert.query.filter(and_(alert.Symbol.like(raw_symbol),or_(*category),or_(*timeframe_filter))).order_by(alert.id.desc()).all() 
                #Divergence.query = query
                #Divergence.tp = tp
                #Divergence.sl = sl
                #bt = Backtest(data, Divergence,cash=cashs, commission=(commissions/100),exclusive_orders=True)
                bt = Backtest(data, BreakOut, cash=cashs, margin=1/50, commission=(commissions/100))
            
                

                stats = bt.run()
                bt.plot(open_browser=False,filename=os.path.join(app.root_path, 'templates/'+uuid+'.html'))


                with open(os.path.join(app.root_path, 'templates/'+uuid+'.html'), 'r') as file:
                    text_file = file.read().replace('{%c}', "{'%c'}")
                with open(os.path.join(app.root_path, 'templates/'+uuid+'.html'),"w") as file: 
                    file.writelines(text_file)
                    file.close()


                return render_template('backtest.html',tp=tp,sl=sl,cashs=cashs,timeframe=timeframe,periods=periods,crypto=crypto,uuid=uuid,stats=stats,symbol=raw_symbol,commissions=commissions)
        else:
            exp_alert='เซสชั่นหมดอายุ'
            return render_template('index.html',exp_alert=exp_alert)
    except Exception as e:
        exp_alert='ไม่มีข้อมูล'
        return render_template('index.html',exp_alert=exp_alert)

if __name__ == '__main__':
    app.run(host='0.0.0.0',threaded=True,debug=False) 
