import requests
import json
import webbrowser

def bitBucketPR():	
	# method for opening team's bitbucket pull requests to be reviewed by user

	team, username, password, email, repos = '', '', '', '', ''
	# inquiring user credentials
	while not username:
		username =  input("Please enter your BitBucket account username:")
	while not email:
		email    =  input("Please enter your BitBucket account email:")
	while not password:
		password =  input("Please enter your BitBucket account password:")
	while not team:
		team     =   input('Please enter your Bitbucket team name:')

	# specifying the repository
	repos = input("Indicate either a reposiory or a list of repositories dividing each by space and press enter. Leave empty if you want to search in all team repositories:")
	
	# requesting data from bitbucket
	r = requests.get('https://api.bitbucket.org/2.0/repositories/%s'%(team), auth=(email, password))


	# checking if data available
	if r.status_code == 200:

		# retrieving and storing all available repositories names
		if not repos:
			data = r.json()
			repositories = []

			for r in data['values']:
				repositories.append(r['slug'])

			links = []  # list for appropriate pull requests urls
			
			
			for rep in repositories:      # iterating over found repositories for pull requests
				r = requests.get('https://api.bitbucket.org/2.0/repositories/%s/%s/pullrequests'%(team,rep), auth=(email, password))
				data = r.json()

				for value in data['values']:    # accessing each pull request
					
					r = requests.get('https://api.bitbucket.org/2.0/repositories/%s/%s/pullrequests/%d'%(team,rep, value['id']), auth=(email, password))
					data = r.json()

					for i in data['participants']:    # checking if prs are addressed to user for reviewing
						if i['user']['username'] == username and i['role'] == 'REVIEWER' and i['approved'] == False and data['state']=='OPEN':
							links.append(data['links']['html']['href']) # appending filtered prs

				
			# checking the qty of pull requests
			# opening if appropriate
			if len(links)>0 and len(links)< 11:
				for i in links:
					print ("Opening pull request in default browser....")

					webbrowser.open(i)
				
			elif len(links)>10:
				print("")
				print("Two many pull requests. Try to filter by repository.")
				print("")
			elif len(links)==0: 
				print("")
				print("Nothing was found. Try checking your credentials")
				print("")
		
		else:    # if repository was specified

			repo = repos.split(" ")
			links= []
			for element in repo:
				r = requests.get('https://api.bitbucket.org/2.0/repositories/%s/%s/pullrequests'%(team, element), auth=(email, password))
				data = r.json()
				if r.status_code == 200: 

					for value in data['values']:   # iterating over repo's pull requests
						links.append(value['links']['html']['href'])
					

					
					# checking the qty of pull requests
					# opening if appropriate

					if len(links)>0 and len(links)<11: # 
					# iterating over links to open them in the browser
						for i in links:
							print ("Opening pull request in default browser....")

							webbrowser.open(i)

					elif len(links)>10:  # optional. if two many prs even if repo is specified, open 10 prs.
						print("bitbucket.py")
						print('Two many PRs.')
						Print('Opening 10 of them')
						for i in range(9):
							print ("Opening pull request in default browser....")
							webbrowser.open(i)
				else: # handling 404 
					print("")
					print('For repository with', element, 'name, nothing was found. Check repository name.')
					print("")


	elif r.status_code == 401: # handling 401 error. 
		print("")
		print ("Unauthorized. Access Denied. Check your credentials. If your Bitbucket account has two-step verification, swith it off in your settings.")
		print("")
	elif r.status_code == 404: # handling 404 error
		print("")
		print ( "Could not find the pull requests.")
		print("")

# executing the function
bitBucketPR()
