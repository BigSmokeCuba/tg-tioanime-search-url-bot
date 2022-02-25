import requests
import bs4

from bs4 import BeautifulSoup


HOST = 'https://tioanime.com'

def search(name=''):
    global HOST
    searchUrl = 'https://tioanime.com/'
    if name != '':
        searchUrl = HOST + '/directorio?q=' + name
        resp = requests.get(searchUrl)
        html = str(resp.text)
        soup = BeautifulSoup(html,'html.parser')
        ul = soup.find('ul',{'class':'animes'})
        list = ul.find_all('li')
        result = []
        for anime in list:
            anime_name = anime.find('h3',{'class':'title'}).next
            anime_image = HOST + anime.find('img').attrs['src']
            anime_url = HOST + anime.find('a').attrs['href']
            result.append({'name':anime_name,'imageurl':anime_image,'url':anime_url})
        return result
    else:
        resp = requests.get(searchUrl)
        html = str(resp.text)
        soup = BeautifulSoup(html,'html.parser')
        episodies = soup.find('ul',{'class':'episodes'}).find_all('li')
        result = []
        for epi in episodies:
            epi_name = epi.find('h3',{'class':'title'}).next
            epi_image = HOST + epi.find('img').attrs['src']
            epi_url = HOST + epi.find('a').attrs['href']
            result.append({'name':epi_name,'imageurl':epi_image,'url':epi_url})
        return result
    return None

def get_info(anime):
    resp = requests.get(anime['url'])
    html = str(resp.text)
    soup = BeautifulSoup(html,'html.parser')
    info = {'name':anime['name'],'imageurl':anime['imageurl']}
    info['sinopsis'] = soup.find('p',{'class':'sinopsis'}).next
    info['genres'] = []
    genres = soup.find('p',{'class':'genres'}).find_all('a')
    for g in genres:
        info['genres'].append(g.next)
    #js parse
    script = str(soup.find_all('script')[-1].next).replace('\r','').replace('\n','').replace(' ','')
    scripttokens = str(script).split(';')
    varepisodies = str(scripttokens[1]).replace('varepisodes=','').replace('[','').replace(']','')
    episodies = varepisodies.split(',')
    #end
    info['episodies'] = episodies
    info['episodies_count'] = len(episodies)
    return info

def make_episodie_url(anime,episodie):
    url = str(anime['url']).replace('/anime/','/ver/') + '-' + str(episodie)
    return url

def get_downloads_url(episodie_url):
    resp = requests.get(episodie_url)
    html = str(resp.text)
    soup = BeautifulSoup(html,'html.parser')
    urls = []
    urllist = soup.find('table',{'class':'table-downloads'}).find('tbody').find_all('tr')
    for url in urllist:
        server = url.find_all('td')[0].next
        download_url = url.find('a').attrs['href']
        urls.append({'server':server,'url':download_url})
    return urls


#result = search()
#print(result)
#result = search('naruto')
#episodie_url = make_episodie_url(result[0],1)
#urls = get_downloads_url(episodie_url)
#info = get_info(result[0])
#print(info)