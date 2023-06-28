import scrapy
from volleyball.items import VolleyballPlayer


class PlayersSpider(scrapy.Spider):
    name = "players"
    allowed_domains = ["bvbinfo.com"]
    # start_urls = ["http://bvbinfo.com/"]
    custom_settings = {"FEED_URI": "players.csv", "FEED_FORMAT": "csv"}

    # explame "http://www.bvbinfo.com/Player.asp?ID=11750"
    def start_requests(self):
        player_codes = []
        with open("player_codes.txt", "r") as file:
            for line in file:
                code = line.strip()
                player_codes.append(code)
        # player_codes = [11750, 1981]
        for code in player_codes:
            url = f"http://www.bvbinfo.com/Player.asp?ID={code}"
            print("URL: ", url)
            yield scrapy.Request(url=url, callback=self.parse, meta={"player_id": code})

    def parse(self, response):
        player = VolleyballPlayer()
        player["player_id"] = response.request.meta["player_id"]
        player["player_name"] = response.xpath(
            "//td[@class='clsPlayerName']/text()"
        ).get()
        country_tag = response.xpath("//td[@class='clsPlayerCountry']/text()")
        player["player_country"] = country_tag.get()

        ##Player info
        path_to_info_table_rows = "//table[@bgcolor='#ccccff']//tr"
        playerData = response.xpath(path_to_info_table_rows)
        for row in playerData:
            row_head = row.xpath("./td[@class='clsPlayerDataLabel']/text()").get()
            # print(row_head)
            row_data = row.xpath("./td[@class='clsPlayerData']/text()").get()
            if row_head == "Birth Date":
                player["DOB"] = row_data
            elif row_head == "Home Town":
                player["home_town"] = row_data
            elif row_head == "Resides":
                player["resides"] = row_data
            elif row_head == "Height":
                player["height_in"] = row_data
        # total stats for international plays
        # print("MARYNA total selecting stats")
        # getting all rows with attribute
        table_headers_selectors = response.xpath(
            "//td[@class='clsPlayerCategoryHeader']"
        )
        for selector in table_headers_selectors:
            header_name = selector.xpath("./text()").get()
            if header_name == "International":
                print(header_name)
                player_totlas = selector.xpath(
                    "../following-sibling::tr[@class='clsPlayerDataTotal']/td"
                )
                player["total_played"] = player_totlas[2].xpath("./text()").get()
                player["total_first"] = player_totlas[3].xpath("./text()").get()
                player["total_second"] = player_totlas[4].xpath("./text()").get()
                player["total_third"] = player_totlas[5].xpath("./text()").get()
                player["total_forth"] = player_totlas[6].xpath("./text()").get()
                player["total_points1"] = player_totlas[11].xpath("./text()").get()
                player["total_points2"] = player_totlas[12].xpath("./text()").get()
                player["total_points3"] = player_totlas[13].xpath("./text()").get()
        # //td[@class="clsPlayerCategoryHeader"]/../following-sibling::tr[@class="clsPlayerDataTotal"]
        yield (player)
