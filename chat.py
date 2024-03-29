import re
import configparser
import json
from bs4 import BeautifulSoup
import random
from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# 使用heroku的environment variables
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

# 預設地址
address = ''
# 你的API_KEY
GOOGLE_API_KEY = 'AIzaSyBKhoq1t6NEHtpbq2ANkrqa8ClnBCzbiWs'

if lineMessage[0:3]=='':
  address=''
  lineMes=lineMessage
  if  lineMes[4:-1]=='':
     address="台中市北區進化路587號"
  else:
    address=lineMes[4:-1]
  addurl = 'https://maps.googleapis.com/maps/api/geocode/json?key={}&address={}&sensor=false'.format(GOOGLE_API_KEY,address)

# 經緯度轉換
  addressReq = requests.get(addurl)
  addressDoc = addressReq.json()
  lat = addressDoc['results'][0]['geometry']['location']['lat']
  lng = addressDoc['results'][0]['geometry']['location']['lng']

# 取得店家資訊
foodStoreSearch = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={}&location={},{}&rankby=distance&type=restaurant&language=zh-TW".format(GOOGLE_API_KEY, lat, lng)

foodReq = requests.get(foodStoreSearch)
nearbyRestaurants_dict = foodReq.json()

top20Restaurants = nearbyRestaurants_dict["results"]
res_num = (len(top20Restaurants)) 
# 取評分高於3.9的店家
bravo=[]
for i in range(res_num):
  try:
    if top20Restaurants[i]['rating'] > 3.9:
      # print('rate: ', top20Restaurants[i]['rating'])
      bravo.append(i)
  except:
    KeyError
if len(bravo) < 0:
  print("沒東西可以吃")
  # restaurant = random.choice(top20Restaurants) 沒有的話隨便選一間

# 從高於3.9的店家隨機選一間
restaurant = top20Restaurants[random.choice(bravo)]

# 檢查餐廳有沒有照片
if restaurant.get("photos") is None:
  thumbnailImageUrl = None
else:
  # 取得照片
  photoReference = restaurant["photos"][0]["photo_reference"]
  photoWidth = restaurant["photos"][0]["width"]
  thumbnailImageUrl = "https://maps.googleapis.com/maps/api/place/photo?key={}&photoreference={}&maxwidth={}".format(GOOGLE_API_KEY, photoReference,photoWidth)
  
# 餐廳詳細資訊
rating = "無" if restaurant.get("rating") is None else restaurant["rating"]
address = "沒有資料" if restaurant.get("vicinity") is None else restaurant["vicinity"]
details = "Google Map評分：{}\n地址：{}".format(rating, address)
print(restaurant.get("name"))
print(details)

 # 取得餐廳的 Google map 網址
mapUrl = "https://www.google.com/maps/search/?api=1&query={lat},{long}&query_place_id={place_id}".format(lat=restaurant["geometry"]["location"]["lat"],long=restaurant["geometry"]["location"]["lng"],place_id=restaurant["place_id"])
#print(mapUrl)
buttons_template=TemplateSendMessage(
alt_text=restaurant["name"],
template=ButtonsTemplate(
  thumbnail_image_url=thumbnail_image_url,
  title=restaurant["name"],
  text=details,
  actions=[
    URITemplateAction(
      label='查看地圖',
      uri=map_url
    ),
  ]
)
)

line_bot_api.reply_message(event.reply_token,buttons_templates)

