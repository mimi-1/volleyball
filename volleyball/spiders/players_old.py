# import scrapy
# from volleyball.items import VolleyballPlayer


# class PlayersSpider(scrapy.Spider):
#     name = "players"
#     allowed_domains = ["bvbinfo.com"]
#     # start_urls = ["http://bvbinfo.com/"]
#     custom_settings = {"FEED_URI": "players.csv", "FEED_FORMAT": "csv"}

#     # explame "http://www.bvbinfo.com/Player.asp?ID=11750"
#     def start_requests(self):
#         player_codes = []
#         with open("player_codes.txt", "r") as file:
#             for line in file:
#                 code = line.strip()
#                 player_codes.append(code)

#         for code in player_codes:
#             url = f"http://www.bvbinfo.com/Player.asp?ID={code}"
#             print("URL: ", url)
#             yield scrapy.Request(url=url, callback=self.parse, meta={"player_id": code})

#     def parse(self, response):
#         player = VolleyballPlayer()
#         player["player_id"] = response.request.meta["player_id"]
#         player["player_name"] = response.xpath(
#             "//td[@class='clsPlayerName']/text()"
#         ).get()
#         country_tag = response.xpath("//td[@class='clsPlayerCountry']/text()")
#         player["player_country"] = country_tag.get()

#         playerData = response.xpath("//td[@class='clsPlayerData']/text()").getall()

#         player["DOB"] = playerData[0]
#         player["home_town"] = playerData[1]
#         player["resides"] = playerData[2]
#         player["height_in"] = playerData[3]
#         # total stats for international plays

#         player_totlas = response.xpath("//tr[@class='clsPlayerDataTotal'][1]/td")
#         # print(player_totlas)
#         player["total_played"] = player_totlas[2].xpath("./text()").get()

#         player["total_first"] = player_totlas[3].xpath("./text()").get()
#         player["total_second"] = player_totlas[4].xpath("./text()").get()
#         player["total_third"] = player_totlas[5].xpath("./text()").get()
#         player["total_forth"] = player_totlas[6].xpath("./text()").get()
#         player["total_points"] = player_totlas[11].xpath("./text()").get()

#         yield (player)
