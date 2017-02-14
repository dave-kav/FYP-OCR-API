# -*- coding: utf-8 -*-
"""
Author:         Dave Kavanagh
                R00013469
                david.j.kavanagh@mycit.ie

Date:           14/02/2017

Description:    File to create tables necessary in db

© Dave Kavanagh, 2017
"""

import pymysql

def db():
    try:
        connection = pymysql.connect(host='fyp-db.cz6vzodupwnl.eu-west-1.rds.amazonaws.com',
                              user='dkav87',
                              passwd='123456789',
                              db='betting_db',
                              port=3306)
    except:
        print "unable to connect"
        exit(1)

    user_sql = 'CREATE TABLE Users (Username VARCHAR(24), Password VARCHAR(8), Name VARCHAR(40), DOB DATE, Credit FLOAT );'
    bet_sql  = 'CREATE TABLE Bets (Bet_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, Selection VARCHAR(40), Race_id INT, Stake FLOAT,' \
               'Status ENUM("Winner", "Loser"), Tranlated BOOL, Manual_tranlated BOOL, Online_bet BOOL, Winnings FLOAT, Image VARCHAR(255) );'
    race_sql = 'CREATE TABLE Races (Race_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY , Time DATETIME, Racetrack VARCHAR(25));'
    horse_sql= 'CREATE TABLE Horses (Name VARCHAR(25), Race_id INT, odds_numerator INT, odds_denominator INT);'
    api_sql  = 'CREATE TABLE Api_keys(Api_key VARCHAR(255), Email VARCHAR(100));'
    sql_dict = {'Users': user_sql,
                'Bets': bet_sql,
                'Races': race_sql,
                'Horses': horse_sql,
                'Api_keys': api_sql}

    try:
        with connection.cursor() as cursor:
            for query in sql_dict:
                cursor.execute(sql_dict[query])
                print 'Table added:', query
    except Exception as e:
        print "Create table failed:", e

if __name__ == "__main__":
    db()