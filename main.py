# Import necessary libraries
import time
import requests
import logging
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import psycopg2
from sklearn.metrics import accuracy_score, f1_score  # Placeholder; you'd use these in your validation

# Initialize logging to keep track of the process, errors, and exceptions
logging.basicConfig(filename='app.log', level=logging.INFO)

# Initialize the MultiLingual BERT Model for Sequence Classification
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-uncased")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-multilingual-uncased", num_labels=2)

# Define a function to classify comments as either normal or toxic
def classify_comment(comment):
    # Tokenize the comment
    inputs = tokenizer(comment, return_tensors="pt", padding=True, truncation=True, max_length=512)
    # Pass tokens through the model
    outputs = model(**inputs)
    # Calculate probabilities using softmax
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    # Return the class label with the highest probability
    return torch.argmax(probs).item()

# Connect to PostgreSQL
# You can change this according to database you created.
try:
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="BaranOpamp1.",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
except Exception as e:
    logging.error(f"Failed to connect to database: {e}")

# Define a function to batch insert data into PostgreSQL
def batch_store_in_db(data):
    try:
        insert_query = '''INSERT INTO comments (comment, label) VALUES (%s, %s);'''
        cursor.executemany(insert_query, data)
        conn.commit()
    except Exception as e:
        logging.error(f"Failed to insert into database: {e}")

# Define constants for YouTube API
# API key must be there
API_KEY = "AIzaSyCWkaul6AWgNBT5v5Zd2VYVp_HU3LcrQqo"

BASE_URL = "https://www.googleapis.com/youtube/v3/search"
BASE_CHAT_URL = "https://www.googleapis.com/youtube/v3/liveChat/messages"
VIDEO_DETAILS_URL = "https://www.googleapis.com/youtube/v3/videos"

params = {
    'key': API_KEY,
    'type': 'video',
    'part': 'id',
    'eventType': 'live',
    'maxResults': 10
}

batch_data = []
# Fetch live videos using YouTube API
try:
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    videos = response.json()
except requests.RequestException as e:
    logging.error(f"API request failed: {e}")
# Extract video IDs
video_ids = [item['id']['videoId'] for item in videos['items']]

# Loop through videos to get comments
for video_id in video_ids:
    params = {
        'key': API_KEY,
        'part': 'snippet,liveStreamingDetails',
        'id': video_id
    }

    try:
        response = requests.get(VIDEO_DETAILS_URL, params=params)
        response.raise_for_status()
        video_data = response.json()
    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")
# Check if the video has live streaming details
    if 'items' in video_data and video_data['items'] and 'liveStreamingDetails' in video_data['items'][0]:
        live_chat_id = video_data['items'][0]['liveStreamingDetails'].get('activeLiveChatId', None)
        # If a live chat is active, fetch comments
        if live_chat_id:
            chat_params = {
                'key': API_KEY,
                'part': 'snippet',
                'liveChatId': live_chat_id,
                'maxResults': 50
            }

            try:
                chat_response = requests.get(BASE_CHAT_URL, params=chat_params)
                chat_response.raise_for_status()
                chat_data = chat_response.json()
            except requests.RequestException as e:
                logging.error(f"API request failed: {e}")
            # Loop through comments and classify them
            for item in chat_data.get('items', []):
                comment = item['snippet']['displayMessage']
                label = classify_comment(comment)
                batch_data.append((comment, label))
    # Batch insert comments and their labels into PostgreSQL        
    batch_store_in_db(batch_data)
    # Sleep to respect the API rate limit
    time.sleep(1)  # Respect the API rate limit

# Close the database connection
cursor.close()
conn.close()
