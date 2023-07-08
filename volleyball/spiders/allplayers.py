import scrapy
from volleyball.items import VolleyballPlayer


class AllPlayersSpider(scrapy.Spider):
    name = "players"
    allowed_domains = ["bvbinfo.com"]
    # start_urls = ["http://bvbinfo.com/"]
    custom_settings = {
        "FEEDS": {
            "./data/allplayers.csv": {
                "format": "csv",
                "item_classes": [VolleyballPlayer],
                "fields": [
                    "player_id",
                    "player_name",
                    "player_country",
                    "DOB",
                    "height_in",
                    "home_town",
                    "resides",
                    "total_first",
                    "total_second",
                    "total_third",
                    "total_forth",
                    "total_played",
                    "total_points",
                    "podium%",
                ],
            }
        }
    }

    # explame "http://www.bvbinfo.com/Player.asp?ID=11750"
    def start_requests(self):
        # Real range of players codes are in between 1 and to 22454 on July 5th. 2023
        player_codes = [code for code in range(1, 22455)]

        # only players in FIVB since 2018 to 2022
        # with open("player_codes.txt", "r") as file:
        #     for line in file:
        #         code = line.strip()
        #         player_codes.append(code)

        # player_codes = [1, 11750, 189, 22454]
        for code in player_codes:
            url = f"http://www.bvbinfo.com/Player.asp?ID={code}"
            print("URL: ", url)
            yield scrapy.Request(url=url, callback=self.parse, meta={"player_id": code})

    def parse(self, response):
        player = VolleyballPlayer()
        player["player_id"] = response.request.meta["player_id"]
        player["player_name"] = (
            response.xpath("//td[@class='clsPlayerName']/text()").get().strip()
        )

        # country_tag = response.xpath("//td[@class='clsPlayerCountry']/text()")

        player["player_country"] = (
            response.xpath("//td[@class='clsPlayerCountry']/text()").get().strip()
        )

        ##Player info is blue table
        ## path_to_info_table_rows = '//td[@class='clsPlayerHeader' and text()='Vital Statistics']/../../tr[3]//table/tbody//table'
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
        # getting all rows with attribute

        if response.xpath(
            "//td[@class='clsPlayerHeader' and text()='Career Summary']/../following-sibling::tr/td/b[text()='Overall']"
        ):
            overall_total_row = response.xpath(
                "//td[@class='clsPlayerHeader' and text()='Career Summary']/../following-sibling::tr/td/b[text()='Overall']/../../following-sibling::tr [@class='clsPlayerDataTotal']"
            )
            player_totlas = overall_total_row.xpath("./td")

            #  we have an array of all dt elements in . each can contain 1 or two pieces of text, we only need first
            print("Total overall elements ", len(player_totlas))

            player["total_played"] = int(player_totlas[2].xpath("./text()").get())
            player["total_first"] = int(player_totlas[3].xpath("./text()").get())
            player["total_second"] = int(player_totlas[4].xpath("./text()").get())
            player["total_third"] = int(player_totlas[5].xpath("./text()").get())
            player["total_forth"] = int(player_totlas[6].xpath("./text()").get())

            for i in range(7, len(player_totlas)):
                print(player_totlas[i].xpath("./text()").get())
                dt = player_totlas[i].xpath("./text()").get()
                if "$" in dt:
                    player["total_points"] = (
                        player_totlas[i + 1]
                        .xpath("./text()")
                        .get()
                        .replace(",", "")
                        .split(".")[0]
                    )
                    break

        # //td[@class="clsPlayerCategoryHeader"]/../following-sibling::tr[@class="clsPlayerDataTotal"]
        yield (player)
