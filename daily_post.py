#!/usr/local/bin/python3
## join all post titles together as a string for each company for each day
import json
import time
import datetime
import sys
import re
import pandas as pd
from pandas import DataFrame as df


def tick2name():
    df = pd.read_csv('/data/ImplementReddit/companies/constituents.csv')
    symb_name = {}
    for line in df[['Symbol', 'Name']].values:
        name = line[1].lower()
        name_ = re.sub(r'(\scorp.{2}|\sinc.*|\scos.*|\&\sco.*|\sco.*|ltd.|the\s)',"",name) # strip off the Inc/Corp stuff
        symb_name[name_] = line[0]
    return symb_name

def reformat(file_in, name_symb):
    """
    reads the json file of file_in, extract [Title | Subreddits | Total votes | Upvotes | Downvotes] for each day for each company. 
    return: {company_name: {date1: extraction, date2:extraction}, ...}
    """
    data = json.load(open(fin)) 
    comp_post_daily = {} # {company_name: {date1:[post],date2:[post]},...}
    for comp,posts in data.items():
        # print("Company name %s, number of posts: %s"%(comp, len(posts)))
        comp = name_symb[comp]
        for post in posts:
            t = post["created_utc"]
            d = datetime.datetime.utcfromtimestamp(float(t)).strftime('%Y-%m-%d,%H:%M:%SZ') # formatted date-time
            day_ = d.split(",")[0]

            ## extract from the post: Title | Subreddits | Total votes |  Scores | #comments
            try:
                title_ = post["title"]
            except KeyError:
                print(" No title!")
                title_ = ""
            try:
                subr_ = post["subreddit"]
            except KeyError:
                print(" No subreddit!")
                subr_ = ""
            try:
                score_=post["score"]
            except KeyError:
                print("No score")
                score_ = 0
            try:
                 n_comment_ =  post["num_comments"]
            except KeyError:
                print("No number of comments!")
                n_comment_ = 0
            info = [title_, subr_,score_,n_comment_]
            if not comp_post_daily.get(comp):
                comp_post_daily[comp]= {}
                comp_post_daily[comp][day_] = info
            else:
                if not comp_post_daily[comp].get(day_):
                    comp_post_daily[comp][day_] = info
                else:
                    title, subred, score, n_comment = comp_post_daily[comp][day_]
                    title += " "+title_
                    subred += " "+subr_
                    score += score_
                    n_comment += n_comment_
                    new_info = [title, subred, down, up]
                    comp_post_daily[comp][day_] = new_info

    print("Processed %s companies in file"%len(comp_post_daily), file_in)
    return comp_post_daily

def to_csv(data, out_file = None):
    dfs = []
    for company, daily_posts in data.items():
        df_ = df.from_dict(daily_posts,orient = 'index')
        df_.columns = ["title","subreddit","scores","num_comments"]
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
    name_symb = tick2name()
    X_feature = reformat(fin, name_symb)
    out = to_csv(X_feature,fout)
   

    
