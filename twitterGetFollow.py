from requests_oauthlib import OAuth1Session
import json

# twitterのアクセス用鍵
# oauth_key_dictはこの形式で与えてください
oauth_key_dict = {
	'consumer_key': '',
	'consumer_secret': '',
	'access_token': '',
	'access_token_secret': ''
}


# 戻り値: フォロワーIDのリスト
def getFollower(oauth_key_dict, screen_name):
	followers = []

	# フォロワー取得用のURL
	url = "https://api.twitter.com/1.1/followers/ids.json"
	params = {"screen_name": screen_name, "count": 1500}
	# OAuth認証で HTTPS GET method
	twitter = OAuth1Session(oauth_key_dict['consumer_key'], oauth_key_dict['consumer_secret'], oauth_key_dict['access_token'], oauth_key_dict['access_token_secret'])
	req = twitter.get(url, params = params)
	if req.status_code == 200:
		# レスポンスはreq.textに含まれる。JSON形式なので parse する
		recdata = json.loads(req.text)
		followers = recdata['ids']
	else:
		# エラーの場合
		print ("Error: %d" % req.status_code)
	return followers

def getFollowee(oauth_key_dict, screen_name):
	followees = []
	# フォロー取得用のURL
	url = "https://api.twitter.com/1.1/friends/ids.json"
	params = {"screen_name": screen_name, "count": 2000}
	# OAuth認証で HTTPS GET method
	twitter = OAuth1Session(oauth_key_dict['consumer_key'], oauth_key_dict['consumer_secret'], oauth_key_dict['access_token'], oauth_key_dict['access_token_secret'])
	req = twitter.get(url, params = params)
	if req.status_code == 200:
		# レスポンスはreq.textに含まれる。JSON形式なので parse する
		recdata = json.loads(req.text)
		followees = recdata['ids']
	else:
		# エラーの場合
		print ("Error: %d" % req.status_code)
	return followees


def getScreennameById(oauth_key_dict, id):
	# ユーザー情報取得用URL
	url = "https://api.twitter.com/1.1/users/lookup.json"
	params = {"user_id": id}
	# OAuth認証で HTTPS GET method
	twitter = OAuth1Session(oauth_key_dict['consumer_key'], oauth_key_dict['consumer_secret'], oauth_key_dict['access_token'], oauth_key_dict['access_token_secret'])
	req = twitter.get(url, params = params)
	if req.status_code == 200:
		# レスポンスはreq.textに含まれる。JSON形式なので parse する
		recdata = json.loads(req.text)
		screen_name = []
		for user in recdata:
			screen_name += [user["screen_name"]]
	else:
		# エラーの場合
		print ("Error: %d" % req.status_code)
	return screen_name


def writeJSONToFile(filename, writedata):
	fout = open(filename, "w")
	json.dump(writedata, fout, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


# 使用例
screen_name = '' # screen name
filename = screen_name + ".json"

followers = getFollower(oauth_key_dict, screen_name)
followees = getFollowee(oauth_key_dict, screen_name)
output = {'screen_name': screen_name, 'followers': followers, 'followees': followees}
writeJSONToFile(filename, output)
print("finished")

