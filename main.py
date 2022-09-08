from bs4 import BeautifulSoup

from db.services import format_date, set_values, s
from db.models import Apartment

import aiohttp
import asyncio

site = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273'


async def get_apartment_data(items: BeautifulSoup):
    apartments = []

    for item in items:

        try:
            image = item.find('picture').find('img')['data-src']
            title = item.find('div', 'title').find('a', 'title').text.strip()
            city = item.find('div', 'location').find('span').text.strip()
            date = item.find('div', 'location').find('span', 'date-posted').text
            formatted_date = format_date(date)
            description = item.find('div', 'description').text.strip()
            price = item.find('div', 'price').text.strip()
            currency = 'Please contact' if price.startswith('Please') else '$'
            seats = item.find('div', 'rental-info').find('span', 'bedrooms').text.strip()

            apartments.append(Apartment(
                image_url=image,
                title=title,
                date=formatted_date,
                description=description,
                amount=price,
                seats=seats,
                city=city,
                currency=currency
            ))

        except AttributeError as e:
            print(e)
            continue

    return apartments


async def get_page_data(session, page):
    url = f'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{page}/c37l1700273'

    async with session.get(url) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'html.parser')

        items = soup.find_all('div', class_='clearfix')

        apartments = await get_apartment_data(items)

        set_values(apartments)


async def gather_data():
    url = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273'

    async with aiohttp.ClientSession() as session:
        response = await session.get(url)

        soup = BeautifulSoup(await response.text(), 'html.parser')
        pages_count = int(soup.find('div', class_='pagination').find_all('a')[-3].text)

        tasks = []

        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)

        # Получаем записи с бд для проверки
        rows = s.query(Apartment).filter(Apartment.id > 1)
        for row in rows:
            print(row.title, row.image_url)


def main():
    asyncio.run(gather_data())


if __name__ == '__main__':
    main()
