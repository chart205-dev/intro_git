from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

import json
with open('secret.json') as f:
    secret = json.load(f)
KEY = secret["KEY"]
ENDPOINT = secret["ENDPOINT"]

computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def get_tags(filepath):
  local_image = open(filepath, "rb")

  tags_result = computervision_client.tag_image_in_stream(local_image)

  tags = tags_result.tags
  tags_name = []
  for tag in tags:
      tags_name.append(tag.name)

  return tags_name

def detect_objects(filepath):
  local_image = open(filepath, "rb")

  detect_objects_results = computervision_client.detect_objects_in_stream(local_image)
  objects = detect_objects_results.objects

  return objects

import streamlit as st
from PIL import ImageDraw
from PIL import ImageFont

st.title("物体検出アプリ")

uploaded_file = st.file_uploader("画像をアップロード", type=["jpg","jpeg","png"])#, accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
if uploaded_file is not None:
   img = Image.open(uploaded_file)

   img = Image.open(uploaded_file)
   img_path = f'img/{uploaded_file.name}'
   img.save(img_path)
   
   objects = detect_objects(img_path)

   # 描画

   draw = ImageDraw.Draw(img)

   for obj in objects:
    x = obj.rectangle.x
    y = obj.rectangle.y
    w = obj.rectangle.w
    h = obj.rectangle.h
    caption = obj.object_property

    font = ImageFont.truetype(font="./OpenSans-Italic.ttf", size=50)

    # テキストサイズを取得（幅・高さ）
    bbox = draw.textbbox((0, 0), caption, font=font)  # 基準位置はダミー
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # 物体検出の枠
    draw.rectangle([(x, y), (x+w, y+h)], outline="green", width=5)
    
    #余白の計算
    dif_y = y - bbox[1]

    # テキスト背景（枠の左上に揃える）
    draw.rectangle([(x, y), (x+text_w, y+text_h)], fill="green")

    # テキストを描画（左上を枠に合わせる）
    draw.text((x, dif_y), caption, fill="white", font=font)

   st.image(img)

   tags_name = get_tags(img_path)
   tags_name = ', '.join(tags_name)

   st.markdown('**認識されたコンテンツタグ**')
   st.markdown(f'> {tags_name}')