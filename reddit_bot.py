import praw, config, time, os

def bot_login():
	print ('Logging in...')
	r = praw.Reddit(username = config.username,
				password = config.password,
				client_id = config.client_id,
				client_secret = config.client_secret,
				user_agent = "The Reddit Commenter v1.0")
	print ('Logged in!')

	return r

def run_bot(r, comments_replied_to):
	print ('Searching last 200 comments')

	for comment in r.subreddit('subreddit').comments(limit=200):
		compareWith = ''
		compareWith = compareWith.upper()
		keyWords = comment.body
		keyWords = keyWords.upper()
		f = open('comments_replied_to.txt')
		if ((compareWith in keyWords) and (comment.id not in comments_replied_to) and (comment.author != r.user.me())):			
			print (f'String with "{compareWith}" found in comment {comment.id}')
			comment.reply('Reply text')
			print (f'Replied to comment {comment.id}')

			file1=open('comments_replied_to.txt', 'a')
			file1.write(comment.id + '\n')
			file1.close()

	print ('Search Completed.')
	print (comments_replied_to)
	print ('Sleeping for 10 seconds...')
	#Sleep for 10 seconds...		
	time.sleep(10)

def get_saved_comments():
	if not os.path.isfile('comments_replied_to.txt'):
		comments_replied_to = []
	else:
		f = open('comments_replied_to.txt', 'r')
		comments_replied_to = f.read()
		comments_replied_to = comments_replied_to.split('\n')
		comments_replied_to = filter(None, comments_replied_to)

	return comments_replied_to

r = bot_login()
comments_replied_to = get_saved_comments()
print (comments_replied_to)

while True:
	comments_replied_to = get_saved_comments()
	run_bot(r, comments_replied_to)
	
