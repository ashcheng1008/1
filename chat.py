if lineMessage[0:3]==“看醫生”:
  address=“”
  lineMes=lineMessage
  if lineMes[4:-1]==“”:
    address="桃園市"
  else:
    address=lineMes[4:-1]
    addurl=‘https://maps.googleapis.com/maps/api/getcode/json?key={}&address={}&sensor=false’.format(AIzaSyBKhoq1t6NEHtpbq2ANkrqa8ClnBCzbiWs,address)
    addressReq=requests.get(addurl)
    addressDoc=addressReq.json()
    lat=addreeDoc[‘results’][0][‘geometry’][‘location’][‘lat’]
    lng=addreeDoc[‘results’][0][‘geometry’][‘location’][‘lng’]

medsearch=‘https://maps.googleapis.com/maps/api/getcode/json?key={}&address={}&sensor=false’.format(AIzaSyBKhoq1t6NEHtpbq2ANkrqa8ClnBCzbiWs,lat,lng)
medReq=requests.get(medsearch)
nearby_clinic_dict=medReq.json()
top20_restaurants=nearby_clinic_dict[“results”]
cli_num=(len(top_clinic))

clinic=random.choice(top_client)
if clinic.get(“photos”) is None:
  thumbnail_image)url=None
else:
  photo_reference=clinic[“photos”][0][“photo_reference”]
  Photo_width=clinic[“photos”][0][“width”]
  thumbnail_image_url=“https://maps.googleapis.com/maps/api/place/photo?key={}&photoreference={}&maxwidth={}”.format(AIzaSyBKhoq1t6NEHtpbq2ANkrqa8ClnBCzbiWs,photo_reference,photo_width)

address=“沒有資料” if clinic.get(“vicinity”) is None else clinic[“vicinity”]
map_url=“https://www.google.com/maps/search/?api=1&query={lat},{long}&query_place_id={place_id}={place_id}”.format(lat=clinic[“geometry”][“location”][“lat”],long=clinic[“geometry”][“location”][“lng”],place_id=clinic[“place_id”])

buttons_template=TemplateSendMessage(
alt_text=clinic[“name”],
template=ButtonsTemplate(
  thumbnail_image_url=thumbnail_image_url,
  title=restaurant[“name”],
  text=details,
  actions=[
    URITemplateAction(
      label=‘查看地圖’,
      uri=map_url
    ),
  ]
)
)
line_bot_api.reply_message(event.reply_token,buttons_template)
Return 0