vergleichswert = 0.000260725 #average points/price value caculated from a 23/24 database
from kickbase_api.kickbase import Kickbase
from kickbase_api.models import player as spieler
import time
import os
from dotenv import load_dotenv
load_dotenv()
kickbase = Kickbase()
user, leagues = kickbase.login(os.getenv('EMAIL'), os.getenv('PASSWORD')) #change the values in a .env file to use the tool

def sortForWert(player):
   return (-player['position'], player['wert']) #function to sort the arrays below

def max_price_change(points, vergleichswert, price):
    return (1 - vergleichswert / (points / price)) * price #calculates the maximum price change so that a player on the market is still 10% above average

def buy_players():
   if kickbase._is_token_valid():
      market = kickbase.market(leagues[0]) #market of the first league you are participating in
      good_players = [] #array to store all players on the market you should buy
      for player in market.players:
         if player.totalPoints != 0:
            wert = player.totalPoints / player.price #calculating points / price ratio
         else:
            wert = 1 #ratio = 1 if the player has never produced any points / was promoted / is a new player in the bundesliga
         if wert >= vergleichswert * 1.1 and wert != 1 and player.totalPoints / player.average_points >= 20 or player.price == 500000 or player.average_points >= 105: #you should buy: 10% over average, at least 20 games played, price at minimum (500k), average points 105+ (top 30 player in the game)
            good_players.append({'spieler': player, 'wert': wert, 'position': player.position})
         
      good_players.sort(key=sortForWert, reverse=True)
      for i in good_players:
         formatted_num = "{:,}".format(int(i['spieler'].price))
         print(f"{i['spieler'].first_name} {i['spieler'].last_name} ({i['spieler'].position.name}): {formatted_num} // Performance: {int((i['wert'] / vergleichswert)  * 100) - 100}% // Preis für 10%: {int(max_price_change(i['spieler'].totalPoints, vergleichswert, i['spieler'].price) + i['spieler'].price)}") #print all the information
      print("\n")

def sell_players():
   if kickbase._is_token_valid():
      bad_players = [] #array to store the players you should sell
      ranking = [] #array to store all players on your team
      for player in kickbase.league_user_players(leagues[0], user): #looping through your team
         if player.totalPoints != 0:
            wert = (player.totalPoints / player.market_value) #calculating points / price ratio
         else:
            wert = 1 #ratio = 1 if the player has never produced any points / was promoted / is a new player in the bundesliga
         ranking.append({'spieler': player, 'wert': wert, 'position': player.position})
         if wert <= vergleichswert - vergleichswert * 0.2 and wert != 1 and player.totalPoints / player.average_points < 30 and player.market_value < 15000000 and player.average_points < 105 or player.status == spieler.PlayerStatus.INJURED: #you should sell: 20% under average, under 30 games played, price < 15 MIO, point average < 105 (not top 30 player), player injured
            bad_players.append({'spieler': player, 'wert': wert, 'position': player.position})

      bad_players.sort(key=sortForWert, reverse=False)
      ranking.sort(key=sortForWert, reverse=True)

      for i in bad_players:
         formatted_num = "{:,}".format(int(i['spieler'].market_value))
         print(f"{i['spieler'].first_name} {i['spieler'].last_name} ({i['spieler'].position.name}): {formatted_num} // Performance: {100 - int((i['wert'] / vergleichswert) * 100)}%") #print all the information

      print("\nRanking:\n")
      for i in ranking:
         formatted_num = "{:,}".format(int(i['spieler'].market_value))
         print(f"{i['spieler'].first_name} {i['spieler'].last_name} ({i['spieler'].position.name}): {formatted_num} // Performance: {int((i['wert'] / vergleichswert) * 100)-100}%") #print ranking of all your players


while (True):

   print("\nDiese Spieler solltest du kaufen:\n")
   buy_players()
   print("Diese Spieler solltest du verkaufen:\n")
   sell_players()
   time.sleep(3600) #if script is running all the time, printing information every hour
