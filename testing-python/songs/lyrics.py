"""
Retrieve lyrics from songs and count most used words

python -m songs.lyrics "Beatles" "All you need is love"
python -m songs.lyrics "The Police" "Roxanne"
python -m songs.lyrics "Alter Bridge" "Blackbird"
python -m songs.lyrics "Yes" "Close to the Edge"
python -m songs.lyrics "Bruce Springsteen" "The River"
python -m songs.lyrics "Marillion" "Kayleigh"

"""

BASE = 'http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?'

from collections import Counter
import string


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def analyse_lyric(text):
    text = text.lower()
    text = remove_punctuation(text)
    words = text.split()
    word_count = Counter(words)
    return words, word_count


if __name__ == '__main__':
    import json
    import sys
    from operator import itemgetter
    from urllib import request, parse
    import xml.etree.ElementTree as ET

    artist, song = sys.argv[1:]

    qs_args = {
        'artist': artist,
        'song': song,
    }

    url = BASE + parse.urlencode(qs_args)

    with request.urlopen(url) as response:
        content = response.read().decode('ascii')
        data = ET.fromstring(content)

    lyric_elem = data.find('{http://api.chartlyrics.com/}Lyric')
    lyric = lyric_elem.text

    print(lyric, '\n\n\n')
    print('-' * 80)

    words, word_count = analyse_lyric(clean_lyrics)

    print('"{}" by {} has {} words'.format(song, artist, len(words)))
    print('Distinct words:', len(word_count.keys()))
    print('Most used words:')
    print(word_count.most_common(20))
    print('-' * 80)
    print('This song is about', word_count.most_common(1)[0][0])
