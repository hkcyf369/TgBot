import os
import telebot
import yfinance as yf
import urllib.request
import json



my_secret = os.environ['API_KEY']
bot = telebot.TeleBot(my_secret)




def busStop_request(message):
  request = message.text.split('-')
  if len(request) < 2 or request[0].lower() not in "bus":
    return False
  else:
    return True 

@bot.message_handler(func=busStop_request)
def busStop_response(message):
  request = message.text.split('-')[1]
  stopIDs = ""
  


def bus_request(message):
  request = message.text.split('-')
  if len(request) < 2 or request[0].lower() not in "bus":
    return False
  else:
    return True
 
@bot.message_handler(func=bus_request)
def bus_response(message):
  request = message.text.split('-')[1]
  url = "http://data.etabus.gov.hk/v1/transport/kmb/route/"
  data = urllib.request.urlopen(url).read().decode()
  data = json.loads(data)
  data = data["data"]
  resString = ''
  #print(type(data))
  
  hasdata = [r for r in data if r["route"]==request]
  print(type(hasdata))
  print(hasdata)
  if(hasdata):
      for i in hasdata:
        busRoute = i["route"]
        orig = i["orig_tc"]
        dest = i["dest_tc"]
      resString += "路線"+busRoute+"\n頭站: "+orig +"\n尾站: "+dest
      bot.send_message(message.chat.id, resString)
  else:
    bot.send_message(message.chat.id, "搵唔到依條巴士線啵")

 
      


  

     

  






@bot.message_handler(commands=['use'])
def greet(message):
  bot.reply_to(message, "Hello，幫緊你幫緊你\n搵美股可用`price-股票代號` 搵")


def stock_request(message):
  request = message.text.split('-')
  if len(request) < 2 or request[0].lower() not in "price":
    return False
  else:
    return True

@bot.message_handler(func=stock_request)
def send_price(message):
  request = message.text.split('-')[1]
  data = yf.download(tickers=request, period='5m', interval='1m')
  if data.size > 0:
    data = data.reset_index()
    data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
    print(data)
    data.set_index('format_date', inplace=True)
    print(data.to_string())
    bot.send_message(message.chat.id,request+"股票報價:\n"+ data['Close'].to_string(header=False))
  else:
    bot.send_message(message.chat.id, "Sor,搵唔到依隻股票")

bot.polling()