# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 12:20:30 2019

@author: lramsier
"""
from pandas import Series, DataFrame
import pandas as pd
from numpy.random import randn
import numpy as np

#function to make separating output easier
def top_lines():
    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")

#read in the data
artists_df = pd.read_table('artists.dat', sep="\t") 
ua_df = pd.read_table('user_artists.dat', sep="\t")

user_artists_df = pd.read_table('user_artists.dat', encoding="utf-8", sep="\t", index_col=['userID', 'artistID'])


#get the artist names
artist_names = artists_df.name.values
artist_ids = artists_df.id.values
artist_names_series = Series(artist_names, index=artist_ids)

# Question 1

# references
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html#pandas.DataFrame.groupby
# https://pandas.pydata.org/pandas-docs/stable/reference/frame.html#indexing-iteration

#get the top ten artistIDs grouped by the sum of the plays
top_ten_artists = ua_df[['artistID','weight']].groupby(['artistID']).sum().sort_values(by='weight', ascending=False).head(10)
top_ten_artist_ids = top_ten_artists.index

#get values in a list of lists
top_ten_plays = top_ten_artists.get_values()

# print answer
top_lines()
print("1. Who are the top artists?")
for num in range(0,10):
    print(artist_names_series[top_ten_artist_ids[num]], "(", top_ten_artist_ids[num], ")", top_ten_plays[num][0])

# Question 2

# reference
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.count.html

# get top ten artist ids and count
top_ten_artists_listeners = ua_df.groupby(['artistID']).count().sort_values(by='userID', ascending=False)

#get artist ids
top_ten_artists_listeners_ids = top_ten_artists_listeners.index

#get get values for top ten listeners in list of lists
top_ten_listeners = top_ten_artists_listeners.get_values()

#print answer
top_lines()
print("2. What artists have the most listeners?")
for num in range(0,10):
    print(artist_names_series[top_ten_artists_listeners_ids[num]], " (", top_ten_artists_listeners_ids[num], ") ", top_ten_listeners[num][0] )

# get top ten users with most songs played
top_ten_users = ua_df[['userID', 'weight']].groupby(['userID']).sum().sort_values(by='weight', ascending=False).head(10)

# print answer
top_lines()
print("3. Who are the top users?")
for num in range(0,10):
    userid = top_ten_users.index[num]
    print(userid, top_ten_users.weight[userid])
    
# Question 4

user_artists_df['weight'].groupby('artistID').sum()
# x = user_artists_df.groupby('artistID').count().sort_values(by='artistID',ascending=False)
# y = user_artists_df.groupby('artistID').sum().sort_values(by='artistID', ascending=False)

# get data
artist_total_listeners = user_artists_df.groupby('artistID').count()
artist_total_plays = user_artists_df.groupby('artistID').sum()

# average plays by total/# of listeners
average_plays = (artist_total_plays/artist_total_listeners).sort_values(by='weight', ascending=False)

# merge dataframes to aggregate information
avg_plays_merge = pd.merge(artists_df, average_plays, left_on='id', right_index=True)
avg_plays_merge = avg_plays_merge[['name','id','weight']].sort_values(by='weight',ascending=False)
avg_plays_merge = pd.merge(avg_plays_merge, artist_total_listeners, left_on='id', right_index=True)
avg_plays_merge = pd.merge(avg_plays_merge, artist_total_plays, left_on='id', right_index=True)
output_avg_plays = avg_plays_merge.head(10)

# print answer
top_lines()
print("4. What artists have the highest average number of plays per listener?")
index_list = output_avg_plays.index
for index in index_list:
    print(output_avg_plays['name'][index], "(", output_avg_plays['id'][index], ")", "has been played", output_avg_plays['weight'][index], "times by", output_avg_plays['weight_y'][index], "user(s) for an average of",output_avg_plays['weight_x'][index], "plays per user.")
    
# Question 5

# Get all the artists with more than 50 listeners
avg_plays_merge_fifty = avg_plays_merge[avg_plays_merge['weight_y']>49.0].sort_values(by='weight_x', ascending=False)

# Get the top 10
output_avg_plays_fifty = avg_plays_merge_fifty.head(10)
top_lines()
print("4. What artists have the highest average number of plays per listener?")
index_list = output_avg_plays_fifty.index
for index in index_list:
    print(output_avg_plays_fifty['name'][index], "(", output_avg_plays_fifty['id'][index], ")", "has been played", output_avg_plays_fifty['weight'][index], "times by", output_avg_plays_fifty['weight_y'][index], "user(s) for an average of",output_avg_plays_fifty['weight_x'][index], "plays per user.")
    
# Question 6

# read in friends data
user_friends_df = pd.read_table('user_friends.dat', sep="\t")

# user_friend_count = user_friends_df.groupby('userID').count()

# get # of songs each user has played
user_total_plays = user_artists_df.sum(level=0)

# merge with friends data
user_friends = pd.merge(user_total_plays, user_friends_df, left_index=True, right_on='userID')

# get number of friends each user has
user_friends_count = user_friends[['friendID','userID']].groupby('userID').count()

# merge number of friends data with total number of songs each user has played
user_friends = pd.merge(user_total_plays, user_friends_count, left_index=True, right_index=True)

# get users in group based on num of friends
user_friends_five_or_more = user_friends[user_friends_count['friendID'] >= 5]
user_friends_less_than_five = user_friends[user_friends_count['friendID'] < 5] 

# get the sum of all song plays for each group
user_friends_five_or_more_total = user_friends_five_or_more.sum()
user_friends_less_than_five_total = user_friends_less_than_five.sum()

# get the total num of users in each group
user_friends_five_or_more_count = user_friends_five_or_more.count()
user_friends_less_than_five_count = user_friends_less_than_five.count()

# calculate averge
avg_five_or_more = user_friends_five_or_more_total['weight']/user_friends_five_or_more_count['friendID']
avg_less_than_five = user_friends_less_than_five_total['weight']/user_friends_less_than_five_count['friendID']

# print output
top_lines()
print("6. Do users with five or more friends listen to more songs?")
print("Users with five or more friends have played an average of", avg_five_or_more, "songs.")
print("Users with less than five friends have played an average of", avg_less_than_five, "songs.")

# Question 7

def artist_sim(aid1, aid2):    
    # get the users who have listened to artist 1 and artist 2 and put them into sets
    artist_listeners = user_artists_df.reset_index().groupby(['artistID','userID']).count() 
    aid1_listeners = set(artist_listeners.loc[aid1].index)
    aid2_listeners = set(artist_listeners.loc[aid2].index)
    
    # get the num of items in the intersection of aid1 and aid2
    intersection_listeners = len(aid1_listeners.intersection(aid2_listeners))
    
    # get the num of items in the union of aid1 and aid2
    union_listeners = len(aid1_listeners.union(aid2_listeners))
    
    # divide the intersection num by the union num
    jaccard_index = intersection_listeners/union_listeners
    
    # print the Jaccard Index
    a1_name = artist_names[aid1]
    a2_name = artist_names[aid2]
    print("The Jaccard Index for", a1_name, "and", a2_name, "is:", jaccard_index)
    
# output
top_lines()
print("7. How similar are two artists?")
artist_sim(735,562)
artist_sim(735,89)
artist_sim(735,289)
artist_sim(89,289)
artist_sim(89,67)
artist_sim(67,735)

# Question 8

# read in the data
user_tags_df = pd.read_table('user_taggedartists.dat', encoding="utf-8", sep="\t", index_col=['artistID', 'year', 'month'])
month_names=['January','February','March','April','May','June','July','August','September','October','November','December']

# get the top ten artists in terms of tags
tag_count = user_tags_df['tagID'].groupby('artistID').count().sort_values(ascending=False).head(10)
artists = tag_count.index

# clean the data
x = user_tags_df.reset_index()
y = x[['year','month','artistID','tagID']].groupby(['year','month','artistID']).count()
z = y.reset_index()
z = z[z['year'] >= 2005]
years = set(z.year)
months = set(z.month)

# print output
top_lines()
print("8. Analysis of top tagged artists")

# iterate through artists
for artist in artists:
    # set/reset variables
    first_month = 0
    count = 0
    # iterate through years and months
    for ye in years:
        for m in months:
            
            #get top ten for the month
            monthly10 = y.loc[ye].loc[m].sort_values(by='tagID', ascending=False).head(10)
            
            # create list of top ten and check if artist is in list
            artists10 = monthly10.index
            # save first month for artist
            if(artist in artists10 and first_month == 0):
                first_month = [ye,m]
            
            # add to count
            if(artist in artists10):
                count += 1
    # adjust index to get right month name
    month = first_month[1] - 1

    # print output for artist
    print(artist_names_series[artist], "(", artist, "): num tags =", tag_count[artist])
    print("first month in top 10 =", month_names[month], first_month[0])
    print("months in top 10 =", count, "\n")