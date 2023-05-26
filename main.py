import csv
import os
import sys
from enum import Enum
from tournament import *
import pypair
import networkx as nx


if __name__ == '__main__':
    #sys.argv[1]
    with open(sys.argv[1], encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        players = {}
        dropList = ['Gratka', 'Bober', 'Leszy']
        reader.__next__()
        for row in reader:
            if row[1] != '':
                # print(row)
                # print(row[1])
                if not row[1] in players:
                    players[row[1]] = (int(row[6]), [row[2]])
                else:
                    players[row[1]] = (players[row[1]][0] + int(row[6]), players[row[1]][1])
                    players[row[1]][1].append(row[2])

        ranking = sorted(players, key=players.get, reverse=True)

        for drop in dropList:
            ranking.remove(drop)

        if len(ranking) % 2 == 1:
            ranking.append('BYE')
            players.update({"BYE": (0, ['Elromir', 'Basior', 'Magda Ciężka'])})

        bracketGraph = nx.Graph()
        for player in ranking:
            bracketGraph.add_node(player)

        for player in ranking:
            # print(player, players[player])
            for opponent in ranking:
                if opponent not in players[player][1] and player not in players[opponent][1] and player != opponent:
                    bracketGraph.add_edge(player, opponent, weight=(abs(players[player][0] - players[opponent][0])))

        pairings = dict(nx.min_weight_matching(bracketGraph))

        i = 1
        with open('result.txt', 'w') as result:
            for pair in pairings:
                print(pair, pairings[pair])
                line = str(i.__str__() + ". " + pair + " - " + pairings[pair] + "\n")
                result.write(line)
                i += 1

            for pair in pairings:
                line = str(pair + "," + pairings[pair] + "\n")
                result.write(line)
                i += 1

        # for x in sorted(players, key=players.get, reverse=True):
        #     print(x, players[x])
