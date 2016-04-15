#!/usr/bin/python

import sys
import csv
from glob import glob #oh my glob
from pprint import pprint

# True if you like the programming giving updates
# False if you want it to be quiet
chatty = False

for i in sys.argv:
    if i == sys.argv[0]:
        continue
    elif i == 'chatty':
        chatty = True
    elif i == 'c':
        chatty = True

def c_print(x):
    print x

def run():
    # grabs all the files and turns it into one dictionary keyed by 
    # {match_num}_{team_num}
    tele1 = {}
    tele2 = {}
    auton = {}

    files = glob('data/*.dbs')
    c_print("Grabbed all " + str(len(files)) + " files")

    team_num = 0
    file_type = 0
    for f_name in files:
        match_num = f_name.split('_')[1]
        team_num = f_name.split('_')[2] 
        file_type = f_name.split('_')[3].split('.')[0]
        data = get_data(open(f_name))
        if file_type == 'Teleop1':
            c_print("Found tele1 match:" + match_num + " by team:" + team_num)
            tele1[match_num + '_' + team_num] = data
        elif file_type == 'Teleop2':
            c_print("Found tele2 match:" + match_num + " by team:" + team_num)
            tele2[match_num + '_' + team_num] = data
        elif file_type == 'Auton':
            c_print("Found auton match:" + match_num + " by team:" + team_num)
            auton[match_num + '_' + team_num] = data
        #print data_dict[team_num + '_' + file_type]
    dic = {} 
    return merge(dic,[tele1,tele2,auton])

def merge(merge_dico,dico_list):
    # Merges dicts
    #c_print("Merging dicts")
    for dico in dico_list:
        for key,value in dico.items():
            if type(value)==type(dict()):
                merge_dico.setdefault(key,dict())
                merge(merge_dico[key],[value])
            else:
                merge_dico[key]=value
    return merge_dico

def get_data(f):
    # Get fed a file, 
    #c_print("Getting data from file: " + str(f))
    return_dict = {}
    for line in f:
        if ":" in line:
            #print "hit"
            #print line
            var = line.split(":")[0]
            #print var
            val_t = line.split(":")[1] 
            val_1 = val_t.replace("(","")
            val = val_1.replace(")","")
            #print val
            return_dict[var] = val.strip()
    #print return_dict
    return return_dict

def csv_test(input_dict):
    c_print("writing to csv now")
    with open('output.csv', 'w') as csvfile:
        c_print("opened and writing to csv")
        fieldnames = ['match','team_num', 'sallyAbility', 'moatScore', 
                'sallyScore', 'HAPC_Drawbridge', 'rampartsScore', 
                'HTC_Drawbridge', 'FieldComments', 'lowbarAbility', 
                'drawbridgeAbility', 'HTC_SallyPort', 'HTC_Moat', 
                'HTC_Cheval-de-Frise', 'roughScore', 'chevalScore', 
                'lowbarScore', 'HAPC_Moat', 'HTC_Ramparts', 'HAPC_RoughTerrain',
                'HTC_Rockwall', 'HTC_RoughTerrain', 'HAPC_Portcullis', 
                'HAPC_Rockwall', 'portScore', 'HTC_Portcullis', 'portAbility',
                'moatAbility', 'HAPC_Ramparts', 'rampartsAbility', 'HTC_LowBar',
                'HAPC_LowBar','chevalAbility', 'rockwallScore', 'roughAbility', 
                'rockwallAbility', 'HAPC_SallyPort', 'HAPC_Cheval-de-Frise', 
                'drawbridgeScore',  'challanged', 'LGF', 'HGS', 'TF', 'PD',
                'HGF', 'LGS', 'scalled', 'TC', 'rockwallCross', 'lowbarCross',
                'sallyReach', 'lowbarReach', 'lowbarStart', 
                'moatReach', 'rampartsCross', 'moatStart', 'rampartsReach', 
                'chevalReach', 'areYouASpyBot', 'portStart', 
                'Shoot in Auton Capibility', 'chevalStart', 'roughStart',
                'moatCross', 'sallyCross', 'startedWithBall', 'drawbridgeCross',
                'chevalCross', 'portReach', 'drawbridgeReach', 'rampartsStart',
                'rockwallReach','drawbridgeStart', 'sallyStart', 'roughCross',
                'roughReach', 'rockwallStart', 'portCross',]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in input_dict:
            match = i.split('_')[0]
            team  = i.split('_')[1]
            input_dict[i]['match']    = match
            input_dict[i]['team_num'] = team
            writer.writerow(input_dict[i])

if __name__ == "__main__":
    csv_test(run())
