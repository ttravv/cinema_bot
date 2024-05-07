import httpx
from dotenv import dotenv_values

config = dotenv_values('.env')

def movie_by_genre_year(genre: str, years: str) -> str:
    base_url = 'https://api.kinopoisk.dev/v1.4/movie'
    url = f'{base_url}?page=1&limit=5&votes.imdb=100000-10000000&type=movie&genres.name={genre}&year={years}&sortField=rating.imdb&sortType=-1'
    return url
    

async def get_request(url: str) -> list[dict]:
    headers = {"X-API-KEY": config['API_TOKEN'] }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    return response.json()['docs']

def parsing(film_info: dict) -> str:
    return f'Название фильма: {film_info['name']}' + \
    f'Описание фильма: {film_info['description']}' + \
    f'Рейтинг фильма: {film_info['rating']['imdb']}' + \
    f'Год выпуска: {film_info['year']}' + \
    f'Ссылка на фильм: https://www.kinopoisk.ru/film/{film_info['id']}'
    









