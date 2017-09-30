#!/usr/local/bin/python3
## join all post titles together as a string for each company for each day
import json
import time
import datetime
import pandas as pd
from pandas import DataFrame as df

def reformat(file_in):
    """
    reads the json file of file_in, extract [Title | Subreddits | Total votes | Upvotes | Downvotes] for each day for each company. 
    return: {company_name: {date1: extraction, date2:extraction}, ...}
    """
    data = json.load(open(fin)) 
    comp_post_daily = {} # {company_name: {date1:[post],date2:[post]},...}
    for comp,posts in data.items():
        # print("Company name %s, number of posts: %s"%(comp, len(posts)))
        for post in posts:
            t = post["created_utc"]
            d = datetime.datetime.utcfromtimestamp(float(t)).strftime('%Y-%m-%d,%H:%M:%SZ') # formatted date-time
            day_ = int(d.split(",")[0].split("-")[2])

            ## extract from the post: Title | Subreddits | Total votes |  Downvotes | Upvotes
            info = [post["title"], post["subreddit"],-post["downs"], post["score"] + post["downs"]]
            if not comp_post_daily.get(comp):
                comp_post_daily[comp]= {}
                comp_post_daily[comp][day_] = info
            else:
                if not comp_post_daily[comp].get(day_):
                    comp_post_daily[comp][day_] = info
                else:
                    title, subred, down, up = comp_post_daily[comp][day_]
                    title += " "+info[0]
                    subred += " "+info[1]
                    down += info[2]
                    up += info[3]
                    new_info = [title, subred, down, up]
                    comp_post_daily[comp][day_] = new_info

    print("Processed %s companies in file"%len(comp_post_daily), file_in)
    return comp_post_daily

def to_csv(data, out_file = None):
    dfs = []
    for company, daily_posts in data.items():
        df_ = df.from_dict(daily_posts,orient = 'index')
        df_.columns = ["title","subreddit","downvotes","upvotes"]
        df_["company"] = [company]*len(daily_posts)
        df_["date"] = df_.index
        dfs.append(df_)

    out = pd.concat(dfs)
    if out_file:
        out.to_csv(out_file)
    return out
    

if __name__=="__main__":
    # fin = "datas/post.json"
    fin = sys.argv[1]
    fout = sys.argv[2]
    X_feature = reformat(fin)
    out = to_csv(X_feature,fout)
   

    
