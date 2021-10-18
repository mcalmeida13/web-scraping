import requests
from bs4 import BeautifulSoup
import pprint

print("Everything works!")

# Request the data
res = requests.get('https://news.ycombinator.com/news')

soup = BeautifulSoup(res.text,'html.parser')

links = soup.select('.storylink')

subtext = soup.select('.subtext')



def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key = lambda k: k['votes'],reverse=True)

def create_custom_hn(links, subtext):
    '''
        This function gets the text inside the tag and append to a list
    '''
    
    hn = []

    for idx, item in enumerate(links):
        # .getText() get the text inside the tag

        title = item.getText()
        
        href = item.get('href',None)
        
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points',''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes':points})
        
    return sort_stories_by_votes(hn)

pprint.pprint(create_custom_hn(links,subtext))