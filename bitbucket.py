import requests
import json
import webbrowser
USERNAME = 'AlanMamphs'
REPOUSERNAME = 'Alisher123'
PASSWORD = 'ALI0303sher'
EMAIL    = 'mamunovalisher@gmail.com'

def userInput():	
	# username, password, email, repo = '', '', '', ''

	# while not username:
	# 	username =  input("Please enter your BitBucket account username:")
	# while not email:
	# 	email    =  input("Please enter your BitBucket account email:")
	# while not password:
	# 	password =  input("Please enter your BitBucket account password:")
			
	repo = input("Do you want to search in concrete repository? Indicate it and press enter. Otherwise press enter with empty field:")
	
	r = requests.get('https://api.bitbucket.org/2.0/repositories/%s'%(USERNAME), auth=(EMAIL, PASSWORD))

	if r.status_code == 200:

		if not repo:
			data = r.json()
			repositories = []
			for r in data['values']:
				repositories.append(r['slug'])

			print (repositories)
			links = []
			ids   = []
			pullrequestslinks = []
			for rep in repositories:
				r = requests.get('https://api.bitbucket.org/2.0/repositories/%s/%s/pullrequests'%(USERNAME,rep), auth=(EMAIL, PASSWORD))
				data = r.json()
				for value in data['values']:
					links.append(value['links']['html']['href'])
					ids.append(value['id'])
					r = requests.get('https://api.bitbucket.org/2.0/repositories/%s/%s/pullrequests/%d'%(USERNAME,rep, value['id']), auth=(EMAIL, PASSWORD))
					data = r.json()
					print (data)
					print(type(data['participants'][0]['approved']))
					
					isReviewer = False;
					isApproved = True;

					for i in data['reviewers']:
						if i['username']== REPOUSERNAME:
							isReviewer == True;

					for i in data['participants']:
						if i['user']['username']== REPOUSERNAME and i['approved']== False:
							isApproved == False;

					if data['state'] == 'OPEN' and  isReviewer == True and isApproved ==False :
					 	pullrequestslinks.append(data['links']['html']['href'])

					print (pullrequestslinks)
			

		

# and 
userInput()
# 		data = r.json()
# 		repositories = []
# 		for r in data['values']:
# 			repositories.append(r['slug'])
# 		r = requests.get('https://api.bitbucket.org/2.0/repositories/%s'%(username), auth=(email, password))


# # 	repo = ""
# # 	repo  =  
# # 	username = "AlanMamphs"
# # 	# repo     = "alanmamphs"
# # 	password = "ALI0303sher"
# # 	email    = "mamunovalisher@gmail.com"

# # 	

# # 		if repositories:


# # 	if repo:
# # 		r = requests.get('https://api.bitbucket.org/2.0/repositories/%s/%s/pullrequests'%(username, repo), auth=(email, password))
# # 		data = r.json()
# # 		pullrequests = []
# # 		for r in data['values']:
# # 			pullrequests.append(r['links']['html']['href'])


# # 		print (pullrequests)


# # 	# print (r.status_code)

		
# # login()


