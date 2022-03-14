import requests
from .models import Quote

url = 'http://quotes.stormconsultancy.co.uk/random.json'

def get_quotes():
    response = requests.get(url)
    return response.json()
    
def process_quote():
    quotes = get_quotes()
    new_quote = Quote(quotes["author"], quotes["quote"])
    print(new_quote)
    return new_quote

