#importing keys 
import tweepy as twitter
import keys
import time, datetime
from pytz import timezone
from datetime import date
import os
import requests
import shutil
import googlesearch


#TWITTER AUTHORIZATION AND TOKENS
auth = twitter.OAuthHandler(keys.API_KEY, keys.API_SECRET_KEY)
auth.set_access_token(keys.ACCESS_TOKEN, keys.SECRET_ACCESS_TOKEN)
api = twitter.API(auth)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='/home/runner/searchthisimage/google.json'

#CREATING FOLDER IN MACHINE
HOME_FOLDER = os. getcwd()
print(HOME_FOLDER)
# HOME_FOLDER = '/home/SelvaPrakash/searchthisimage'
TWEETS_UPLOADED_FOLDER = HOME_FOLDER+ '/infiles/'
GDOC_BEARER_TOKEN = keys.GDOC_BEARER_TOKEN
print(TWEETS_UPLOADED_FOLDER)

# GET /2/users/by/username/:username
headers = {"Authorization": "Bearer {}".format(GDOC_BEARER_TOKEN)}

def retrieve_last_mentioned_tweet_id():
    os.chdir(TWEETS_UPLOADED_FOLDER)
    f_read = open('last_mentioned_tweet_id.py', 'r')
    last_mentioned_tweet_id = int(f_read.read().strip())
    f_read.close()
    print(last_mentioned_tweet_id)
    return last_mentioned_tweet_id

def save_last_mention_tweet_id(id):
    os.chdir(HOME_FOLDER+'/infiles/')
    with open('last_mentioned_tweet_id.py','w') as file:
        file.write(str(id))
        print ('file written')

      #REQUESTS

def get_id(last_mentioned_tweet_id):
    r = requests.request("GET",'https://api.twitter.com/2/users/by/username/TWITTER',headers=headers)
    myid = r.json()['data']['id']
    print(myid)
   
     
    params =  {
    'expansions' : 'referenced_tweets.id,author_id',
    'since_id': last_mentioned_tweet_id,
    'user.fields': 'username'
     }

     # REQUESTSTO GET NEW_ID

    r_men = requests.request("GET",'https://api.twitter.com/2/users/4449919873/mentions',headers=headers,params = params)
    print ('r_men',r_men.json())
    new_id = (r_men.json()['meta']['newest_id'])
    print('newest_id=',new_id)
    
# def use_name(username): 
  
    username = (r_men.json()['includes']['users'][0]['username'])
    print('USERNAME=',username)
   
   

    #GET THE PREVIOUS TWEET  

    prev_tweet =(r_men.json()['data'][0]['referenced_tweets'][0]['id'])
    print('replied to=',prev_tweet)

    # REQUEST TO GET THE ORIGINAL TWEET

    orig_tweet_url = "https://api.twitter.com/2/tweets/{}?expansions=attachments.media_keys&media.fields=url".format(prev_tweet)
    r_tweet = requests.request("GET",orig_tweet_url,headers=headers)
    # tweet=requests.get(orig_tweet_url)
    print('r_tweet=',r_tweet.json())
    
# def image(image_url,username) :
  #  TO GET THE IMG_URL

    img_url = (r_tweet.json()['includes']['media'][0]['url']) 
    print('IMAGE',img_url,username,new_id)
    return img_url,username,new_id

    #ANNOTATIONS BY GOOGLE
    
    
