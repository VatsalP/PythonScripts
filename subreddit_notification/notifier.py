import configparser
import logging
import re

from datetime import datetime
from typing import Sequence, List

import orjson
import praw
import requests

from pony import orm


logging.basicConfig(level=logging.WARNING)
db = orm.Database()


class Post(db.Entity):
    name = orm.PrimaryKey(str)
    subreddit = orm.Required(str)
    title = orm.Required(str)
    link = orm.Required(str)
    created_at = orm.Required(datetime)


def get_posts(url: str) -> List[Post]:
    """Get new posts using the url

    If any store them and return them as a list
    """
    headers = {"user-agent": "Subreddit Notification Script"}
    request = requests.get(url, headers=headers)
    content = orjson.loads(request.content.decode("utf-8"))
    posts = []
    with orm.db_session:
        for post in content["data"]["children"]:
            data = post["data"]
            posts.append(
                Post(
                    name=data["name"],
                    subreddit=data["subreddit"],
                    title=data["title"],
                    link=data["permalink"],
                    created_at=datetime.utcfromtimestamp(data["created_utc"]),
                )
            )
    return posts


def send_notifications(posts: List[Post], config: configparser.ConfigParser):
    """Send private reddit message to yourself"""
    reddit_conf = config["REDDIT"]
    user = reddit_conf["Username"]
    subreddit = config["DEFAULT"]["Subreddit"].strip()
    reddit = praw.Reddit(
        client_id=reddit_conf["ClientID"],
        client_secret=reddit_conf["ClientSecret"],
        password=reddit_conf["Password"],
        user_agent="Subreddit Notification Script",
        username=user,
    )
    for post in posts:
        reddit.redditor(user).message(
            f"{subreddit}: new post matching query", f"{post.title}\n{post.link}")


def main(args: Sequence[str]):
    config = configparser.ConfigParser()
    files = config.read(args.config)
    if not files:
        logging.error("Config not found")
        return

    # connect to db
    db_file = config["DEFAULT"]["SqliteDB"]
    db.bind(provider="sqlite", filename=db_file, create_db=True)
    db.generate_mapping(create_tables=True)

    # format the url
    subreddit = config["DEFAULT"]["Subreddit"].strip()
    url = f"https://reddit.com/r/{subreddit}/new/.json?count=5"
    with orm.db_session:
        latest_post = Post.select().sort_by(orm.desc(Post.created_at))[
            :1
        ]
    if latest_post:
        url += f"&before={latest_post[0].name}"
    posts = get_posts(url)

    # filters posts based on queries
    # and then send notification
    # using praw with user provided config
    regex_comp = re.compile(config["DEFAULT"]["FilterQuery"])
    posts = list(filter(lambda post: regex_comp.search(post.title) != None, posts))
    send_notifications(posts, config)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Subreddit new posts notifier with filtering"
    )
    parser.add_argument(
        "--config",
        "-c",
        default="notifier.cfg",
        help="Config with options for notifier",
    )
    args = parser.parse_args()
    main(args)
