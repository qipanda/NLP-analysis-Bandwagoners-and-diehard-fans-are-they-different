import pickle
import constants as cnst
import pandas as pd
import datetime
import pytz
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

def cvt_json_to_df():
    '''
    Given pickle files for nfl comments data, convert and save them as pandas dataframe pickle files
    '''
    for fname in list(set(cnst.REG_SEASON_FNAMES + cnst.FIRST_MONTH_FNAMES)):
        # load json's (lists of dicts)
        with open("nfl_comments_json/{}.pkl".format(fname), "rb") as f_read:
            raw_pickle = pickle.load(f_read)

        # convert to df and filter to proper flairs
        df = pd.DataFrame(raw_pickle)
        df = df.loc[df["author_flair_css_class"].isin(cnst.FLAIRS_PROPER), :]

        print(len(list(df.loc[df["author_flair_css_class"].isin(cnst.FLAIRS_PROPER), "author_flair_css_class"].unique())))

        # pandas can directly take list of dicts
        with open("nfl_comments_pandas_df/{}.pkl".format(fname), "wb") as f_dump:
            pickle.dump(df, f_dump)

def create_reg_comments():
    fnames = cnst.REG_SEASON_FNAMES

    dfs_comments = []
    for fname in fnames:
        with open("nfl_comments_pandas_df/{}.pkl".format(fname), "rb") as f_read:
            dfs_comments.append(pickle.load(f_read))

    df_comments = pd.concat(dfs_comments)
    df_comments = df_comments.loc[
        (df_comments["created_utc"]>=cnst.REG_UTC_START - 7*24*60*60)&
        (df_comments["created_utc"]<=cnst.REG_UTC_END + 6*24*60*60), :] # sept 1st to jan 8th PST reg season +- 7days

    with open("dfs/df_comments.pkl", "wb") as f_dump:
        pickle.dump(df_comments, f_dump)

def load_dfs():
    '''
    return preprocessed dfs
    '''
    with open("dfs/df_comments.pkl", "rb") as f_comments:
        df_comments = pickle.load(f_comments)

    with open("dfs/df_author_flair.pkl", "rb") as f_teamauth:
        df_teamauth = pickle.load(f_teamauth)

    with open("dfs/df_win_loss.pkl", "rb") as f_winloss:
        df_winloss = pickle.load(f_winloss)

    return df_comments, df_teamauth, df_winloss

def load_dfs_from_pkl(reg=True):
    if reg:
        fnames = cnst.REG_SEASON_FNAMES
    else:
        fnames = cnts.FIRST_MONTH_FNAMES

    dfs_comments = []
    for fname in fnames:
        with open("nfl_comments_pandas_df/{}.pkl".format(fname), "rb") as f_read:
            dfs_comments.append(pickle.load(f_read))

    return dfs_comments

def create_team_author_pairs():
    '''
    takes dataframes and creates team/author pairs including last year since start of season they had that flair (rounded down to nearest year)
    '''
    dfs = load_dfs_from_pkl(reg=False)

    print("{}".format(dfs[-1]["created_utc"].max()))

    # for 2016, find unique team-author pairs
    df_team_auth = dfs[-1]\
        .drop_duplicates(subset=["author_flair_css_class", "author"])\
        .loc[:, ["author_flair_css_class", "author"]]\
        .reset_index(drop=True)

    # create such team-author pairs for all years, left join and find how far back existed as that fan
    dfs = dfs[:-1] # remove 2016
    dfs.reverse() # order now from 2015 -> 2010
    df_team_auth.loc[:, "yrs_existed_back"] = 0 # so far only exist in 2016 (0 yrs back)

    for i, df in enumerate(dfs, 1):
        print("{}".format(df["created_utc"].max()))

        # find the team-author pairs from the past september comments
        df_team_auth_past = df\
            .drop_duplicates(subset=["author_flair_css_class", "author"])\
            .loc[:, ["author_flair_css_class", "author"]]\
            .reset_index(drop=True)
        df_team_auth_past["dummy"] = True

        # if existed, then at least existed i years back (enumerate started at 1 here) otherwise dummy = NULL
        df_team_auth = df_team_auth.merge(
            right=df_team_auth_past, how="left", on=["author_flair_css_class", "author"])
        df_team_auth.loc[df_team_auth["dummy"]==True, "yrs_existed_back"] = i
        df_team_auth.drop(labels="dummy", axis=1, inplace=True)

    # pandas can directly take list of dicts
    with open("dfs/df_author_flair.pkl", "wb") as f_dump:
        pickle.dump(df_team_auth, f_dump)

