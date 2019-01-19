import json
from random import choice
from pprint import pprint

import requests

import requests
from bs4 import BeautifulSoup

# HTTP Header to trick the web server into thinking we are making a HTTP
# request from a normal browser.
_user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
]

class InstagramScraper:

    def __init__(self, user_agents=None, proxy=None):
        self.user_agents = user_agents
        self.proxy = proxy

    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(_user_agents)

    def __request_url(self, url):
        try:
            response = requests.get(url, headers={'User-Agent': self.__random_agent()}, proxies={'http': self.proxy,
                                                                                                 'https': self.proxy})
            response.raise_for_status()
        except requests.HTTPError:
            raise requests.HTTPError('Received non 200 status code from Instagram')
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response.text

    @staticmethod
    def extract_json_data(html):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)

    def profile_page_recent_posts(self, profile_url):
        results = []
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']["edges"]
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    results.append(node)
        return results

# Settings:

username = 'ceit_pucmm'
post_number = 0 # Last post made on Instagram.

instagram = InstagramScraper()
results = instagram.profile_page_recent_posts('https://www.instagram.com/' + username + '/?hl=en')

caption = results[post_number]["edge_media_to_caption"]["edges"][0]["node"]["text"]
image_url = results[post_number]["display_url"]

#Check if the post is a video.
if results[post_number]["is_video"] == 'True':
    is_video = True
else:
    is_video = False

# Request and download the image:
r = requests.get(image_url, allow_redirects=True)
open('last_instagram_post.jpg', 'wb').write(r.content)

# Save the last post caption in a .txt file:
open('last_post_caption.txt', 'w').write(caption)

#last_image_url = results[0]["thumbnail_resources"][4]["src"]
