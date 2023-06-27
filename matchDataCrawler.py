from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import json
import base64

#크롤링 결과 중 일부 커스터마이징
def fullFormTeam(team):
    if team == "맨유":
        return "맨체스터 유나이티드"
    else:
        return team
#크롤링한 팀 별 엠블럼 url -> base64 포맷으로 변환해서 열기(http에러 발생 시 로컬에 저장된 기본 이미지 파일로 대체)
def openImageUrl(imgUrl):
    try:
        img = urlopen(imgUrl).read()
        return base64.encodebytes(img) 
    except HTTPError as e:
        code = e.getcode()
        print(str(code)+": impropal image url")
        return base64.b64encode(open("defaultEmblem.png", "rb").read())

#main 코드에서 빈번하게 사용되는 크롤링한 데이터를 객체로 관리하기 위해 class 선언
#크롤링한 xhr 파일 본문의json 데이터 문자열화 및 파싱      
class MatchData:

    #클래스 내 self 변수들 초기화
    def __init__(self):
        self.monthlyScheduleDailyGroup = []
        self.dateTuple = ()
    
    #크롤링 및 json 파싱
    def crawlMatchData(self,year,month,league):
        try:
            url = "https://sports.news.naver.com/wfootball/schedule/monthly?year="+year+"&month="+month+"&category="+league
            html = urlopen(url)
            #bs4 파싱 성능 개선 위해 lxml 모듈 사용
            soup = BeautifulSoup(html, "lxml")
            #xhr 파일 본문의 json 데이터 역직렬화
            data = json.loads(soup.find("p").getText())
            self.monthlyScheduleDailyGroup = data["monthlyScheduleDailyGroup"]
            html.close()
            
        except Exception as e:
            self.monthlyScheduleDailyGroup = None
            print(e)
    #크롤링한 조건(리그, 연월, 월)에 해당되는 경기 일자 튜플로 구성
    def getMatchDates(self):
        dateList = []
        for matchOfDate in self.monthlyScheduleDailyGroup:
            dateList.append(matchOfDate["date"])
        self.dateTuple = tuple(dateList)
        return self.dateTuple
    
    #입력된 날짜에 해당하는 경기 정보 딕셔너리 형태로 반환
    def getMatches(self,date):
        index = self.dateTuple.index(date)
        matchOfDate = self.monthlyScheduleDailyGroup[index]
        return matchOfDate["scheduleList"]
    
    #홈 팀 이름 가져오기
    def homeTeamName(self, match):
       return fullFormTeam(match["homeTeamName"])
    #어웨이 팀 이름 가져오기
    def awayTeamName(self, match):
       return fullFormTeam(match["awayTeamName"])
    #홈 팀 점수 가져오기
    def homeTeamScore(self, match):
       return match["homeTeamScore"]
    #어웨이 팀 점수 가져오기
    def awayTeamScore(self, match):
       return match["awayTeamScore"]
    #홈 팀 엠블럼 가져오럼
    def homeTeamEmblem(self, match):
        return openImageUrl(match["homeTeamEmblem64URI"])
    #홈 팀 엠블럼 가져오기
    def awayTeamEmblem(self, match):
       return openImageUrl(match["awayTeamEmblem64URI"])
    #경기 시작 시간 가져오기
    def gameStartTime(self, match):
       return match["gameStartTime"]
    #경기장 정보 가져오기
    def stadium(self, match):
       return match["stadium"]
    #경기 승자 가져오기
    def winner(self,match):
        if match["homeTeamWon"]==True and match["awayTeamWon"]==False:
            return "home"
        elif match["homeTeamWon"]==False and match["awayTeamWon"]==True:
            return "away"
        else:
            return None