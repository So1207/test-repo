import requests
import telegram as tel
from bs4 import BeautifulSoup

bot = tel.Bot(token="5049644362:AAH1EDr5VgJbnMtSziwwC0wWiCNb4fkcTDU")
chat_id = 990167577

url = 'http://www.cgv.co.kr/reserve/show-times/?areacode=05%2C207&theaterCode=0128&date=20211207'
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
list = soup.select('.info-hall')
if '스파이더' in html and 'IMAX' in str(list):
    bot.sendMessage(chat_id = chat_id, text="예매 오픈!") # 메세지 보내기
    
    
