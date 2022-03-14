import requests
from .models import Quote

url = 'http://quotes.stormconsultancy.co.uk/random.json'

def get_quotes():
    response = requests.get(url)
    return response.json()
    
def process_quote():
    quote = get_quotes()
    return Quote(quote["author"], quote["quote"])
