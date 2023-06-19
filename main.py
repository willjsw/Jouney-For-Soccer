from tkinter.ttk import *
from tkinter import *
from matchDataCrawler import *
from airportDataCrawler import *
from datetime import datetime
import tkinter.font as tkFont
import tkinter.messagebox as msgbox
import base64

league = ("Premier League","LaLiga", "BUNDESLIGA","SERIE A","LIGUE 1","UEFA Champions League")
leaguePathVar = ("epl","primera","bundesliga","seria","ligue1","champs")

month = ("JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC")
monthPathVar = ("1","2","3","4","5","6","7","8","9","10","11","12")

year = ("2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024","2025")

searchMonth = None
searchYear = None
searchLeague = None
stadium = None
matchData = MatchData()
matches = []



def main():

    mainBgColor="#112a4a"
    fgColor="#fff"
    
    root = Tk()
    root.title("Journey for Soccer")
    root.geometry("1100x1000+200+300")
    root.configure(bg=mainBgColor)

    titleFont=tkFont.Font(family="Arial", size=50, weight="bold", slant="italic")
    widgetFont=tkFont.Font(family="Arial", size=16, weight="bold", slant="italic")
    matchInfoFont=tkFont.Font(family="Arial", size=25, weight="bold")
    airportInfoFont=tkFont.Font(family="Arial", size=30, weight="bold",slant="italic")

    def findAirport():
        airportLabel.config(text=None)
        airport = crawlNearestAirport(stadium)
        if airport == None:
            msgbox.showwarning("공항 찾기 실패","공항을 찾을 수 없습니다.\n 인터넷 연결을 확인하세요")
        else:
            airportLabel.config(text="DESTINATION → "+airport)


    def setImgUrl(imgUrl):
        image_byt = urlopen(imgUrl).read()
        return base64.encodebytes(image_byt)

    
    def consistMatchList(event2):
        if not event2.widget.curselection():
            return
        global stadium
        selectedMatch = matches[matchListBox.curselection()[0]]
        selected_item = matchListBox.get(matchListBox.curselection()[0])
        if matchData.homeTeamName(selectedMatch)=="맨유":
           homeVar.set("맨체스터 유나이티드")
        else:
            homeVar.set(matchData.homeTeamName(selectedMatch))
        awayVar.set(matchData.awayTeamName(selectedMatch))

        homeTeamEmblemPhoto.config(data = setImgUrl(matchData.homeTeamEmblem(selectedMatch)))
        awayTeamEmblemPhoto.config(data = setImgUrl(matchData.awayTeamEmblem(selectedMatch)))

        stadium = matchData.stadium(selectedMatch)

        vsLabel.config(text="\n\nVS"+"\n\n"+matchData.stadium(selectedMatch)+"\nStarts At: "+matchData.gameStartTime(selectedMatch))
        resultbtn.config(state="normal")
        print(selected_item)

    def consistDateList(event1):
        if not event1.widget.curselection():
            return
        
        global matchData
        global matches
        
        matchListBox.delete(0,END)
        selection = dateListBox.curselection()[0]
      
        matches = matchData.getMatches(dateList[selection])
        
        
        for m in range(len(matches)):
            matchNum = matches[m]
            homeTeamName = matchData.homeTeamName(matchNum)
            awayTeamName = matchData.awayTeamName(matchNum)
            gameStartTime = matchData.gameStartTime(matchNum)
            stadium = matchData.stadium(matchNum)
            matchListBox.insert(m, "%s vs %s (%s - %s)"%(homeTeamName,awayTeamName,stadium,gameStartTime))
    

    def searchMonthlyMatch():
        dateListBox.delete(0,END)
        matchListBox.delete(0,END)
        
        global matchData
        global dateList
        global dateList
        dateList=[]

        matchData = MatchData()
        try:
            matchData.crawlMatchData(searchYear,searchMonth,searchLeague)
            dateTuple = matchData.getMatchDate()
            date_format = "%Y%m%d"
            if str(datetime.strptime(dateTuple[0], date_format).date().month)!=searchMonth:
               msgbox.showwarning("알림","해당 기간에 예정/진행된 경기가 없거나 아직 시작되지 않은 시즌입니다.\n검색된 기간으로부터 가장 최근 경기가 있었던 기간을 조회합니다.") 
            for i in range(len(dateTuple)):
                date = dateTuple[i]
                if len(matchData.getMatches(date))==0:
                    continue
                else:
                    dateList.append(date)
                    
                    dateShow = datetime.strptime(date, date_format).date()
                    dateListBox.insert(i,dateShow)
    
                
        except:
            msgbox.showwarning("입력오류","경기 목록을 불러올 수 없습니다.\n모든 검색 조건을 입력했는지,\n인터넷에 연결되어 있는지 확인하세요")
        
    def leagueVarChange(*args):
        global searchLeague
        searchLeague = leaguePathVar[leagueCombo.current()]

    def yearVarChange(*args):
        global searchYear
        selectedYear = yearVar.get()
        searchYear = selectedYear

    def monthVarChange(*args):
        global searchMonth
        searchMonth = monthPathVar[monthCombo.current()]
    
    titleLabel = Label(height=3,text="Journey for Soccer",font=titleFont,fg=fgColor,bg=mainBgColor)
    titleLabel.pack()

    widgetFrame = LabelFrame(root,bg=mainBgColor,borderwidth=0)

    #combobox
    comboFrame = LabelFrame(widgetFrame,bg=mainBgColor,borderwidth=0)

    leagueCombo = Combobox(comboFrame,state="readonly",font=widgetFont,width=25)
    leagueCombo.set("Select League")
    leagueCombo['values']=league
    leagueCombo.pack()
    leagueCombo.bind("<<ComboboxSelected>>", leagueVarChange)

    yearVar = StringVar()
    yearCombo = Combobox(comboFrame, textvariable=yearVar,state="readonly",font=widgetFont,width=25)
    yearCombo.set("Select Year")
    yearCombo['values']=year
    yearCombo.pack()
    yearCombo.bind("<<ComboboxSelected>>", yearVarChange)

    monthCombo = Combobox(comboFrame,state="readonly",font=widgetFont ,width=25)
    monthCombo.set("Select Month")
    monthCombo['values']=month
    monthCombo.pack()
    monthCombo.bind("<<ComboboxSelected>>", monthVarChange)

    comboFrame.pack(side="left",padx=30)
    
    #buttons
    btnFrame = LabelFrame(widgetFrame,bg=mainBgColor,borderwidth=0)
    selectBtn = Button(btnFrame,command=searchMonthlyMatch, text='Searching Match',font=widgetFont,width=25)
    selectBtn.pack(pady=10)

    resultbtn = Button(btnFrame,command=findAirport,background="black",state="disabled", text='Nearest Airport From Stadium',font=widgetFont,anchor="center",width=25)
    resultbtn.pack(pady=10)
    btnFrame.pack(side="right",padx=30)

    widgetFrame.pack(pady=30)

    #listboxes
    listBoxframe = LabelFrame(root,bg="gray")
    listBoxframe.pack()

    dateListBox = Listbox(listBoxframe,
                          selectmode="browse",
                          relief="solid",
                          height=10, 
                          width=20,
                          selectbackground="#2a2831",
                          selectforeground=fgColor,
                          font=widgetFont)
    dateListBox.bind("<<ListboxSelect>>",consistDateList)
    dateListBox.pack(side="left",pady=5,padx=2.5)

    matchListBox = Listbox(listBoxframe,
                           selectmode="browse",
                           relief="solid",height=10, 
                           width=60,
                           selectbackground="#2a2831",
                           selectforeground=fgColor,
                           font=widgetFont)
    matchListBox.bind("<<ListboxSelect>>",consistMatchList)
    matchListBox.pack(side="right",pady=5,padx=2.5)

    #매치 정보
    matchInfoframe = LabelFrame(root,borderwidth=0,bg=mainBgColor)
    matchInfoframe.pack()

    homeFrame = LabelFrame(matchInfoframe,borderwidth=0,bg=mainBgColor)
    homeFrame.pack(side="left",pady=10)
    
    homeTeamEmblemPhoto = PhotoImage(width=100,height=100)
    
    homeCv = Canvas(homeFrame,width=150,height=150,bg=mainBgColor,highlightthickness = 0)
    homeCv.pack(side="top")
    homeCv.create_image(95,100, anchor="center", image = homeTeamEmblemPhoto)

    homeVar =StringVar()
    homeLabel= Label(homeFrame, width=25,textvariable=homeVar, font=matchInfoFont,anchor="center",bg=mainBgColor,fg=fgColor)
    homeLabel.pack(side="bottom")

    #vs& 경기정보 패널
    vsLabel = Label(matchInfoframe,font=matchInfoFont,fg=fgColor,bg=mainBgColor)
    vsLabel.pack(side="left")

    #away
    awayFrame = LabelFrame(matchInfoframe,borderwidth=0,bg=mainBgColor)
    awayFrame.pack(side="right",pady=10)

    awayTeamEmblemPhoto = PhotoImage(width=100,height=100)

    awayCv = Canvas(awayFrame,width=150,height=150,bg=mainBgColor,highlightthickness = 0)
    awayCv.pack(side="top")
    awayCv.create_image(95,100, anchor="center", image = awayTeamEmblemPhoto)

    awayVar =StringVar()
    awayLabel= Label(awayFrame, width=25, textvariable=awayVar,font=matchInfoFont,anchor="center", bg=mainBgColor,fg=fgColor)
    awayLabel.pack(side="bottom")

    #공항정보 검색 패널
    airportLabel = Label(root,font=airportInfoFont,fg="#ffe500",bg=mainBgColor)
    airportLabel.pack(pady=30)
    
    root.mainloop()

main()

        

