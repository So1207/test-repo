import requests
import telegram
import time
import calendar

from bs4 import BeautifulSoup
from datetime import datetime
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)

# 텔레그램 봇 토큰
my_token = '5049644362:AAH1EDr5VgJbnMtSziwwC0wWiCNb4fkcTDU'  # ' 여기에 토큰을 입력'
bot = telegram.Bot(token=my_token)

updates = bot.getUpdates()  # 업데이트 내역을 받아옴
chat_id1 = -1001768371038  # bot.getUpdates()[-1].message.chat.id

# 시작날짜 및 마지막으로 메세지가 발송된 날짜
date = 20211208
confirm_date = 20211207
i = 0


while True:
    # date의 용아맥 예매 데이터 크롤링
    now = datetime.now()
    url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=05,207&theatercode=0128&date=' + str(
        date) + '&screencodes=&screenratingcode=02&regioncode=cf'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    title = soup.select_one('body > div > div.sect-showtimes > ul > li > div > div.info-movie > a > strong')
    result = []
    result.append(str(title))
    nullvalue = '<strong>\r\n                                                '
    nullvalue2 = '</strong>'
    result = [word.replace(nullvalue, '') for word in result]
    result = [word.replace(nullvalue2, '') for word in result]

    # 연월일 마지막 예외처리
    if date - (now.year * 10000 + now.month * 100) > calendar.monthrange(now.year, now.month)[1] and date - (
            now.year * 10000 + (now.month + 1) * 100) < 1:
        if now.month == 12:
            date = (now.year + 1) * 10000 + 101
        else:
            date = now.year * 10000 + (now.month + 1) * 100 + 1
        print(now)
        print('date =', date)
        print('confirm_date =', confirm_date)
        print('다음달로넘어감')

    # 스캔을 끝낼 날짜 지정, 이후 5초간 대기
    elif i == 14:
        date = confirm_date + 1
        i = 0
        time.sleep(5)

    # 영화제목이 크롤링 데이터 내에 있는지 확인후 메세지 전송
    elif str(date) in html:
        if str('info-movie') in html:
            bot.sendMessage(chat_id=chat_id1, text= "%d %s 예매오픈!" % (date,result))
            confirm_date = date
        if str('nodata') in html:
            bot.sendMessage(chat_id=chat_id1, text= "%d 오픈된 IMAX 영화가 없습니다." % date)
            confirm_date = date
        print(now)
        print('date =', date)
        print('정상작동중')
        date = date + 1
        i = i + 1

    # 매일 1회 정상작동 메세지 출력, 이후 1분간 휴식
    else:
        if (now.hour == 12 and now.minute == 40):
            bot.sendMessage(chat_id=chat_id1, text="%d:%d 아맥알리미 스파이더맨 정상작동중!" % (now.hour, now.minute))
            time.sleep(60)
        print(now)
        print('date =', date)
        print('정상작동중')
        date = date + 1
        i = i + 1

