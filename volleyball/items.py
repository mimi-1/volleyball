# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VolleyballTournament(scrapy.Item):
    season_title = scrapy.Field()
    year = scrapy.Field()
    date = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    tournament_id = scrapy.Field()
    gender = scrapy.Field()
    p1_player_1_id = scrapy.Field()
    p1_player_1_name = scrapy.Field()
    p1_player_2_id = scrapy.Field()
    p1_player_2_name = scrapy.Field()
    p2_player_1_id = scrapy.Field()
    p2_player_1_name = scrapy.Field()
    p2_player_2_id = scrapy.Field()
    p2_player_2_name = scrapy.Field()
    p3_player_1_id = scrapy.Field()
    p3_player_1_name = scrapy.Field()
    p3_player_2_id = scrapy.Field()
    p3_player_2_name = scrapy.Field()
    p4_player_1_id = scrapy.Field()
    p4_player_1_name = scrapy.Field()
    p4_player_2_id = scrapy.Field()
    p4_player_2_name = scrapy.Field()


class VolleyballPlayer(scrapy.Item):
    player_id = scrapy.Field()
    player_name = scrapy.Field()
    player_country = scrapy.Field()
    DOB = scrapy.Field()
    home_town = scrapy.Field()
    resides = scrapy.Field()
    height_in = scrapy.Field()
    total_played = scrapy.Field()
    total_first = scrapy.Field()
    total_second = scrapy.Field()
    total_third = scrapy.Field()
    total_forth = scrapy.Field()
    total_points = scrapy.Field()
    podium_percent = scrapy.Field()


class VolleyballPlayerRecords(scrapy.Item):  # Only international records
    player_id = scrapy.Field()
    season = scrapy.Field()
    assoc = scrapy.Field()
    points = scrapy.Field()
    rank = scrapy.Field()
    # there are also lots of points here


# ony and only we want records earlier then 2018
class VolleyballPlayerVictory(scrapy.Item):
    player_id = scrapy.Field()
    date = scrapy.Field()
    assoc = scrapy.Field()
    tournament = scrapy.Field()
    tournament_id = scrapy.Field()
    partner_id = scrapy.Field()
    seed = scrapy.Field()
