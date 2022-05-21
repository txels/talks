from unittest import TestCase

from hamcrest import assert_that, any_of, is_

from songs.lyrics2 import (
    analyse_lyric, extract_lyric, remove_punctuation
)

from ..utils import load_song


class TestAnalyseLyric(TestCase):

    def test_most_relevant_word_in_all_you_need_is_love(self):
        song = load_song('All you need is Love')

        main_topic, _ = analyse_lyric(song)

        self.assertEqual(main_topic, 'love')

    def test_all_you_need_is_love_contains_love_39_times(self):
        song = load_song('All you need is Love')

        _, word_count = analyse_lyric(song)

        self.assertEqual(word_count['love'], 39)

    def test_more_than_one_relevant_word(self):
        song = 'Hi ho, hi ho'

        main_topic, _ = analyse_lyric(song)

        assert_that(main_topic, any_of('hi', 'ho'))


class TestRemovePunctuation(TestCase):

    def test_returns_original_string_without_punctuation(self):
        text = 'Love, (love,) love is all you need!!!'

        result = remove_punctuation(text)

        self.assertEqual(result, 'Love love love is all you need')

    def test_string_with_no_punctuation_is_unaltered(self):
        text = 'There are mitigating circumstances'

        result = remove_punctuation(text)

        self.assertEqual(result, text)


class TestExtractLyric(TestCase):

    def test_lyric_text_is_extracted_from_xml(self):
        lyric = load_song('All you need is Love')
        xml = load_song('All you need is Love', 'xml')

        result = extract_lyric(xml)

        self.assertEqual(result, lyric)
