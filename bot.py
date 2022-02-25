from pyobigram.client import ObigramClient,inlineQueryResultArticle

import config
import animedl



def oninline(update,bot:ObigramClient):
    querytext = update.inline_query.query
    query_id = update.inline_query.id
    result = []
    list = animedl.search(querytext)
    qid = 0
    cmd = '/episodie '
    if querytext!='':
       cmd = '/anime_' + str(qid) + ' ' 
    for anime in list:
         result.append(inlineQueryResultArticle(qid,title=anime['name'],text=cmd+anime['name'],thumb_url=anime['imageurl']))
         qid+=1
    bot.answerInline(query_id,result)
    pass


def onstart(update,bot:ObigramClient):
    bot.sendMessage(update.message.chat.id,text='😄Bienvenido a AnimeSBot😄\n-Use el buscador inline @animesbot_bot para buscar un anime especifico o uno de los episodios estrenos.')

def onepisodie(update,bot:ObigramClient):
    name = str(update.message.text).replace('/episodie ','')
    if name!='':
        list = animedl.search()
        episodie = None
        for epi in list:
            if epi['name']==name:
                episodie = epi
                break
        urls = animedl.get_downloads_url(episodie['url'])
        html = '<a href="'+episodie['imageurl']+'">'+episodie['name']+'</a>\n\n'
        html += '<b>🔗Enlaces De Descarga🔗</b>\n'
        for url in urls:
            html += '<a href="'+url['url']+'">📥Descargar Por '+url['server']+'📥</a>\n\n'
        bot.sendMessage(update.message.chat.id,text=html,parse_mode='html')
    pass

def onanime(update,bot:ObigramClient):
    text = str(update.message.text).replace('/anime_','')
    if text!='':
        tokens = text.split(' ',1)
        name = tokens[1]
        qid = tokens[0]
        list = animedl.search(name)
        anime = list[int(qid)]
        info = animedl.get_info(anime)
        episodies_urls = []
        episodies = []
        for epi in info['episodies']:
            episodies.append(int(epi))
        episodies.sort()
        for epi in episodies:
            epiurl = animedl.make_episodie_url(anime,epi)
            urls = animedl.get_downloads_url(epiurl)
            episodies_urls.append({'index':epi,'urls':urls})
        html = '<a href="'+anime['imageurl']+'">'+anime['name']+'</a>\n'
        html += '<b>Episodios : '+str(len(episodies))+'</b>\n'
        html += '<b>📃Descripcion📃</b>\n'
        html += '<b>'+info['sinopsis']+'</b>\n'
        html += '<b>🗳Capitulos🗳</b>\n'
        for epiurls in episodies_urls:
            html += '<b>🗂Capitulo '+str(epiurls['index'])+'🗂</b>\n'
            for url in epiurls['urls']:
                html += '<a href="'+url['url']+'">📥Descargar Por '+url['server']+'📥</a>\n'
        bot.sendMessage(update.message.chat.id,text=html,parse_mode='html')
    pass


def main():
    bot = ObigramClient(config.BOT_TOKEN)
    bot.on('/start',onstart)
    bot.on('/episodie',onepisodie)
    bot.on('/anime',onanime)
    bot.onInline(oninline)
    print('Bot is Run!')
    bot.run()
    print('Bot is Stoped!')
    pass
if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print(str(ex))
        print('Bot is Restarted!')
        main()