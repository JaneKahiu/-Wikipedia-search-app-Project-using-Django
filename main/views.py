import requests
from django.shortcuts import render
from .forms import SearchForm

def search_view(request):
    form = SearchForm()
    result = None

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            print(f'Debug: Query received: {query}')  # Debugging query
            
            url = f'https://en.wikipedia.org/w/api.php'
            params = {
                'action': 'query',
                'format': 'json',
                'prop': 'extracts',
                'titles': query,
                'formatversion': 2,
                'exintro': 1
            }
            headers = {'User-Agent': 'MyWikiSearchApp/1.0 (jkahiu2020@gmail.com)'}
            response = requests.get(url, headers=headers, params=params)

            # Debug: print status code and full response content
            print(f'Debug: Response status code: {response.status_code}')
            print(f'Debug: Response JSON: {response.json()}')

            data = response.json()
            pages = data.get('query', {}).get('pages', [])

            if pages and pages[0].get('missing') is None:
                page = pages[0]
                result = {
                    'title': page['title'],
                    'summary': page.get('extract', 'No summary available.'),
                    'url': f'https://en.wikipedia.org/wiki/{page["title"].replace(" ", "_")}',
                }
                print(f'Debug: Result found: {result}')  # Debugging result
            else:
                result = {'error': 'No results found for your query.'}
                print(f'Debug: No results found for the query.')  # Debugging no result
    
    return render(request, 'search.html', {'form': form, 'result': result})       
