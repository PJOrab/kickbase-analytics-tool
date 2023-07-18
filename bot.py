# with open("kickbase_data.txt", "r") as file:
#     lines = file.readlines()

#     punkte = 0
#     marktwert = 0
#     spiele = 0

#     for line in lines:
#         data = line.strip().split(";")
#         punkte += float(data[8])
#         marktwert += float(data[5].replace(".", "").replace("€", ""))
#         spiele += int(data[6])

# punkte_average = punkte / len(lines)
# marktwert_average = marktwert / len(lines)
# average_ratio = (punkte / marktwert) * (spiele / len(lines)) * 1.5

# print(f'Punkte Average: {punkte_average}\nMarktwert Average: {marktwert_average}\nRatio: {average_ratio}')

vergleichswert = 0.000260725
from kickbase_api.kickbase import Kickbase
from kickbase_api.models import player as spieler
import time
kickbase = Kickbase()
user, leagues = kickbase.login("pjbaro@web.de", "2013kPuLzsm")

gk_player_count = 0
def_player_count = 0
mid_player_count = 0
attack_player_count = 0

def sortForWert(player):
   return player['wert']

def buy_players():
   if kickbase._is_token_valid():
      market = kickbase.market(leagues[0])
      good_players = []
      for player in market.players:
         if player.totalPoints != 0:
            wert = player.totalPoints / player.market_value
         else:
            wert = 1
         if wert >= vergleichswert * 1.1 and wert != 1 and player.totalPoints / player.average_points >= 20 or player.price == 500000:
            good_players.append({'spieler': player, 'wert': wert})
         
      good_players.sort(key=sortForWert, reverse=True)
      for i in good_players:
         #print(f"{i['spieler'].first_name} {i['spieler'].last_name}: {i['wert']}")
         kickbase.make_offer(i['spieler'].market_value * 1.01, i['spieler'], leagues[0])

def sell_players():
   if kickbase._is_token_valid():
      bad_players = []
      for player in kickbase.league_user_players(leagues[0], user):
         if player.totalPoints != 0:
            wert = (player.totalPoints / player.market_value)
         else:
            wert = 1
         if wert <= vergleichswert - vergleichswert * 0.2 and wert != 1 and player.totalPoints / player.average_points < 20 and player.market_value < 15000000 and player.average_points < 105:
            if player.position == spieler.PlayerPosition.GOAL_KEEPER and gk_player_count > 1:
               bad_players.append({'spieler': player, 'wert': wert})
            elif player.position == spieler.PlayerPosition.DEFENDER and def_player_count > 3:
               bad_players.append({'spieler': player, 'wert': wert})
            elif player.position == spieler.PlayerPosition.MIDFIELDER and mid_player_count > 4:
               bad_players.append({'spieler': player, 'wert': wert})
            elif player.position == spieler.PlayerPosition.FORWARD and attack_player_count > 3:
               bad_players.append({'spieler': player, 'wert': wert})

      bad_players.sort(key=sortForWert, reverse=False)
      for i in bad_players:
         print(f"{i['spieler'].first_name} {i['spieler'].last_name}: {i['wert']}")
         #kickbase.add_to_market(i['spieler'].market_value * 1.03, i['spieler'], leagues[0])

# def line_up_players():
#    if kickbase._is_token_valid():
#       players_in_team = []
#       line_up = []
#       gk_counter = 0
#       def_counter = 0
#       mid_counter = 0
#       attack_counter = 0
#       counter = 0
#       for player in kickbase.league_user_players(leagues[0], user):
#          points = player.average_points
#          players_in_team.append({'spieler': player, 'punkte': points})
#       players_in_team.sort(key=sortForWert, reverse=True)
#       for i in players_in_team:
#          if i['spieler'].position == player.position.GOAL_KEEPER and gk_counter < 1 and counter < 11:
#             line_up.append(i['spieler'])
#             gk_counter += 1
#             counter += 1
#          if i['spieler'].position == player.position.DEFENDER and def_counter < 3 and counter < 11:
#             line_up.append(i['spieler'])
#             def_counter += 1
#             counter += 1
#          if i['spieler'].position == player.position.MIDFIELDER and def_counter < 4 and counter < 11:
#             line_up.append(i['spieler'])
#             mid_counter += 1
#             counter += 1
#          if i['spieler'].position == player.position.FORWARD and attack_counter < 3 and counter < 11:
#             line_up.append(i['spieler'])
#             attack_counter += 1
#             counter += 1
#       my_lineup = lineup.LineUp(line_up)
#       kickbase.set_line_up(my_lineup, leagues[0])
#       kickbase.


while (True):
   for i in kickbase.league_user_players(leagues[0], user):
      if i.position == spieler.PlayerPosition.GOAL_KEEPER:
         gk_player_count += 1
      if i.position == spieler.PlayerPosition.MIDFIELDER:
         mid_player_count += 1
      if i.position == spieler.PlayerPosition.DEFENDER:
         def_player_count += 1
      if i.position == spieler.PlayerPosition.FORWARD:
         attack_player_count += 1

   buy_players()
   sell_players()
   time.sleep(3600)

# line_up_players()