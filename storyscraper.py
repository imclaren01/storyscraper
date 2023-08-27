import praw
import sys
import json
import html2text as ht


def main(client_id, client_secret,
         user_agent, username=None,
         password=None, subreddit="writingprompts",
         multireddit=None, time="month",
         sort_type="top", number=5,
         score_minimum=300, story_in_comments=True,
         prefix="[WP]", filename="stories/stories.json"):
    if username and password:
        reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent,
                username=username,
                password=password)
    else:
        reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent)

    reddit.read_only = True

    if multireddit:
        subreddit = reddit.multireddit(redditor=multireddit(0),
                                       name=multireddit(1))
    else:
        subreddit = reddit.subreddit(subreddit)

    print(subreddit.display_name)

    stories = find_content(
        reddit, subreddit, sort_type, time,
        number, score_minimum, story_in_comments, prefix)

    write_content(stories, filename)


def find_content(reddit, sub, sort_type, time,
                 number, score_minimum, story_in_comments, prefix):
    match sort_type:
        case "top":
            submissions = sub.top(time_filter=time, limit=number)
        case "hot":
            submissions = sub.hot(limit=number)
        case "new":
            submissions = sub.new(limit=number)
        case "gilded":
            submissions = sub.gilded(limit=number)

    stories = []
    story_data = []

    if story_in_comments:
        for s in submissions:
            print(f"Title: {s.title}, Score: {s.score}")

            s.comment_limit = 3
            s.comments.replace_more(limit=0)
            comments = s.comments.list()
            prompt_text = s.title

            if (prefix != "" and
                    prefix not in prompt_text[0:len(prefix) + 4]):
                print("Prefix failure")
                continue
            prompt_text = prompt_text[prompt_text.index(prefix) + len(prefix):].strip()

            for c in comments:
                if (not c.stickied) and (c.score >= score_minimum):
                    story_text = ht.html2text(c.body_html)
                    stories.append(story_text)
                    story_data.append({
                       "Title": f"{prompt_text}",
                       "Subreddit": f"{sub.display_name}",
                       "Author": f"{c.author.name if c.author else 'No name'}",
                       "Prompt Author": f"{s.author.name if s.author else 'No name'}",
                       "Read": False})
                    break
    else:
        for s in submissions:
            print(f"Title: {s.title}, Score: {s.score}")

            title = s.title
            text = s.selftext

            if (prefix != "" and
                    prefix not in title[0:len(prefix) + 4]):
                print("Prefix failure")
                continue

            title = title[title.index(prefix) + len(prefix):].strip()
            text = text.strip()

            if (not s.stickied) and (s.score >= score_minimum):
                stories.append(text)
                story_data.append({
                    "Title": f"{title}",
                    "Subreddit": f"{sub.display_name}",
                    "Author": f"{s.author.name}",
                    "Read": False})

    stories = {f"{story}": story_data[i] for (i, story) in enumerate(stories)}

    return stories


def write_content(stories, filename):
    with open(f"{filename}", "a") as f:
        json.dump(stories, f, indent=4)

    # print(f"{list(stories.keys())[0]}")

    print(f"Elements added to {filename}")


if __name__ == "__main__":
    client_id = "knWWW9skY0tyMxjYYIv2og"
    client_secret = "Uet89J1bSJJsJjUU3ZHPZ3I0Polfyw"
    user_agent = "windows:storyscraper:v0.0.1 (by /u/entercenterstage)"
    username = "entercenterstage"
    password = "Dogtoast11"

    main(client_id, client_secret, user_agent, username, password)
