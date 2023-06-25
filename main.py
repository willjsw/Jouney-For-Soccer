from tkinter.ttk import *
from tkinter import *
from matchDataCrawler import *
from airportDataCrawler import *
from datetime import datetime
import tkinter.font as tkFont
import tkinter.messagebox as msgbox

#콤보박스 선택지 구성용 기본 튜플
leagueUiTuple = ("Premier League","LaLiga", "BUNDESLIGA","SERIE A","LIGUE 1","UEFA Champions League","UEFA Europa League","UEFA Europa Conference League","The FA Cup","EFL Cup","Copa del Rey","FIFA Club World Cup")
leaguePathVarTuple = ("epl","primera","bundesliga","seria","ligue1","champs","europa","uecl","facup","carlingcup","copadelrey","clubworldcup")
monthUiTuple = ("JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC")
monthPathVarTuple = ("1","2","3","4","5","6","7","8","9","10","11","12")
yearTuple = ("2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024","2025")
#크롤링 url path 변수
yearPathVar,monthPathVar,leaguePathVar = None,None,None
#전역변수 초기화
nowStadium,nowMatchDate,nowMatches,nowMatchData = "","",[],MatchData()
#팔레트
mainBgColor,fgColor1,fgColor2,winfgColor,curBgColor="#112a4a","#fff","#ffe500","#c21525","#2a2831"


