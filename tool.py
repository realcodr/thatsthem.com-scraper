from typing import Sequence, Any

import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

from writers import CSVWriter

def get_text(list_: Sequence) -> Any:
	return list_[0].text.strip() if list_ else '-'


def extract_data(record: object) -> None:
	name = get_text(record.select(".name")) 
	residence = get_text(record.select(".resides")).replace(',', '')
	age = get_text(record.select(".age")).replace(',', '')
	phone = get_text(record.select("span.number"))
	address = get_text(record.select(".location"))
	address = ' '.join(address.replace(',', '').split())
	print('*', name, ',', residence, age, phone, address)
	data = {'name': name, 'residence': residence, 'age': age, 'phone': phone, 'address': address}
	writer.writerow(data)


def request_data(url: str) -> None:
	headers = { 
		"user-agent": useraget_randomizer.random, 
		"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
		"accept-encoding": "gzip, deflate, br",
		"accept-language": "en-US,en;q=0.9",
		"cache-control": "max-age=0",
	}
	res = requests.get(url, headers=headers, timeout=60)
	make_soup(res) if res.ok and res.url == url else print(res.url)


def make_soup(res: object) -> None:
	soup = bs(res.text, features="html.parser")
	records = soup.select('div.record')
	for record in records:
		extract_data(record)


def main(name: str = 'jean doe') -> None:
	url: str = f"https://thatsthem.com/name/{name.title().replace(' ', '-')}"
	request_data(url)
	for number in range(2, 10):
		next_url = f"{url}?page={number}"
		# print(next_url)
		request_data(next_url)

if __name__ == "__main__":
	useraget_randomizer = UserAgent(fallback='Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1ua.ff')
	fields = ['name', 'residence', 'age', 'phone', 'address',]
	writer = CSVWriter(fields)
	main()