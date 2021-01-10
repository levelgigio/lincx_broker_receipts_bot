""" Quickstart script for InstaPy usage """
# imports
from instapy import InstaPy
from instapy import smart_run
import time
from datetime import datetime
from datetime import timedelta
import random

# login credentials
insta_username = 'unicorn.rentals'  # <- enter username here
insta_password = 'iFoster42'  # <- enter password here

hashtags = ['unicornio', 'unicorn', 'felicidade', 'followforfollow', 'gay', 
            'branding', 'marketing', 'startup', 'firma',]

users = []

while True:
    try:
        # get an InstaPy session!
        # set headless_browser=True to run InstaPy in the background
        session = InstaPy(username=insta_username,
                        password=insta_password,
                        headless_browser=False)

        with smart_run(session):
            """ Activity flow """
            random.shuffle(hashtags)
            random.shuffle(users)

            selected_hashtags = hashtags[:1]
            selected_users = users[:1]
            print(selected_hashtags)
            print(selected_users)
            # session.set_quota_supervisor(enabled=True,
            #                             sleep_after=["likes", "follows"],
            #                             sleepyhead=True, 
            #                             stochastic_flow=True,
            #                             notify_me=True,
            #                             peak_likes_hourly=20,
            #                             peak_likes_daily=60,
            #                             peak_follows_hourly=20,
            #                             peak_follows_daily=150,
            #                             peak_unfollows_hourly=35,
            #                             peak_unfollows_daily=210,
            #                             peak_server_calls_hourly=None,
            #                             peak_server_calls_daily=4700)

            session.set_do_follow(enabled=True, percentage=80, times=1)
            session.set_do_like(True, percentage=70)
            session.set_user_interact(amount=3, randomize=True, percentage=80)


            session.like_by_tags(selected_hashtags, amount=1)
            session.follow_user_followers(selected_users, amount=1, randomize=False)

            # session.unfollow_users(amount=20, instapy_followed_enabled=True, instapy_followed_param="nonfollowers",
            #                     style="FIFO",
            #                     unfollow_after=12 * 60 * 60, sleep_delay=501)
            # session.unfollow_users(amount=20, instapy_followed_enabled=True, instapy_followed_param="all",
            #                     style="FIFO", unfollow_after=24 * 60 * 60,
            #                     sleep_delay=501)

            # session.join_pods(topic='entertainment', engagement_mode='no_comments')
        session.end()

        next_run = datetime.now() + timedelta(days=1)
        next_run = next_run.replace(hour=10, minute=0, second=0, microsecond=0)
        sleep_time = next_run - datetime.now()
        print(f'Sleeping {sleep_time.hours} hours...')
        time.sleep(sleep_time.seconds)
    
    except KeyboardInterrupt:
        print('Done')
        break
    except:
        pass