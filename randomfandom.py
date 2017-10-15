# -*- coding: utf-8 -*-

# scraping from memory-alpha, the star trek fan wiki

import requests, time, random
from bs4 import BeautifulSoup

BS_PARSER = "html.parser" 
RUN = True # switch this to true to run script
ROOT_URL = u'http://memory-alpha.wikia.com'
RANDOM_URL = ROOT_URL + u'/wiki/Special:Random'

SERIES = {'TOS' : 3, # number of seasons in each series
          'TNG' : 7,
          'DS9' : 7,
          'VOY' : 7,
          'ENT' : 4}
          
def get_season_url(show, season):
    '''get the URL corresponding to a season of a particular show, which contains a list of episodes of that season'''
    if int(season) <= SERIES[show] and int(season) > 0 and show in SERIES.keys():
        return u'http://memory-alpha.wikia.com/wiki/{0}_Season_{1}'.format(show, str(season))
    else:
        raise ValueError('''That show/season doesn't exist!''')

def load_url(url, parser = BS_PARSER):
    content = requests.get(url).text
    return BeautifulSoup(content, parser)
    
def random_episode():
    '''get URL of a random star trek episode'''
    # pick a random show and season
    show = random.choice(SERIES.keys())
    season = random.randint(1, SERIES[show])
    
    # load episode list
    sand = load_url(get_season_url(show, season))
    episodetable = sand.find_all('table')[-2] 
    episodes = [a['href'] for i, a in enumerate(episodetable.find_all('a', href=True)) if a['href'].endswith('(episode)')] 
    return ROOT_URL + random.choice(episodes)

def random_synopsis():
    '''get the synopsis of a random star trek episode'''
    sand = load_url(random_episode())
    return sand.find('meta', property='og:description')['content'] # this synopsis sometimes trails off with ellipses if it is over 500 char

def episode_sentences(synopsis):
    '''split an episode synposis into component sentences and return them in a list of sentences'''
    return [(i+'.').strip() for i in synopsis.split('.') if len(i) > 0]

def hybrid_episode(synopsis1, synopsis2):
    '''combines sentences from two episode synopses'''
    sentences1 = episode_sentences(synopsis1)[1:]
    sentences2 = episode_sentences(synopsis2)[1:]

    hybrid = []
    hybridlength = random.randint(4, 6)
    probability = 0.5

    while hybridlength != 0:
        got_a_sentence = False

        if random.random() < probability:
            if len(sentences1) > 0:
                hybrid.append(sentences1.pop(0))
                got_a_sentence = True
                probability = probability - .1
        else:
            if len(sentences2) > 0:
                hybrid.append(sentences2.pop(0))
                got_a_sentence = True
                probability = probability + .1

        if got_a_sentence:
            hybridlength = hybridlength-1

    return ' '.join(hybrid)

if __name__ == "__main__" and RUN:
    a = random_synopsis()
    b = random_synopsis()
    print a
    print "\n"
    print b 
    print "\n"

    print "HYBRID EPISODE:"
    print hybrid_episode(a, b)