import tweepy

from api_keys import oauth, oauth_secret, token, token_secret

auth = tweepy.OAuthHandler(oauth, oauth_secret)
auth.set_access_token(token, token_secret)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


for status in tweepy.Cursor(api.user_timeline).items():
    try:
        if status.id in protected_tweets:
            continue
        api.destroy_status(status.id)
        print("Deleted:", status.id)
    except:
        print("Failed to delete:", status.id)
