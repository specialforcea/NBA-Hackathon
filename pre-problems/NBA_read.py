import pandas as pd
import operator as op

def read_teams(filename):
    '''
    Read first work sheet to get team information
    Return dictionary of {str:bool}
    {"team_name1":True, "team_name2":False} True = is west team, False = is east team
    '''
    with open(filename, 'rb') as inf:
        data = pd.read_excel(inf, sheetname=0, header=0, dtype=str)
    #print(data)
    #print(data['Team_Name'])
    teams = {}
    for row in data.itertuples():
        if row[3] == 'East':
            teams[row[1]] = False
        else:
            teams[row[1]] = True
    #print(len(west_teams))
    #print(len(east_teams))
    return teams

def read_matches(filename, teams):
    '''
    Read second data sheet and process game information
    Return 1) a list of dates for used as lookup table, 2) a list of dicts as everyday's game information, 
        where tuple of team names is key, and 0/1 as value means home team wins/away team wins
    1): ["2016/10/25", "2016/10/26"....]
    2): [{("Home_team_name", "Away_team_name"):0, ("Home_team_name", "Away_team_name"):1}, {...}...]
    '''
    with open(filename, 'rb') as inf:
        data = pd.read_excel(inf, sheetname=1, header=0, dtype=object)
    #print(data['Date'][0].strftime('%Y/%m/%d'))
    data['Date'] = data['Date'].apply(lambda x: x.strftime('%Y/%m/%d'))
    #print(data['Date'][0])
    dates = []
    matches = []
    matches_of_day = {}
    for row in data.itertuples():
        if row[1] not in dates:
            if len(matches_of_day) > 0:
                matches.append(matches_of_day)
            dates.append(row[1])
            matches_of_day = {}
        hometeam = row[2]
        awayteam = row[3]
        winner = 0 if row[6] == 'Home' else 1
        matches_of_day[(hometeam, awayteam)] = winner
    if len(matches_of_day) > 0:
        matches.append(matches_of_day)
    #print(len(dates))
    #print(len(matches))
    return dates, matches

def cal_scores(teams, matches):
    '''
    Calculate each team's daily number of wins (accumulative)
    Return west_team_scores, east_team_scores 
    dictionary, where keys are team names, and values are list of accumulative number of wins for that team
    {"Team_name":[0,1,2,2...], "Team_name":[0,0,1,2,3...]}
    '''
    days = len(matches)
    score_board_west = {}
    score_board_east = {}

    for team in teams:
        if teams[team]:
            score_board_west[team] = [(0,0)]
        else:
            score_board_east[team] = [(0,0)]
    
    for i in range(days):
        winner_teams = []
        loser_teams = []
        for match in matches[i]:
            winner_teams.append(match[matches[i][match]])
            loser_teams.append(match[1 - matches[i][match]])
        for team in teams:
            if team in winner_teams:
                if teams[team]:
                    score_board_west[team].append((score_board_west[team][-1][0] + 1, score_board_west[team][-1][1]))
                else:
                    score_board_east[team].append((score_board_east[team][-1][0] + 1, score_board_east[team][-1][1]))
            elif team in loser_teams:
                if teams[team]:
                    score_board_west[team].append((score_board_west[team][-1][0], score_board_west[team][-1][1] + 1))
                else:
                    score_board_east[team].append((score_board_east[team][-1][0], score_board_east[team][-1][1] + 1))
            else:
                if teams[team]:
                    score_board_west[team].append(score_board_west[team][-1])
                else:
                    score_board_east[team].append(score_board_east[team][-1])

    for team in teams:
        if teams[team]:
            score_board_west[team] = score_board_west[team][1:]
        else:
            score_board_east[team] = score_board_east[team][1:]

    #print("Len of scores = {}".format(len(score_board_east['Toronto Raptors'])))
    return score_board_west, score_board_east

def cal_rank(teams, west_team_scores, east_team_scores):
    '''
    Calculate each team's daily ranking
    Same score will result tie ranking
    Return a list of dicts contains each team's daily rank
    [{"Team_name":rank, "Team_name":rank...},{}....]
    '''
    days = len(matches)
    #print("Days={}".format(days))
    daily_rank_board_west = []
    daily_rank_board_east = []

    score_board_west = {}
    score_board_east = {}
    for team in teams:
        if teams[team]:
            score_board_west[team] = 0
        else:
            score_board_east[team] = 0
    
    for i in range(days):
        '''for match in matches[i]:
            winner_team = match[matches[i][match]]
            if teams[winner_team]:
                score_board_west[winner_team] += 1
            else:
                score_board_east[winner_team] += 1'''
        for team in teams:
            if teams[team]:
                score_board_west[team] = west_team_scores[team][i][0] - west_team_scores[team][i][1]
            else:
                score_board_east[team] = east_team_scores[team][i][0] - east_team_scores[team][i][1]
        sorted_west_scores = sorted(score_board_west.items(), key=op.itemgetter(1), reverse=True)
        sorted_east_scores = sorted(score_board_east.items(), key=op.itemgetter(1), reverse=True)
        
        rank_board_west = {}
        rank_board_east = {}

        last_score = -1
        rank = 0
        count = 0
        for team, score in sorted_west_scores:
            count += 1
            if score != last_score:
                rank = count
            last_score = score
            rank_board_west[team] = rank

        last_score = -1
        rank = 0
        count = 0
        for team, score in sorted_east_scores:
            count += 1
            if score != last_score:
                rank = count
            last_score = score
            rank_board_east[team] = rank

        daily_rank_board_west.append(rank_board_west)
        daily_rank_board_east.append(rank_board_east)

    return daily_rank_board_west, daily_rank_board_east



teams = read_teams('NBA.xlsx')
dates, matches = read_matches('NBA.xlsx', teams)
# print(dates)
# print(matches)
daily_scores_west, daily_scores_east = cal_scores(teams, matches)
# print(daily_scores_west)
# print(daily_scores_east)
daily_rank_board_west, daily_rank_board_east = cal_rank(teams, daily_scores_west, daily_scores_east)
# print(daily_rank_board_west)
# print(daily_rank_board_east)