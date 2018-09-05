# standard 'author_flair_css_class' teams (all 32)
FLAIRS_PROPER = [
    "patriots",
    "eagles",
    "vikings",
    "packers",
    "seahawks",
    "broncos",
    "cowboys",
    "panthers",
    "fortyniners",
    "steelers",
    "giants",
    "bears",
    "raiders",
    "ravens",
    "lions",
    "texans",
    "redskins",
    "colts",
    "chargers",
    "browns",
    "saints",
    "jets",
    "falcons",
    "bengals",
    "dolphins",
    "cardinals",
    "chiefs",
    "bills",
    "buccaneers",
    "jaguars",
    "rams",
    "titans"
]

# W/L record df Team names <-> 'author_flair_css_class'
OFFICIAL_FLAIR_MAP = {
        "patriots":"New England Patriots",
        "eagles":"Philadelphia Eagles",
        "vikings":"Minnesota Vikings",
        "packers":"Green Bay Packers",
        "seahawks":"Seattle Seahawks",
        "broncos":"Denver Broncos",
        "cowboys":"Dallas Cowboys",
        "panthers":"Carolina Panthers",
        "fortyniners":"San Francisco 49ers",
        "steelers":"Pittsburgh Steelers",
        "giants":"New York Giants",
        "bears":"Chicago Bears",
        "raiders":"Oakland Raiders",
        "ravens":"Baltimore Ravens",
        "lions":"Detroit Lions",
        "texans":"Houston Texans",
        "redskins":"Washington Redskins",
        "colts":"Indianapolis Colts",
        "chargers":"San Diego Chargers",
        "browns":"Cleveland Browns",
        "saints":"New Orleans Saints",
        "jets":"New York Jets",
        "falcons":"Atlanta Falcons",
        "bengals":"Cincinnati Bengals",
        "dolphins":"Miami Dolphins",
        "cardinals":"Arizona Cardinals",
        "chiefs":"Kansas City Chiefs",
        "bills":"Buffalo Bills",
        "buccaneers":"Tampa Bay Buccaneers",
        "jaguars":"Jacksonville Jaguars",
        "rams":"Los Angeles Rams",
        "titans":"Tennessee Titans"
}

# Final reg season w/l ratio
FINAL_WINRATIO = {
        "New England Patriots":14/16,
        "Philadelphia Eagles":7/16,
        "Minnesota Vikings":8/16,
        "Green Bay Packers":10/16,
        "Seattle Seahawks":10.5/16,
        "Denver Broncos":9/16,
        "Dallas Cowboys":13/16,
        "Carolina Panthers":6/16,
        "San Francisco 49ers":2/16,
        "Pittsburgh Steelers":11/16,
        "New York Giants":11/16,
        "Chicago Bears":3/16,
        "Oakland Raiders":12/16,
        "Baltimore Ravens":8/16,
        "Detroit Lions":9/16,
        "Houston Texans":9/16,
        "Washington Redskins":8.5/16,
        "Indianapolis Colts":8/16,
        "San Diego Chargers":5/16,
        "Cleveland Browns":1/16,
        "New Orleans Saints":7/16,
        "New York Jets":5/16,
        "Atlanta Falcons":11/16,
        "Cincinnati Bengals":6.5/16,
        "Miami Dolphins":10/16,
        "Arizona Cardinals":7.5/16,
        "Kansas City Chiefs":12/16,
        "Buffalo Bills":7/16,
        "Tampa Bay Buccaneers":9/16,
        "Jacksonville Jaguars":3/16,
        "Los Angeles Rams":4/16,
        "Tennessee Titans":9/16
}

# Final reg season whether in playoffs or not
FINAL_PLAYOFF_SEED = {
        "New England Patriots":1,
        "Philadelphia Eagles":0,
        "Minnesota Vikings":0,
        "Green Bay Packers":4,
        "Seattle Seahawks":3,
        "Denver Broncos":0,
        "Dallas Cowboys":1,
        "Carolina Panthers":0,
        "San Francisco 49ers":0,
        "Pittsburgh Steelers":3,
        "New York Giants":5,
        "Chicago Bears":0,
        "Oakland Raiders":5,
        "Baltimore Ravens":0,
        "Detroit Lions":6,
        "Houston Texans":4,
        "Washington Redskins":0,
        "Indianapolis Colts":0,
        "San Diego Chargers":0,
        "Cleveland Browns":0,
        "New Orleans Saints":0,
        "New York Jets":0,
        "Atlanta Falcons":2,
        "Cincinnati Bengals":0,
        "Miami Dolphins":6,
        "Arizona Cardinals":0,
        "Kansas City Chiefs":2,
        "Buffalo Bills":0,
        "Tampa Bay Buccaneers":0,
        "Jacksonville Jaguars":0,
        "Los Angeles Rams":0,
        "Tennessee Titans":0
}

