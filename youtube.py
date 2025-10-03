from googleapiclient.discovery import build
import json

import pandas as pd
import streamlit as st

with open('secret.json') as f:
		secret = json.load(f)

DEVELOPER_KEY = secret["KEY"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

def video_search(youtube, q = '自動化', max_results=20):
		response = youtube.search().list(
				q=q,
				part="id,snippet",
				order = 'viewCount',
				type = 'video',
				maxResults=max_results
		).execute()

		items_id = []
		items = response['items']
		for item in items:
				item_id = {}
				item_id['video_id'] = item['id']['videoId']
				# print(item_id['video_id'])
				item_id['channel_id'] = item['snippet']['channelId']
				# print(item_id['channel_id'])
				items_id.append(item_id)
				
		df_video = pd.DataFrame(items_id)
		return df_video

def get_results(df_video, threshold=5000):
		channel_ids = df_video['channel_id'].unique().tolist()

		subscriber_list = youtube.channels().list(
			id = ','.join(channel_ids),	
			part="statistics",
			fields="items(id,statistics(subscriberCount))"
		).execute()

		subscriberes = []
		for item in subscriber_list['items']:
				subscribere = {}
				if len(item['statistics']) > 0:
						subscribere['channel_id'] = item['id']
						subscribere['subscriberCount'] = int(item['statistics']['subscriberCount'])
				else:
						subscribere['channel_id'] = item['id']
				subscriberes.append(subscribere)

		df_subscriber = pd.DataFrame(subscriberes)

		df = pd.merge(left=df_video, right=df_subscriber, on='channel_id')
		df_extracted = df[df['subscriberCount'] < threshold]

		video_id = df_extracted['video_id'].tolist()

		video_list = youtube.videos().list(
			id = ','.join(video_id),
			part='snippet,statistics',
			fields = 'items(id,snippet(title),statistics(viewCount))'
		).execute()

		videos_info = []
		items = video_list['items']
		for item in items:
			video_info = {}
			video_info['video_id'] = item['id']
			video_info['title'] = item['snippet']['title']
			video_info['viewCount'] = int(item['statistics']['viewCount'])
			videos_info.append(video_info)

		df_videos_info = pd.DataFrame(videos_info)

		results = pd.merge(left=df_extracted, right=df_videos_info, on='video_id')
		results = results.loc[:,['video_id','title','viewCount','subscriberCount','channel_id']]
		
		return results

st.title('Youtube分析アプリ')

st.sidebar.write('### クエリと閾値の設定')
st.sidebar.write('### クエリの入力')
query = st.sidebar.text_input('検索クエリを入力してください', 'python Excel')

st.sidebar.write('### 閾値の設定')
threshold = st.sidebar.slider('チャンネル登録者数の閾値を設定してください', 1000, 100000, 50000)

st.write('### 選択中のパラメータ')
st.markdown(f"""
						- 検索クエリ: {query}
						- チャンネル登録者数の閾値: {threshold}
""")

df_video = video_search(youtube, q=query, max_results=50)
results = get_results(df_video, threshold=100000)

st.write('### 分析結果', results)
st.write('### 動画再生')

video_id = st.text_input('動画IDを入力してください')
url = f'https://www.youtube.com/watch?v={video_id}'

video_filed = st.empty()
video_filed.write('こちらに動画が表示されます')

if st.button('ビデオ表示'):
	if len(video_id) > 0:
		try:
			video_filed.video(url)
		except:
			st.error('おっと、何かエラーが発生しました。動画IDを確認してください')