STAT_TYPE_MAPPINGS = {
    "passing": ["name", "pass_yds", "yds_att", "att", "cmp", "cmp%", "td", "int", "rate", "1st", "1st%", "20+", "40+", "long", "sck", "scky"],
    "rushing": ["name", "rush_yds", "att", "td", "20+", "40+", "long", "rush_1st", "rush_1st%", "rush_fum"],
    "receiving": ["name", "rec", "yds", "td", "20+", "40+", "lng", "rec_1st", "1st%", "rec_fum", "rec_yac/r", "tgts"],
    "field-goals": ["name", "fgm", "fga", "fg_percent", "fg_1_19", "fg_20_29", "fg_30_39", "fg_40_49", "fg_50_59", "fg_60_plus", "fg_long", "fg_blocked"]
}

POSITION_ABBREV = {
    "passing": "passing",
    "rushing": "rushing",        
    "receiving": "receiving",
    "field-goals": "kicking"    
}


STAT_SORT_KEYS = {
    "passing": "passingyards",
    "rushing": "rushingyards",
    "receiving": "receivingreceptions",
    "field-goals": "kickingfgmade"
}