def create_winloss():
    # read in data, get rid of nan rows, apply datetime
    df = pd.read_csv("2016_Reg_Season_Games.csv")
    df = df.loc[(~df["PtsW"].isnull()) & (df["Week"].str.isnumeric()), :]
    df.loc[:, "UTC_START_DAY"] = pd.to_datetime(arg=df["Date"], format="%d-%b")
    df.loc[:, "UTC_START_DAY"] = \
        df.loc[:, "UTC_START_DAY"].apply(
            lambda x: datetime.datetime(year=2016, day=x.day, month=x.month, tzinfo=pytz.UTC).timestamp() \
            if x.month >=9 else \
            datetime.datetime(year=2017, day=x.day, month=x.month, tzinfo=pytz.UTC).timestamp()
        )

    '''
    each row is a game, split each row into two rows into the schema:
    WEEK | UTC_START_DAY | TEAM | RESULT \in {W,L,T}
    '''
    data = []
    for idx, row in df.iterrows():
        new_row = {}
        new_row["Week"] = int(row["Week"])
        new_row["UTC_START_DAY"] = row["UTC_START_DAY"]

        # if a tie
        if row["PtsW"] == row['PtsL']:
            new_row["Team"] = row["Winner/tie"]
            new_row["Result"] = "T"
            data.append(new_row.copy())
            new_row["Team"] = row["Loser/tie"]
            data.append(new_row.copy())
        else:
            new_row["Team"] = row["Winner/tie"]
            new_row["Result"] = "W"
            data.append(new_row.copy())

            new_row["Team"] = row["Loser/tie"]
            new_row["Result"] = "L"
            data.append(new_row.copy())

    # find the order of games out of the 17 weeks
    df_expanded = pd.DataFrame(data)
    df_expanded["Game Order"] = df_expanded.groupby("Team")["Week"].rank(ascending=True)
    df_expanded.drop(labels="Week", axis=1, inplace=True)

    # pandas can directly take list of dicts
    with open("dfs/df_win_loss.pkl", "wb") as f_dump:
        pickle.dump(df_expanded, f_dump)

