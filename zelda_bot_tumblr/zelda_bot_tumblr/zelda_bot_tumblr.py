
import pytumblr
import deviantart
import urllib.request

#creating a client

#You'll need to add your tumblr api keys here
client = pytumblr.TumblrRestClient(
  '',
  '',
  '',
  ''
)

#deviantart api keys go here
da = deviantart.Api("", "")

has_more = True #boolean

#Add your tags here
_tags = ["Follow for more", "Zelda", "loz", "tloz", "nintendo", "art", "deviantart", "fanart", "video", "games", "legend of zelda", "The", "Legend", "of", "Zelda", "Series" , "botw", "zelda fan art", "link", "cute"]
_queued_urls = []
_posted_urls = []

#initializing some variables
skip = 0
mature = 0
not_enough_favorites = 0
personal = 0
nonetype = 0
already_queued = 0
already_posted = 0

_offset = 0

pages = 0

#SET THESE BEFORE YOU RUN! Uhm, i'm not sure how to grab the amount of posts already submitted to tumblr, or the amount already in queue...
#(Actually you might not have to set these)
POSTS_MADE = 3
AMOUNT_IN_QUEUE = 7
que_d = 0

#Grabs Queue Urls (Actually I think this part of the script checks for duplicates and ensures no double posts!)
while(que_d < AMOUNT_IN_QUEUE): 
    #Add you're tumblr username here
    queue_data = client.queue('hylian-obsessed', offset = que_d)

    for post in queue_data['posts']:
        _queued_urls.append(post['summary'])

    que_d += 20

print("Queued Urls Grabbed...")
#Grabs Posted Urls (for links
##Add your tumblr username here
posted_data = client.posts("hylian-obsessed", limit = POSTS_MADE)
for post in posted_data['posts']:
    if (post['type'] != "photo"): #skips none photo posts
        continue
    _posted_urls.append(post['summary'])

print("Posted urls grabbed")

while(has_more):
    pages += 1
    #The post parameters (popular, post tag type, time range)
    data = da.browse(endpoint='popular', q="zelda", timerange='1month', offset = _offset)
    has_more = data['has_more']

    if(has_more == False):
        has_more = False
        break

    _offset = data['next_offset']

    for deviation in data['results']:
        if(deviation.category == "Personal"):
            skip += 1
            personal += 1
            continue
        #ensures quality posts
        if(deviation.stats['favourites'] < 200):
            skip += 1
            not_enough_favorites += 1
            continue
        #no mature posts
        if(deviation.is_mature):
            skip += 1
            mature += 1
            continue;
        #no posts that aren't art
        if(deviation.preview == None):
            skip += 1
            nonetype += 1
            print("NONE TYPE FOUND")
            continue

        #Bools
        queued = False
        posted = False

        #Adding artist name and source to tumblr post!
        _summary = deviation.author.username +": " + "\'"+ deviation.title + "\'\n\n Source " + deviation.url

        #no duplicated urls!
        for url in _queued_urls:
            if(url[1:40] == _summary[1:40]):
                already_queued += 1
                skip += 1
                queued = True
                break

        if(queued):
            continue

        print("Queue check finished... checking posts")
        for url in _posted_urls:
            if(url[1:40] == _summary[1:40]):
                already_posted += 1
                skip += 1
                posted = True
                break

        if(posted):
            continue

        #All parameters passed... creating link
        _url = deviation.url
        _preview_pic = deviation.preview['src']
        _title = deviation.title
        _category = deviation.category

        _artist_image = (
        "<figure class='tmblr-full'data-orig-height='50' data-orig-width='50'>"+"<img style='width: 50px; height: 50px; display: inline;' src="+deviation.author.usericon+"data-orig-height='50' data-orig-width='50'></figure>")
        _description = (_artist_image + " <h1 align='center'>" + deviation.author.username +": " + "\'"+ deviation.title + "\'" + "</h1>\n\n <p style = 'size: 2em; font-family: monospace;'>Source " + deviation.url)


        print(deviation.stats['favourites'])
        print(_url)
        print(_preview_pic)
        print(_title)
        print(_description)

        #download url
        ##urllib.request.urlretrieve(_preview_pic, "zelda_image.jpg")
 
        _tags.append(deviation.category)
        _tags.append(_title)

        ##client.create_link("zelda-posts-hourly", state = "queue", title = _title, tags = _tags, thumbnail = _preview_pic, url = _url, description = _description)
        client.create_photo("hylias-den", slug = _url, format = "html", state = "queue", tags = _tags, caption = _description, source = _preview_pic)

        _queued_urls.append(_summary)#adding summary to queued urls...

        print("-----")

print("Total skipped: " + str(skip))
print("Mature: " + str(mature))
print("Less than 30 favorites: " + str(not_enough_favorites))
print("Personal journal: " + str(personal))
print("No preview: " + str(nonetype))
print("Already Queued: " + str(already_queued))
print("Already Posted: " +str(already_posted))
print("Total Num skipped: " + str(skip))

print("Total grabbed: " + str(_offset))
print("Total queued: " + str(_offset - skip))


## THIS IS THE OLD PART OF THE SCRIPT ---------------- I'm too scared to delete it...

#moredata = da.browse_morelikethis_preview(data['results'])
#data = client.tagged("Breath of the wild", limit = 50)

#REBLOG EXAMPLE#
#id = data[0]['id']
#reblog_key = data[0]['reblog_key']
#print(client.reblog("zelda-memes-hourly", id = id, reblog_key = reblog_key))


#for post in data:
#    if(post["type"] == "photo"):
#        for tags in post['tags']:
#            if (tags == "art" or tags == "fanart" or tags == "artist" or tags == "sketch"):
#                #id = post['id']
#                #reblog_key = post['reblog_key']
#                url = post['post_url']
#                print(url)
#                client.create_link("zelda-memes-hourly", title = url, state = "queue")
#                print("Post was queued...")
#    else:
#        print("not photo")

