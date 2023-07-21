#to get a channel id, use this site: https://commentpicker.com/youtube-channel-id.php
#you will have to replace the API key with your own at https://developers.google.com/youtube/v3
#if you encounter any problems, join my discord: https://discord.gg/WW5PuDBySt
#i would recommend NOT using the synonyms


import requests
import html
import nltk
from nltk.corpus import wordnet
import random

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

def get_video_titles(api_key, channel_id, max_results=500): #change number of videos here
    try:
        base_url = "https://www.googleapis.com/youtube/v3/search"
        titles = []
        next_page_token = None

        while len(titles) < max_results:
            params = {
                "key": api_key,
                "part": "snippet",
                "channelId": channel_id,
                "maxResults": min(50, max_results - len(titles)),
                "pageToken": next_page_token,
            }

            response = requests.get(base_url, params=params)
            if response.status_code != 200:
                print("Failed to fetch video data from YouTube API.")
                break

            data = response.json()
            titles += [item["snippet"]["title"] for item in data["items"]]
            next_page_token = data.get("nextPageToken")

            if not next_page_token:
                break

        return titles
    except Exception as e:
        print("An error occurred:", e)
        return []

def rewrite_video_titles(titles):
    nltk.download("wordnet")
    rewritten_titles = []

    for title in titles:
        words = title.split()
        new_title = []
        for word in words:
            synonyms = get_synonyms(word)
            if synonyms:
                new_word = random.choice(synonyms)
            else:
                new_word = word
            new_title.append(new_word)
        rewritten_titles.append(" ".join(new_title))

    return rewritten_titles

def scrape_youtube_titles(channel_id):
    try:
        api_key = "PUT API HERE" #replace api key with youtube api key here https://developers.google.com/youtube/v3
        titles = get_video_titles(api_key, channel_id)

        print(f"Scraped {len(titles)} video titles.")

        rewrite_choice = input("Do you want to rewrite the video titles with synonyms? (not recommended) (y/n): ")
        if rewrite_choice.lower() == "y":
            rewritten_titles = rewrite_video_titles(titles)
            titles = rewritten_titles

        titles = [html.unescape(title) for title in titles]
        with open("video_titles.txt", "w", encoding="utf-8") as file:
            for title in titles:
                file.write(title + "\n")

        print(f"Successfully saved {'rewritten ' if rewrite_choice.lower() == 'y' else ''}{len(titles)} video titles to 'video_titles.txt'")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    youtube_channel_id = input("Enter the YouTube channel ID (e.g., UC1234567890): ")
    scrape_youtube_titles(youtube_channel_id)