def create_final_df():
    '''
    Load preprocessed dataframes
    df_comments - comments of all reddit users for the 2016-2017 NFL regular season
        the /r/nfl subreddit +- 7 days from season beginning to end in PST (timestamps
        are given in UTC however)
    df_teamauth - flair/author combinations for all users who commented and their
        years as a fan of that team rounded to the lowest year
    df_winloss -
    '''
    df_comments, df_teamauth, df_winloss = load_dfs()

    # join comments with teamauth to get the yrs_existed_back as a fan for all authors in every comment
    df = pd.merge(left=df_comments, right=df_teamauth, how="inner", on=["author_flair_css_class", "author"])

    # convert author_flair_css_class to proper team name title
    df.loc[:, "author_flair_css_class"] = df.loc[:, "author_flair_css_class"]\
        .apply(lambda x: cnst.OFFICIAL_FLAIR_MAP[x])

    # add 7 hours to all UTC_START_DAYS to make them align with PST
    df_winloss.loc[:, "UTC_START_DAY"] = df_winloss.loc[:, "UTC_START_DAY"] + 7*60*60

    # first merge each comment with the 16 possible games it could be associated with
    df = pd.merge(left=df, right=df_winloss, how="inner", left_on="author_flair_css_class", right_on="Team")

    # for every comment-game pair, take difference of time stamps as comment_UTC - game_UTC
    df.loc[:, "UTC_Diff"] = df["created_utc"] - df["UTC_START_DAY"]

    # at this point, filter out some uneccesary rows
    df.drop(labels=[
        "author_cakeday",
        "author_flair_css_class",
        "author_flair_text",
        "distinguished",
        "retrieved_on",
        "subreddit",
        "subreddit_id"], axis=1, inplace=True)

    # take only positive differences (comment was after the game), and closest one (min)
    df = df.loc[df["UTC_Diff"]>=0, :]
    diff_filter = df.groupby("id")["UTC_Diff"].min().to_frame().reset_index() # msg id
    df = pd.merge(left=df, right=diff_filter, how="inner", on=["id", "UTC_Diff"])
    df = df.loc[df["UTC_Diff"]>= 24*60*60, :] # must be at least 24 hrs since game start
    df.drop(labels=["UTC_Diff"], axis=1, inplace=True)

    with open("dfs/df_final.pkl", "wb") as f_dump:
        pickle.dump(df, f_dump)

def create_metric_df():
    # load preprocessed data
    with open("dfs/df_final.pkl", "rb") as f:
        df = pickle.load(f)

    # make we column
    df.loc[:, "We"] = df["body"].apply(lambda x: "we" in x.lower().split())

    # make sentiment column
    sid = SentimentIntensityAnalyzer()
    df.loc[:, "VADER"] = df["body"].apply(lambda x: sid.polarity_scores(x)['compound'])

    with open("dfs/df_metrics.pkl", "wb") as f_dump:
        pickle.dump(df, f_dump)

def append_metrics():
    with open("dfs/df_metrics.pkl", "rb") as f:
        df = pickle.load(f)

    # df.drop(labels=["Win Ratio_x", "Seed_x", "Win Ratio_y", "Seed_y", "Win Rank Quartile", "Win Rank"], axis=1, inplace=True)

    team_winratios = [(team, ratio) for team, ratio in cnst.FINAL_WINRATIO.items()]
    df_ratios = pd.DataFrame(team_winratios, columns=["Team", "Win Ratio"])

    team_playoff_seed = [(team, seed) for team, seed in cnst.FINAL_PLAYOFF_SEED.items()]
    df_seeds = pd.DataFrame(team_playoff_seed, columns=["Team", "Seed"])

    # give ranks based on winratio, and split into quartiles
    df_ratios["Win Rank"] = df_ratios["Win Ratio"].rank(ascending=False)
    df_ratios["Win Rank Quartile"] = df_ratios["Win Rank"].apply(lambda x: 1 if x<=8 else (2 if x <=16 else (3 if x <= 24 else 4)))

    df = df.merge(right=df_ratios, how="inner", on="Team")
    df = df.merge(right=df_seeds, how="inner", on="Team")

    with open("dfs/df_metrics.pkl", "wb") as f_dump:
        pickle.dump(df, f_dump)

