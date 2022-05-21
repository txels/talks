from unittest import TestCase

from songs.lyrics import (
    analyse_lyric, remove_punctuation
)

from ..utils import load_song


class TestAnalyseLyric(TestCase):

    def test_most_used_word_in_all_you_need_is_love(self):
        song = load_song('All you need is love')

        _, word_count = analyse_lyric(song)

        top_word = word_count.most_common(1)[0][0]
        self.assertEqual(top_word, 'love')


class TestRemovePunctuation(TestCase):

    def test_commas_are_removed(self):
        text = 'Love, love, love'

        result = remove_punctuation(text)

        self.assertEqual(result, 'Love love love')

    def test_punctuation_only_string_returns_empty_string(self):
        text = '?&*!'

        result = remove_punctuation(text)

        self.assertEqual(result, '')
