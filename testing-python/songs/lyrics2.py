"""
Retrieve lyrics from songs and count most used words

python -m songs.lyrics "Beatles" "All you need is love"
python -m songs.lyrics "The Police" "Roxanne"
python -m songs.lyrics "Alter Bridge" "Blackbird"
python -m songs.lyrics "Yes" "Close to the Edge"
python -m songs.lyrics "Bruce Springsteen" "The River"
python -m songs.lyrics "Marillion" "Kayleigh"

"""
from collections import Counter
import string
import xml.etree.ElementTree as ET


BASE = 'http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?'
WORDS_I_DONT_CARE_ABOUT = {
    'i', 'you', 'he', 'we', 'they', 'the', 'a', 'of', 'in', 'out', 'and', 'to',
    'is', 'be', 'on', 'its', 'your', 'very', 'but', 'from', 'this', 'that',
    'oh', 'so', 'do', 'it'
}


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def remove_non_key_words(word_counter):
    for word in WORDS_I_DONT_CARE_ABOUT:
        del word_counter[word]


def analyse_lyric(text, topmost=5):
    clean_lyric = remove_punctuation(text.lower())
    words = clean_lyric.split()
    word_counter = Counter(words)
    remove_non_key_words(word_counter)

    most_common_words = word_counter.most_common(topmost)
    main_word = most_common_words[0][0]

    return main_word, word_counter


def extract_lyric(xml_text):
    data = ET.fromstring(xml_text)
    lyric_elem = data.find('{http://api.chartlyrics.com/}Lyric')
    lyric = lyric_elem.text
    trimmed = '\n'.join(map(str.strip, lyric.splitlines()))
    return trimmed


def retrieve_song(artist, song):
    qs_args = {
        'artist': artist,
        'song': song,
    }

    url = BASE + parse.urlencode(qs_args)

    with request.urlopen(url) as response:
        content = response.read().decode('ascii')

    return content


if __name__ == '__main__':
    import json
    import sys
    from operator import itemgetter
    from urllib import request, parse

    artist, song = sys.argv[1:]

    content = retrieve_song(artist, song)
    lyric = extract_lyric(content)
    main_topic, word_count = analyse_lyric(lyric)

    print('"{}" by {} has {} words'.format(
        song, artist, len(word_count.keys())))
    print('Distinct words:', len(word_count.keys()))
    print('Most used words:', word_count.most_common(10))
    print('-' * 80)
    print('This song is about', word_count.most_common(1)[0][0])



# issues to find in tests:
# - punctuation is not processed correctly (e.g. "hello,").
# - articles and "common words" are counted
# - lyrics with non-ascii letters / hardcoded encoding
    # print(response.headers['content-type'])
# - songs not found, missing lyrics...
# - arbitrary answers when multiple words have same count


