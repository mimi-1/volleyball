import scrapy
import re
from volleyball.items import VolleyballTournament


def extract_id(mystr):
    return mystr.split("=")[-1]


class SeasonsSpider(scrapy.Spider):
    name = "seasons"
    allowed_domains = ["bvbinfo.com"]
    # start_urls = ["http://bvbinfo.com/"]
    custom_settings = {"FEED_URI": "tournaments.csv", "FEED_FORMAT": "csv"}
    player_codes = set()

    # explame "http://www.bvbinfo.com/Season.asp?AssocID=3&Year=2018
    def start_requests(self):
        for year in range(2018, 2023):
            url = f"http://www.bvbinfo.com/Season.asp?AssocID=3&Year={year}"
            # print("URL: ", url)
            yield scrapy.Request(url=url, callback=self.parse, meta={"year": year})

    def parse(self, response):
        year = response.request.meta["year"]
        # print(f"VOLLEYBALL PROCESSING {year} year")
        season_title_dirty = response.xpath(
            '//td[@class="clsSeasonHeader"]/text()'
        ).get()
        season_title = re.sub(r"[\r\n\t]", "", season_title_dirty).strip()
        tournamets_rows_block = response.xpath(
            '//table[3]//tr[@valign="bottom" and @align="center"]'
        )
        print(len(tournamets_rows_block))
        for tournament_row in tournamets_rows_block:
            tournament = VolleyballTournament()
            tournament["season_title"] = season_title
            tournament["year"] = year
            tournament["date"] = tournament_row.xpath("./td[1]/text()").get()
            tournament_id = tournament_row.xpath("./td[2]/a/@href").get()
            # tournament["tournament_id"] = tournament_id[-4:]
            tournament["tournament_id"] = extract_id(tournament_id)
            print("Tournament_id = ", tournament["tournament_id"])
            tournament["city"] = tournament_row.xpath("./td[2]/a/text()").get()
            tournament["country"] = tournament_row.xpath("./td[2]/text()").get()[1:]
            tournament["gender"] = tournament_row.xpath("./td[3]/text()").get()
            print("GENDER", tournament["gender"])
            for i in range(4, 8):
                # <a href="Player.asp?ID=11750">Jan Pokersnik</a>
                player1_href = tournament_row.xpath(f"./td[{i}]/a[1]/@href").get()
                tournament[f"p{i-3}_player_1_id"] = extract_id(player1_href)
                tournament[f"p{i-3}_player_1_name"] = tournament_row.xpath(
                    f"./td[{i}]/a[1]/text()"
                ).get()
                self.player_codes.add(tournament[f"p{i-3}_player_1_id"])
                player2_href = tournament_row.xpath(f"./td[{i}]/a[2]/@href").get()
                tournament[f"p{i-3}_player_2_id"] = extract_id(player2_href)
                self.player_codes.add(tournament[f"p{i-3}_player_2_id"])
                tournament[f"p{i-3}_player_2_name"] = tournament_row.xpath(
                    f"./td[{i}]/a[2]/text()"
                ).get()

            yield (tournament)

    def closed(self, reason):
        # Save the player codes list to a file
        with open("player_codes.txt", "w") as file:
            file.write("\n".join(self.player_codes))