#메인 함수
def main():
    #경기장 최근거리 공항 조회
    def findAirport():
        airport=crawlNearestAirport(nowStadium)
        if airport==None:
            msgbox.showwarning("공항 찾기 실패","공항을 찾을 수 없습니다.\n 인터넷 연결을 확인하세요")
        else:
            airportLabel.config(text="DESTINATION → "+airport[0]+"("+airport[1]+")")
            
    #GUI 3.2 단일 매치 조회용 리스트박스 항목 구성
    def consistMatchList(event2):
        if not event2.widget.curselection():
            return
        airportLabel.config(text="")
        global nowStadium
        selectedMatch = nowMatches[matchListBox.curselection()[0]]

        homeVar.set(nowMatchData.homeTeamName(selectedMatch))
        awayVar.set(nowMatchData.awayTeamName(selectedMatch))

        homeTeamEmblemPhoto.config(data=nowMatchData.homeTeamEmblem(selectedMatch))
        awayTeamEmblemPhoto.config(data=nowMatchData.awayTeamEmblem(selectedMatch))
        homeScore = nowMatchData.homeTeamScore(selectedMatch)
        awayScore = nowMatchData.awayTeamScore(selectedMatch)
        winner = nowMatchData.winner(selectedMatch)
        nowStadium = nowMatchData.stadium(selectedMatch)
  
        if homeScore==False and awayScore==False:
            VSLabel.config(text="VS")
            homeTeamScoreLabel.config(text=None)
            awayTeamScoreLabel.config(text=None)
        else:
            VSLabel.config(text=" : ")
            if winner=="home":
                homeLabel.config(fg=fgColor2)
                homeTeamScoreLabel.config(text=homeScore,fg=winfgColor)
                awayLabel.config(fg=fgColor1)
                awayTeamScoreLabel.config(text=awayScore,fg=fgColor1)
            elif winner=="away":
                homeLabel.config(fg=fgColor1)
                homeTeamScoreLabel.config(text=homeScore,fg=fgColor1)
                awayLabel.config(fg=fgColor2)
                awayTeamScoreLabel.config(text=awayScore,fg=winfgColor)
            else:
                homeLabel.config(fg=fgColor1)
                homeTeamScoreLabel.config(text=homeScore,fg=fgColor1)
                awayLabel.config(fg=fgColor1)
                awayTeamScoreLabel.config(text=awayScore,fg=fgColor1)
            
        subInfoLabel.config(text=nowMatchData.stadium(selectedMatch)+"\n"+nowMatchDate+", "+nowMatchData.gameStartTime(selectedMatch)+" KST ")
        resultbtn.config(state="normal")

    #GUI 3.1 매치 날짜 조회용 리스트박스 항목 구성
    def consistDateList(event1):
        if not event1.widget.curselection():
            return
        
        global nowMatchData
        global nowMatches
        global nowMatchDate

        matchListBox.delete(0,END)
        selection = dateListBox.curselection()[0]
        selectedDate = dateList[selection]
        nowMatches = nowMatchData.getMatches(dateList[selection])
        nowMatchDate = str(datetime.strptime(selectedDate,"%Y%m%d").date())

        for m in range(len(nowMatches)):
            match=nowMatches[m]
            homeTeamName = nowMatchData.homeTeamName(match)
            awayTeamName = nowMatchData.awayTeamName(match)
            gameStartTime = nowMatchData.gameStartTime(match)
            stadium = nowMatchData.stadium(match)
            matchListBox.insert(m, "%s vs %s (%s - %s KST)"%(homeTeamName,awayTeamName,stadium,gameStartTime))

    #조건에 맞는 매치 정보 조회(크롤링)
    def searchMonthlyMatch():
        dateListBox.delete(0,END)
        matchListBox.delete(0,END)

        global nowMatchData
        global dateList
        nowMatchData = MatchData()
        dateList=[]

        try:
            if yearPathVar!=None and monthPathVar!=None and leaguePathVar!=None:
                
                #매치 정보 크롤링
                nowMatchData.crawlMatchData(yearPathVar,monthPathVar,leaguePathVar)
                dateTuple = nowMatchData.getMatchDates()

                #검색조건 해당하는 매치가 없어 리다이렉트 됐을 경우
                if str(datetime.strptime(dateTuple[0],"%Y%m%d").date().month)!=monthPathVar:
                    msgbox.showwarning("알림","해당 기간에 예정/진행된 매치가 없거나 아직 시작되지 않은 시즌입니다.\n검색된 기간으로부터 가장 최근 매치가 있었던 기간을 조회합니다.")

                for d in range(len(dateTuple)):
                    date = dateTuple[d]
                    #매치가 없는 날짜는 리스트박스 패널 구성에서 제외
                    if len(nowMatchData.getMatches(date))==0:
                        continue
                    else:
                        dateList.append(date)
                        dateShow = datetime.strptime(date,"%Y%m%d").date()
                        dateListBox.insert(d,dateShow)
            else:
                msgbox.showwarning("알림","매치 정보 조회를 위해 모든 검색 조건을 입력해주세요.") 
                
        except Exception as e:
            print(e)
            msgbox.showwarning("입력오류","경기 목록을 불러올 수 없습니다.\n모든 검색 조건을 입력했는지,\n인터넷에 연결되어 있는지 확인하세요")
        
    #url path 변수 변경 함수
    def setLeaguePathVar(*args):
        global leaguePathVar
        leaguePathVar = leaguePathVarTuple[leagueCombo.current()]

    def setYearPathVar(*args):
        global yearPathVar
        selectedYear = yearVar.get()
        yearPathVar = selectedYear

    def setMonthPathVar(*args):
        global monthPathVar
        monthPathVar = monthPathVarTuple[monthCombo.current()]



    #--------------------tkinter 화면 구성 시작--------------------
    root = Tk()
    root.title("Journey for Soccer")
    root.geometry("1300x1000+50+300")
    root.configure(bg=mainBgColor)

    #폰트 세팅
    titleFont=tkFont.Font(family="Arial", size=40, weight="bold", slant="italic")
    widgetFont=tkFont.Font(family="Arial", size=16, weight="bold", slant="italic")
    matchInfoFont=tkFont.Font(family="Arial", size=25, weight="bold")
    scoreFont=tkFont.Font(family="Arial", size=40, weight="bold")
    airportInfoFont=tkFont.Font(family="Arial", size=25, weight="bold",slant="italic")
    
    #---------------1.제목 라벨---------------
    titleLabel = Label(root,height=3,text="Journey for Soccer",font=titleFont,fg=fgColor1,bg=mainBgColor)
    titleLabel.pack()
    
    #---------------2.위젯 프레임---------------
    widgetFrame = LabelFrame(root,bg=mainBgColor,borderwidth=0)
    widgetFrame.pack(pady=30)

    #-----2.1.크롤링 조건 입력용 콤보박스 프레임-----
    comboFrame = LabelFrame(widgetFrame,bg=mainBgColor,borderwidth=0)
    comboFrame.pack(side="left",padx=30)
    #2.1.1.리그 입력
    leagueCombo = Combobox(comboFrame,state="readonly",font=widgetFont,width=30)
    leagueCombo.set("Select League")
    leagueCombo['values']=leagueUiTuple
    leagueCombo.pack()
    leagueCombo.bind("<<ComboboxSelected>>", setLeaguePathVar)
    #2.1.2.연도 입력
    yearVar = StringVar()
    yearCombo = Combobox(comboFrame, textvariable=yearVar,state="readonly",font=widgetFont,width=30)
    yearCombo.set("Select Year")
    yearCombo['values']=yearTuple
    yearCombo.pack()
    yearCombo.bind("<<ComboboxSelected>>", setYearPathVar)
    #2.1.3.월 입력
    monthCombo = Combobox(comboFrame,state="readonly",font=widgetFont ,width=30)
    monthCombo.set("Select Month")
    monthCombo['values']=monthUiTuple
    monthCombo.pack()
    monthCombo.bind("<<ComboboxSelected>>", setMonthPathVar)
    
    #-----2.2.검색 버튼 프레임-----
    btnFrame = LabelFrame(widgetFrame,bg=mainBgColor,borderwidth=0)
    btnFrame.pack(side="right",padx=30)
    #2.2.1.매치 정보 크롤링
    selectBtn = Button(btnFrame,command=searchMonthlyMatch, text='Searching Match',font=widgetFont,width=25)
    selectBtn.pack(pady=10)
    #2.2.1.경기장 최근거리 공항 크롤링
    resultbtn = Button(btnFrame,command=findAirport,state="disabled", text='Nearest Airport From Stadium',font=widgetFont,anchor="center",width=25)
    resultbtn.pack(pady=10)
    
    #---------------3.매치 선택용 리스트박스 패널 프레임---------------
    listBoxframe = LabelFrame(root,bg="gray")
    listBoxframe.pack()
    #-----3.1.매치 조회할 날짜 선택-----
    dateListBox = Listbox(listBoxframe,selectmode="browse",height=10,width=20,selectbackground=curBgColor,selectforeground=fgColor1,font=widgetFont)
    dateListBox.bind("<<ListboxSelect>>",consistDateList)
    dateListBox.pack(side="left",pady=3,padx=2.5)
    #-----3.2.단일 매치 선택-----
    matchListBox = Listbox(listBoxframe,selectmode="browse",height=10,width=60,selectbackground=curBgColor,selectforeground=fgColor1,font=widgetFont)
    matchListBox.bind("<<ListboxSelect>>",consistMatchList)
    matchListBox.pack(side="right",pady=5,padx=2.5)

    #---------------4.매치 정보 프레임---------------
    matchInfoFrame = LabelFrame(root,borderwidth=0,bg=mainBgColor)
    matchInfoFrame.pack()
    #-----4.1.홈팀-----
    homeFrame = LabelFrame(matchInfoFrame,borderwidth=0,bg=mainBgColor)
    homeFrame.pack(side="left",pady=10)
    #4.1.1.홈팀 엠블럼
    homeTeamEmblemPhoto = PhotoImage(width=100,height=100)
    homeCv = Canvas(homeFrame,width=150,height=150,bg=mainBgColor,highlightthickness = 0)
    homeCv.pack(side="top")
    homeCv.create_image(95,100, anchor="center", image=homeTeamEmblemPhoto)
    #4.1.2.홈팀 이름
    homeVar =StringVar()
    homeLabel= Label(homeFrame, width=25,textvariable=homeVar, font=matchInfoFont,anchor="center",bg=mainBgColor)
    homeLabel.pack(side="bottom")

    #-----4.2.스코어/경기장/매치시간 정보 라벨-----
    InfoFrame = LabelFrame(matchInfoFrame,borderwidth=0,bg=mainBgColor)
    InfoFrame.pack(side="left",anchor="s",pady=10)
    #---4.2.1.스코어 패널---
    scoreFrame = LabelFrame(InfoFrame,borderwidth=0,bg=mainBgColor)
    scoreFrame.pack(side="top",pady=20)
    #4.2.1.1.홈팀 스코어
    homeTeamScoreLabel= Label(scoreFrame,font=scoreFont,bg=mainBgColor)
    homeTeamScoreLabel.pack(side="left")
    #4.2.1.2.VS 
    VSLabel= Label(scoreFrame,fg=fgColor1,font=scoreFont,bg=mainBgColor)
    VSLabel.pack(side="left")
    #4.2.1.3.어웨이팀 스코어
    awayTeamScoreLabel= Label(scoreFrame,font=scoreFont,bg=mainBgColor)
    awayTeamScoreLabel.pack(side="right")
    #.---4.2.2.경기장/매치시간---
    subInfoLabel = Label(InfoFrame,font=matchInfoFont,fg=fgColor1,bg=mainBgColor)
    subInfoLabel.pack(side="bottom")
    

    #-----4.3.어웨이팀-----
    awayFrame = LabelFrame(matchInfoFrame,borderwidth=0,bg=mainBgColor)
    awayFrame.pack(side="right",pady=10)
    #4.3.1.어웨이팀 엠블럼
    awayTeamEmblemPhoto = PhotoImage(width=100,height=100)
    awayCv = Canvas(awayFrame,width=150,height=150,bg=mainBgColor,highlightthickness=0)
    awayCv.pack(side="top")
    awayCv.create_image(95,100, anchor="center", image=awayTeamEmblemPhoto)
    #4.3.2.어웨이팀 이름
    awayVar =StringVar()
    awayLabel= Label(awayFrame, width=25, textvariable=awayVar,font=matchInfoFont,anchor="center", bg=mainBgColor)
    awayLabel.pack(side="bottom")

    #---------------5.경기장 최근거리 공항 정보 라벨---------------
    airportLabel = Label(root,font=airportInfoFont,fg=fgColor2,bg=mainBgColor)
    airportLabel.pack(pady=25)
    
    root.mainloop()

#메인 함수 실행
main()

