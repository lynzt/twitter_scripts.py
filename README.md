## Synopsis
random repo to put twitter scripts...


## Running

docker build -t py/twitter .
docker run -it --rm -v "$PWD":/usr/src/app --env-file dev/config py/twitter python3 ./get_tweet_images.py
