from InstagramAPI import InstagramAPI
import json
from flask import Flask
from time import sleep
from markupsafe import escape

         
class User:
    def __init__(self,pk,username,private,photo_url,follow_count,following_count,following_tag,usertags_count,bio,category,phone_numbre,email):
       self.pk=pk
       self.username=username
       self.private=private
       self.photo_url=photo_url
       self.follow_count=follow_count
       self.following_count=following_count
       self.following_tag = following_tag
       self.usertags_count = usertags_count
       self.bio=bio
       self.category=category
       self.phone_numbre=phone_numbre
       self.email=email

    def getuserinfojson(self):
         if(self.pk != None):
             user = {
                 "id":self.pk,
                 "username":self.username,
                 "private":self.private,
                 "photo_url":self.photo_url,
                 "follow_count":self.follow_count,
                 "following_count":self.following_count,
                 "following_tags":self.following_tag,
                 "user_tags":self.usertags_count,
                 "bio":self.bio,
                 "category":self.category,
                 "phone_numbre":self.phone_numbre,
                 "email":self.email,
             }   
             
         return  json.dumps(user,indent=4)       


        

    def show_user(self):
        if(self.pk != None):
            print("ID : " + str(self.pk))
            print("Username : " + self.username)
            print("is Private ? : " + str(self.private))
            print("Photo url : " + self.photo_url)
            print("Follow Count : " + str(self.follow_count))
            print("Following Count : " + str(self.following_count))
            print("Following Tags : " + str(self.following_tag))
            print("User Tags Account  : " + str(self.usertags_count))
            print("Biography : " + self.bio)
            print("Category : " + self.category)
            print("Phone Numbre : " + self.phone_numbre)
            print("Adress Email : " + self.email)
        else:
            print("May Be You're Not Loggin")
       


class   InstagramBot:
    def __init__(self,username,password):
        
        self.username = username
        self.password = password
        try:
            self.api = InstagramAPI(username,password)
        except :
            print('Something went wrong ...')    
        
        


    def login(self):
        try:
            if(self.api.login()):
                return "200"
            else:
                return self.api.LastJson['message']
            
        except ValueError:
            print("Something went wrong ...")    
           
        
    def getlikersfrompost(self,post_id):
        self.api.getMediaLikers(post_id)
        return json.dumps(self.api.LastJson,indent=4)   




    def followuserfrompost(self,post_id):
        self.api.getSelfUsersFollowing()
        following_users = []
        users_list=[]
        result = self.api.LastJson
        for user in result['users']:
            following_users.append(user['pk'])
        self.api.getMediaLikers(post_id)
        result=self.api.LastJson
        for user in result['users']:  
            users_list.append({'pk':user['pk'],'username':user['username']})
        for user in users_list:
            if not user['pk']  in following_users:
                self.api.follow(user['pk'])
                print("follow @"+str(user['username']+" succesfuly "))
                sleep(20)
            else :
                 print("Already following @"+str(user['username']+" ! "))
                 sleep(10)
        return 'done !'

       
                 
    def follow(self,pk):
        self.api.getSelfUsersFollowing()
        following_users = []
        result = self.api.LastJson
        for user in result['users']:
            following_users.append(user['pk'])
        if not pk in following_users:
            self.api.follow(pk)
            return("following succesfuly ")
        else:
            return("Already following !")





    def unfollowall(self):

        following_users = []
        self.api.getSelfUsersFollowing()
        result = self.api.LastJson
        
        for user in result['users']:
            following_users.append({'pk':user['pk'],'username':user['username']})       #GET YOUR FOLLOWERS
        for user in following_users:
             print('Unfollowing @' + user['username'])
             self.api.unfollow(user['pk'])
             sleep(20)




    def unfollowpeople(self):
        follower_users = []
        following_users = []
        self.api.getSelfUserFollowers()
        result = self.api.LastJson
        
        for user in result['users']:
            follower_users.append({'pk':user['pk'],'username':user['username']})   #GET YOUR FOLLOWERS
        self.api.getSelfUsersFollowing()
        result = self.api.LastJson
        for user in result['users']:
            following_users.append({'pk':user['pk'],'username':user['username'],'is_private':user['is_private']})
        
        for user in following_users:
            if (not user['pk'] in follower_users and not user['is_private']):
                print('Unfollowing @' + user['username'])
                self.api.unfollow(user['pk'])
                sleep(20)
            else:
                 print(user['username']+' is following you !')
                 sleep(10)


       

       


    def getuserpost(self,user):
        self.api.getUserFeed(user.pk)
        result = self.api.LastJson
        list_post={}
        i=1
        for item in result['items']:
            list_img=[]
            if("carousel_media" in item ):
                for img in item['carousel_media']:
                    list_img.append(img['image_versions2']['candidates'][0]['url'])
            else:
                list_img.append(item['image_versions2']['candidates'][0]['url'])   
            post = {
                "taken_at":item['taken_at'],
                "pk":item['pk'],
                "id":item['id'],
                "code":item['code'],
                "likes_count":item['like_count'],
                "comments_count":item['comment_count'],
                "carousel":list_img,

            }
            list_post['post_'+str(i)]=post
            i=i+1         
        
        return json.dumps(list_post,indent=4)
        
       
        
       


    def userinfo(self):
        self.api.searchUsername(self.username)
        result = self.api.LastJson
        return User(result['user']['pk'],result['user']['username'],result['user']['is_private'],result['user']['profile_pic_url'],result['user']['follower_count'],result['user']['following_count'],result['user']['following_tag_count'],result['user']['usertags_count'],result['user']['biography'],result['user']['category'],result['user']['contact_phone_number'],result['user']['public_email']) 

      
            

        

