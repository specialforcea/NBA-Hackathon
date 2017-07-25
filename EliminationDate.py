import numpy as np 
import pandas as pd 
from NBA_read import * 



def EliminationDate(team,dates,matches,daily_scores_east,daily_scores_west,daily_rank_board_east,daily_rank_board_west):
	if teams[team] == True:
		return Find_EDate(team,dates,matches,daily_scores_west,daily_rank_board_west)
	else:
		return Find_EDate(team,dates,matches,daily_scores_east,daily_rank_board_east)


def Find_EDate(team,dates,matches,daily_scores,daily_rank_board):
	Num_of_dates = len(dates)
	if daily_rank_board[Num_of_dates-1][team] < 9:
		return 'Playoff'
	else:
		for i in range(1,Num_of_dates):
			date = dates[Num_of_dates-i]
			BF_Rank = Best_Final_Rank(team,date,dates,matches,daily_scores,daily_rank_board)
			print BF_Rank[team]
			if BF_Rank[team] < 9:
				return date
			elif i == Num_of_dates-1:
				return 'ERROR, No one is eliminated at the beginning'


def Best_Final_Rank(team,date,dates,matches,daily_scores,daily_rank_board):
	daily_score = {}
	Num_of_date = dates.index(date)
	for team in daily_rank_board[0].keys():
		daily_score[team] = daily_scores[team][Num_of_date-1]


	Daily_Rank = daily_rank_board[Num_of_date-1]
	Best_score = daily_score
	Best_Rank = Daily_Rank
	#print Best_score
	while True:
		if Num_of_date == len(dates):
			break


		daily_match = matches[Num_of_date]
		Best_Rank, Best_score = Best_daily_Rank(team,teams,Best_Rank,Best_score,daily_match)
		Num_of_date = Num_of_date + 1
		#print Best_Rank
	return Best_Rank


def Best_daily_Rank(team,teams,Best_Rank,Best_score,daily_match):
	conference = teams[team]
	for match in daily_match.keys():
		if match[0] == team:
			Best_score[match[0]] = (Best_score[match[0]][0] + 1, Best_score[match[0]][1] )
			if teams[match[1]] == conference:
				Best_score[match[1]] = (Best_score[match[1]][0], Best_score[match[1]][1] + 1)
		elif match[1] == team:
			Best_score[match[1]] = (Best_score[match[1]][0] + 1, Best_score[match[1]][1] )
			if teams[match[0]] == conference:
				Best_score[match[0]] = (Best_score[match[0]][0], Best_score[match[0]][1] + 1)
			
		elif teams[match[0]] == conference and teams[match[1]] == conference:
			r1 = Best_Rank[match[0]]
			r2 = Best_Rank[match[1]]
			r = Best_Rank[team]
			if r1 < r2:
				if r1 < r < r2 :
					Best_score[match[1]] = (Best_score[match[1]][0] + 1, Best_score[match[1]][1] )
					Best_score[match[0]] = (Best_score[match[0]][0], Best_score[match[0]][1] + 1)
				elif r < r1 < r2 :
					Best_score[match[1]] = (Best_score[match[1]][0] + 1, Best_score[match[1]][1] )
					Best_score[match[0]] = (Best_score[match[0]][0], Best_score[match[0]][1] + 1)
				elif r1 < r2 < r :
					Best_score[match[0]] = (Best_score[match[0]][0] + 1, Best_score[match[0]][1] )
					Best_score[match[1]] = (Best_score[match[1]][0], Best_score[match[1]][1] + 1)

			elif r2 < r1:
				if r2 < r < r1 :
					Best_score[match[0]] = (Best_score[match[0]][0] + 1, Best_score[match[0]][1] )
					Best_score[match[1]] = (Best_score[match[1]][0], Best_score[match[1]][1] + 1)
				elif r < r2 < r1:
					Best_score[match[0]] = (Best_score[match[0]][0] + 1, Best_score[match[0]][1] )
					Best_score[match[1]] = (Best_score[match[1]][0], Best_score[match[1]][1] + 1)
				elif r2 < r1 < r :
					Best_score[match[1]] = (Best_score[match[1]][0] + 1, Best_score[match[1]][1] )
					Best_score[match[0]] = (Best_score[match[0]][0], Best_score[match[0]][1] + 1)

			elif r1 == r2:
				if Best_score[match[0]][0] < Best_score[match[1]][0]:
					Best_score[match[0]] = (Best_score[match[0]][0] + 1, Best_score[match[0]][1] )
					Best_score[match[1]] = (Best_score[match[1]][0], Best_score[match[1]][1] + 1)
				else:
					Best_score[match[1]] = (Best_score[match[1]][0] + 1, Best_score[match[1]][1] )
					Best_score[match[0]] = (Best_score[match[0]][0], Best_score[match[0]][1] + 1)

		elif teams[match[0]] == conference and teams[match[1]] != conference:
			
			Best_score[match[0]] = (Best_score[match[0]][0], Best_score[match[0]][1] + 1)
		elif teams[match[1]] == conference and teams[match[0]] != conference:
			
			Best_score[match[1]] = (Best_score[match[1]][0], Best_score[match[1]][1] + 1)
			        
			

	Best_Rank = Rank(Best_score)
	return Best_Rank,Best_score

def Rank(Best_score):
	net_win = {}
	Best_Rank = {}
	net_win_ls = []
	dup = []
	for team in Best_score.keys():
		net_win[team] = Best_score[team][0] - Best_score[team][1]
		if net_win[team] in net_win_ls:
			dup.append(net_win[team])
		else:
			net_win_ls.append(net_win[team])

	sorted_ls = sorted(net_win_ls,reverse = True)
	for team in Best_score.keys():
		Best_Rank[team] = sorted_ls.index(net_win[team]) + 1
	#print sorted_ls
	for team in Best_Rank.keys():
		n = 0
		for dups in dup:
			if net_win[team] < dups:
				n = n + 1
		Best_Rank[team] = Best_Rank[team] + n
	#print Best_Rank
	return Best_Rank



print (EliminationDate('Brooklyn Nets',dates,matches,daily_scores_east,daily_scores_west,daily_rank_board_east,daily_rank_board_west))