CITY_ABRVS = {
        "New England Patriots":"NE",
        "Philadelphia Eagles":"PHI",
        "Minnesota Vikings":"N/A",# bad because was is a common word
        "Green Bay Packers":"GB",
        "Seattle Seahawks":"N/A", # bad because was is a common word
        "Denver Broncos":"N/A", # bad because was is a common word
        "Dallas Cowboys":"DAL",
        "Carolina Panthers":"N/A", # bad because was is a common word
        "San Francisco 49ers":"SF",
        "Pittsburgh Steelers":"N/A", # bad because was is a common word
        "New York Giants":"NYG",
        "Chicago Bears":"CHI",
        "Oakland Raiders":"N/A", # bad because was is a common word
        "Baltimore Ravens":"BAL",
        "Detroit Lions":"DET",
        "Houston Texans":"HOU",
        "Washington Redskins":"N/A", # bad because was is a common word
        "Indianapolis Colts":"IND",
        "San Diego Chargers":"SD",
        "Cleveland Browns":"CLE",
        "New Orleans Saints":"N/A", # bad because was is a common word
        "New York Jets":"NYJ",
        "Atlanta Falcons":"ATL",
        "Cincinnati Bengals":"CIN",
        "Miami Dolphins":"MIA",
        "Arizona Cardinals":"ARI",
        "Kansas City Chiefs":"KC",
        "Buffalo Bills":"BUF",
        "Tampa Bay Buccaneers":"TB",
        "Jacksonville Jaguars":"JAX",
        "Los Angeles Rams":"LA",
        "Tennessee Titans":"TEN"
}

# need to be gated by (^|\s) and ($|\s) when used
TEAM_NICKNAMES_REGEX = {
        "New England Patriots":["pat('){0,1}s"],
        "Philadelphia Eagles":["iggle('){0,1}s"],
        "Minnesota Vikings":["vike('){0,1}s"],
        "Green Bay Packers":["pack"],
        "Seattle Seahawks":["hawk('){0,1}s", "legion.{0,1}of.{0,1}boom"],
        "Denver Broncos":["bronc('){0,1}s"],
        "Dallas Cowboys":["boy('){0,1}s", "america('){0,1}s.{0,1}team"],
        "Carolina Panthers":["cardiac.{0,1}cat('){0,1}s"],
        "San Francisco 49ers":["niner('){0,1}s"],
        "Pittsburgh Steelers":["black.{0,1}(and|&).{0,1}gold"],
        "New York Giants":["big.{0,1}blue", "g.{0,1}men", "jint('){0,1}s"],
        "Chicago Bears":["monsters.*midway"],
        "Oakland Raiders":["silver.{0,1}(and|&).{0,1}black", "raidah('){0,1}s"],
        "Baltimore Ravens":[],
        "Detroit Lions":["lie.{0,1}down('){0,1}s", "silver.{0,1}rush"],
        "Houston Texans":[],
        "Washington Redskins":["skin('){0,1}s"],
        "Indianapolis Colts":["dolt('){0,1}s"],
        "San Diego Chargers":["bolt('){0,1}s"],
        "Cleveland Browns":["dawg('){0,1}s", "dawg.{0,1}pound"],
        "New Orleans Saints":[],
        "New York Jets":["gang.{0,1}green"],
        "Atlanta Falcons":["dirty.{0,1}bird('){0,1}s"],
        "Cincinnati Bengals":["bungle('){0,1}s"],
        "Miami Dolphins":["fin('){0,1}s"],
        "Arizona Cardinals":[],
        "Kansas City Chiefs":[],
        "Buffalo Bills":[],
        "Tampa Bay Buccaneers":["buc('){0,1}s", "buckie('){0,1}s"],
        "Jacksonville Jaguars":["jag('){0,1}s"],
        "Los Angeles Rams":["lamb('){0,1}s"],
        "Tennessee Titans":["oiler('){0,1}s"]
}


# names of data files of the first month of each reg season
FIRST_MONTH_FNAMES = [
    "RC_2010-09",
    "RC_2011-09",
    "RC_2012-09",
    "RC_2013-09",
    "RC_2014-09",
    "RC_2015-09",
    "RC_2016-09"
]

# names of data files of the 2016-2017 regular season
REG_SEASON_FNAMES = [
    "RC_2016-09",
    "RC_2016-10",
    "RC_2016-11",
    "RC_2016-12",
    "RC_2017-01",
    "RC_2017-02",
]

# the utc times of the starting and ending dates in regular season, +25300s is for 7 hours as PST is -7 GMT
REG_UTC_START = 1473292800 + 25300 # Sep 8th, 2016, 00:00:00 PST
REG_UTC_END = 1483315200 + 25300 # Jan 2nd, 2017, 00:00:00 PST
PLAY_UTC_END = 1486339200 + 25300 # Feb 6th, 2017, 00:00:00 PST

# "we"
WE_WORDS = [
    "we"
]
