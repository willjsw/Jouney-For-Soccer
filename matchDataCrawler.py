from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

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
            
        except Exception as e:
            self.monthlyScheduleDailyGroup = None
            print("크롤링 실패")
        
    def getMatchDate(self):
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
       return match["homeTeamName"]
    
    def awayTeamName(self, match):
       return match["awayTeamName"]
    
    def homeTeamEmblem(self, match):
       return match["homeTeamEmblem64URI"]
    
    def awayTeamEmblem(self, match):
       return match["awayTeamEmblem64URI"]
    
    def gameStartTime(self, match):
       return match["gameStartTime"]
    
    def stadium(self, match):
       return match["stadium"]
    
    