app = Flask(__name__)

#LOGIN
@app.route('/login/<username>/<password>')
def login(username,password):
    auth = InstagramBot(username,password)
    auth.login()
    user = auth.userinfo()
    return user.getuserinfojson()

#GET POSTS OF THE CURRENT USER 
@app.route('/post/<username>/<password>')
def post(username,password):
    auth = InstagramBot(username,password)
    auth.login()
    user = auth.userinfo()
    return auth.getuserpost(user)

#FOLLOW USERS FROM POST
@app.route('/followuserfrompost/<username>/<password>/<post_id>')
def followuserfrompost(username,password,post_id):
    auth = InstagramBot(username,password)
    auth.login()
    return auth.followuserfrompost(post_id)

#GET USERS LIKERS FROM POST
@app.route('/getlikersfrompost/<username>/<password>/<post_id>')
def getlikersfrompost(username,password,post_id):
    auth = InstagramBot(username,password)
    auth.login()
    return auth.getlikersfrompost(post_id)

#FOLLOW USER 
@app.route('/follow/<username>/<password>/<int:pk>')
def follow(username,password,pk):
    auth = InstagramBot(username,password)
    auth.login()
    return auth.follow(pk)  

#UNFOLLOW ALL USER WHO FOLLOW YOU
@app.route('/unfollowall/<username>/<password>')
def unfollowall(username,password):
    auth = InstagramBot(username,password)
    auth.login()
    return auth.unfollowall() 

#UNFOLLOW USER WHO DON'T FOLLOW YOU
@app.route('/unfollowpeople/<username>/<password>')
def unfollowpeople(username,password):
    auth = InstagramBot(username,password)
    auth.login()
    return auth.unfollowpeople() 
if __name__ == "__main__":
    app.run(debug=True)









































# username = "zineddine_haddad"
# passworrd = "0698918467"
# api = InstagramAPI(username,passworrd)
# api.login()



# api.searchUsername(username)
# result = api.LastJson   #GET INFO ABOUT CURRENT USER
# username_id = result['user']['pk']

# user_posts = api.getUserFeed(username_id)  #GET USER FEED
# result = api.LastJson

# media_id = result['items'][0]['id']
# api.getMediaComments(media_id) # Get users who liked
# comments = api.LastJson['comments']