def googleurl(img_url):

    nsfw = googlesearch.detect_safe_search_uri(img_url)
    if nsfw == 'VERY_LIKELY':
      return 'No Result Found'

    annotations = (googlesearch.annotate(img_url))

    print ((annotations.pages_with_matching_images))
    save_google_url_all(img_url,annotations.pages_with_matching_images)
    # for page in annotations.pages_with_matching_images:
      
    #  print(' Searched Url   : {}'.format(page.url))

    result_len = len((annotations.pages_with_matching_images))
    print (result_len)
    if result_len==0:
      print ('No Result Found')
      return "No Result Found"

    else:
      google_url="No Result Found" #annotations.pages_with_matching_images[0].url
      for i in range(0,result_len):
        if (annotations.pages_with_matching_images[i].url.find("twitter.com") >=0 or annotations.pages_with_matching_images[i].url.find("youtube.com") >=0 or annotations.pages_with_matching_images[i].url.find("gurushots") >=0  or     annotations.pages_with_matching_images[i].url.find("everything.explained.today") >=0  or          annotations.pages_with_matching_images[i].url.find("faqs.org") >=0 or        annotations.pages_with_matching_images[i].url.find("what-is") >=0 or        annotations.pages_with_matching_images[i].url.find("https://t.co") >=0 or    annotations.pages_with_matching_images[i].url.find("https://nitter.net") >=0 or    annotations.pages_with_matching_images[i].url.find("https://trendsmap.com" ) >=0 or
annotations.pages_with_matching_images[i].url.find("wiki" ) >=0
        ) :
          continue
        elif len(annotations.pages_with_matching_images[i].full_matching_images)==0 and len(annotations.pages_with_matching_images[i].partial_matching_images)==0:
          print("No Matching Images")
          continue
           
        else:
          print ('google_search_img_url  : {}',annotations.pages_with_matching_images[i].url)
          google_url=annotations.pages_with_matching_images[i].url
          print(google_url)
          break
  

      return google_url

def save_google_url(img_url,last_mentioned_tweet_id):
  os.chdir(HOME_FOLDER+'/save url/')
  with open('google_url','a') as file:
    now = datetime.datetime.now()
    
    # current_time = now.strftime("%H:%M:%S")
    print("now =", now)

    #dt_string = now.strftime("%d-/%m-/%Y %H:%M:%S %Z%z")
    now_asia = now.astimezone(timezone('Asia/Kolkata'))    
    new_asia=now_asia.strftime("%Y-%m-%d %H:%M:%S") 
    print(new_asia)

    file.write((new_asia) + ' - ' +str(last_mentioned_tweet_id) +' - '+   (img_url) + '\n')

    file.close()

    print('written url and id')


def save_google_url_all(img_url,all_matching_urls):
  os.chdir(HOME_FOLDER+'/save url/')
  with open('all_urls.txt','a') as file:
    now = datetime.datetime.now()
    
    # current_time = now.strftime("%H:%M:%S")
    print("now =", now)

    #dt_string = now.strftime("%d-/%m-/%Y %H:%M:%S %Z%z")
    now_asia = now.astimezone(timezone('Asia/Kolkata'))    
    new_asia=now_asia.strftime("%Y-%m-%d %H:%M:%S") 
    print(new_asia)

    file.write((new_asia) + ' - ' +str(img_url)  + '\n')
    file.write('\n' + str(all_matching_urls) +'\n'  )
    file.write('----------------------\n\n'  )
    file.close()




    print('written url and id')

      
def reply2tweet(searched_url,men_tweet_id,men_userid):

          api.update_status('@' + men_userid  +' '+
                            searched_url, (men_tweet_id))
          print('Replied')
    



if __name__ =='__main__': 

  while (True):
    
      last_mentioned_tweet_id = retrieve_last_mentioned_tweet_id()
      # last_mentioned_id = last_mentioned_tweet_id
      print ('in main',last_mentioned_tweet_id )

      # # SAVE THE LAST MENTION TWEET ID
      # save_last_mention_tweet_id (last_mentioned_tweet_id)
      try:
        img_url,men_userid,new_id=get_id(last_mentioned_tweet_id)
      except Exception as e:
        print (e)
        time.sleep(15)
        continue
    
      save_last_mention_tweet_id (new_id)

      # save_last_mention_tweet_id (new_id)
      if img_url:
        google_url=googleurl(img_url)

        save_google_url(google_url,last_mentioned_tweet_id)

        replied=reply2tweet(google_url,new_id,men_userid)

    