def create_team_nicks():
    '''
    Create a dictionary, team_nicknames, where:
        KEY     = official team name
        VALUE   = list of regex
    '''
    team_nicknames = {}

    with open("dfs/df_metrics.pkl", "rb") as f:
        df = pickle.load(f)

    official_team_names = df["Team"].drop_duplicates().values.tolist()
    for team_name in official_team_names:
        nicknames = []
        # split team name into location and name
        team_name_split = team_name.split()
        off_location_name = ".{0,1}".join(team_name_split[:-1]) # if team name is two words, allow for 0 or 1 char inbetween
        off_team_name = team_name_split[-1]
        off_team_name = off_team_name[:-1] # trim the s off to append ('){0,1}s for flexibility

        # add location name and team name | (^\s)'s make sure white space or begin before and
        # ($\s)'s make sure white space or end after'
        nicknames.append("(^|\s)" + off_location_name + "($|.{0,1}\s|)")
        nicknames.append("(^|\s)" + off_team_name + "('){0,1}s($|.{0,1}\s)") # last letter is 's' must have

        # add team location abrv. if not N/A indicating it is a common word
        if cnst.CITY_ABRVS[team_name]!="N/A":
            nicknames.append("(^|\s)" + cnst.CITY_ABRVS[team_name] + "($|.{0,1}\s)")

        # add specific team names if any
        if len(cnst.TEAM_NICKNAMES_REGEX[team_name]) > 0:
            for nick in cnst.TEAM_NICKNAMES_REGEX[team_name]:
                nicknames.append("(^|\s)" + nick + "($|.{0,1}\s)")

        team_nicknames[team_name] = nicknames

    # now create dictionary for each team with the nicknames of all OTHER teams
    other_team_nicks = {}
    for team_name in official_team_names:
        other_nicks = []
        # iterate through other teams nicknames and add them
        for other_team, value in team_nicknames.items():
            if (other_team != team_name) & (len(value)>0):
                for nick in value:
                    other_nicks.append(nick)
        other_team_nicks[team_name] = other_nicks

    # save these dictionaries
    with open("dicts/team_nicknames.pkl", "wb") as f_dump1:
        pickle.dump(team_nicknames, f_dump1)

    with open("dicts/other_team_nicks.pkl", "wb") as f_dump2:
        pickle.dump(other_team_nicks, f_dump2)

def append_nick_binaries():
    '''
    Insert binary scores of whether or not own team mentioned, other team mentioned based on dicts
    '''
    with open("dfs/df_metrics.pkl", "rb") as f:
        df = pickle.load(f)

    with open("dicts/team_nicknames.pkl", "rb") as f_dump1:
        team_nicknames = pickle.load(f_dump1)

    with open("dicts/other_team_nicks.pkl", "rb") as f_dump2:
        other_team_nicks = pickle.load(f_dump2)

    df.loc[:, "Team Mention"] = df.loc[:, ["Team", "body"]].apply(
        func=search_for_mention,
        axis=1,
        args=(team_nicknames,)
    )

    df.loc[:, "Other Team Mention"] = df.loc[:, ["Team", "body"]].apply(
        func=search_for_mention,
        axis=1,
        args=(other_team_nicks,)
    )

    with open("dfs/df_metrics.pkl", "wb") as f_dump:
        pickle.dump(df, f_dump)

def search_for_mention(row, nicks):
    '''
        row         = row of current comment -> row["Team"] gives team of current commenter -> row[""]
        nicks       = dictionary where nicks[team_key] gives list of regex to look for
    '''
    for nick in nicks[row["Team"]]:
        if re.search(pattern=nick, string=row["body"], flags=re.IGNORECASE) is not None:
            return True

    return False

def final_df_ammendments():
    '''
        Get VADER pos, neut, neg scores as well not just compound
    '''
    with open("dfs/df_metrics.pkl", "rb") as f:
        df = pickle.load(f)

    # make sentiment column
    sid = SentimentIntensityAnalyzer()
    df.loc[:, "VADER_tup"] = df.loc[:, "body"].apply(lambda x: sid.polarity_scores(x))
    df.loc[:, "POS"] = df.loc[:, "VADER_tup"].apply(lambda x: x["pos"])
    df.loc[:, "NEU"] = df.loc[:, "VADER_tup"].apply(lambda x: x["neu"])
    df.loc[:, "NEG"] = df.loc[:, "VADER_tup"].apply(lambda x: x["neg"])
    df.drop(labels=["VADER_tup"], axis=1, inplace=True)

    with open("dfs/df_metrics.pkl", "wb") as f_dump:
        pickle.dump(df, f_dump)
