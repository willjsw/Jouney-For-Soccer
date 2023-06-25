from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import json
import base64


def fullFormTeam(team):
    if team == "맨유":
        return "맨체스터 유나이티드"
    else:
        return team
    
def openImageUrl(imgUrl):
    try:
        img = urlopen(imgUrl).read()
        return base64.encodebytes(img) 
    except HTTPError as e:
        code = e.getcode()
        print(code+": impropal image url")
        return base64.b64encode(open("defaultEmblem.png", "rb").read())

        
class MatchData:
    def __init__(self):
        self.monthlyScheduleDailyGroup = []
        self.dateTuple = ()
     
    def crawlMatchData(self,year,month,league):
        try:
            url = "https://sports.news.naver.com/wfootball/schedule/monthly?year="+year+"&month="+month+"&category="+league
            html = urlopen(url)
            soup = BeautifulSoup(html, "lxml")
            data = json.loads(soup.find("p").getText())
            self.monthlyScheduleDailyGroup = data["monthlyScheduleDailyGroup"]
            html.close()
            
        except Exception as e:
            self.monthlyScheduleDailyGroup = None
            print(e)
        
    def getMatchDates(self):
        dateList = []
        for matchOfDate in self.monthlyScheduleDailyGroup:
            dateList.append(matchOfDate["date"])
        self.dateTuple = tuple(dateList)
        return self.dateTuple

    def getMatches(self,date):
        index = self.dateTuple.index(date)
        matchOfDate = self.monthlyScheduleDailyGroup[index]
        return matchOfDate["scheduleList"]

    def homeTeamName(self, match):
       return fullFormTeam(match["homeTeamName"])
    
    def awayTeamName(self, match):
       return fullFormTeam(match["awayTeamName"])
    
    def homeTeamScore(self, match):
       return match["homeTeamScore"]
    
    def awayTeamScore(self, match):
       return match["awayTeamScore"]

    def homeTeamEmblem(self, match):
        return openImageUrl(match["homeTeamEmblem64URI"])

    def awayTeamEmblem(self, match):
       return openImageUrl(match["awayTeamEmblem64URI"])
    
    def gameStartTime(self, match):
       return match["gameStartTime"]
    
    def stadium(self, match):
       return match["stadium"]
    
    def winner(self,match):
        if match["homeTeamWon"]==True and match["awayTeamWon"]==False:
            return "home"
        elif match["homeTeamWon"]==False and match["awayTeamWon"]==True:
            return "away"
        else:
            return None