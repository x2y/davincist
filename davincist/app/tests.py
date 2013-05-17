from django.test import TestCase
from models import *


class LevelTests(TestCase):
  def test_level_hours_needed(self):
    expected = {
        0: 0,
        1: 1,
        4: 42,
        9: 255,
        15: 788,
        20: 1485,
    }
    actual = {}
    for key in expected:
      actual[key] = Level(rank=key).hours_needed()
    self.assertEqual(actual, expected);


class QuestTests(TestCase):
  def test_quest_hours_needed(self):
    expected = {
        (0, Quest.SMALL): 0.0,
        (0, Quest.MEDIUM): 0.0,
        (0, Quest.LARGE): 0.0,
        (0, Quest.EXTRA_LARGE): 0.0,

        (1, Quest.SMALL): 0.25,
        (1, Quest.MEDIUM): 0.5,
        (1, Quest.LARGE): 1.0,
        (1, Quest.EXTRA_LARGE): 1.5,

        (4, Quest.SMALL): 4.0,
        (4, Quest.MEDIUM): 8.0,
        (4, Quest.LARGE): 16.0,
        (4, Quest.EXTRA_LARGE): 24.0,

        (9, Quest.SMALL): 10.25,
        (9, Quest.MEDIUM): 20.5,
        (9, Quest.LARGE): 41.0,
        (9, Quest.EXTRA_LARGE): 61.5,

        (15, Quest.SMALL): 17.75,
        (15, Quest.MEDIUM): 35.5,
        (15, Quest.LARGE): 71.0,
        (15, Quest.EXTRA_LARGE): 106.5,

        (20, Quest.SMALL): 24.0,
        (20, Quest.MEDIUM): 48.0,
        (20, Quest.LARGE): 96.0,
        (20, Quest.EXTRA_LARGE): 144.0,
    }
    actual = {}
    for key in expected:
      actual[key] = Quest(name='Test quest',
                          description='A test quest',
                          level=Level(rank=key[0]),
                          size=key[1]).hours_needed();
    self.assertEqual(actual, expected);

  def test_quest_xp(self):
    expected = {
        (0, Quest.SMALL): 0,
        (0, Quest.MEDIUM): 0,
        (0, Quest.LARGE): 0,
        (0, Quest.EXTRA_LARGE): 0,

        (1, Quest.SMALL): 5,
        (1, Quest.MEDIUM): 10,
        (1, Quest.LARGE): 20,
        (1, Quest.EXTRA_LARGE): 30,

        (4, Quest.SMALL): 1688,
        (4, Quest.MEDIUM): 3376,
        (4, Quest.LARGE): 6752,
        (4, Quest.EXTRA_LARGE): 10128,

        (9, Quest.SMALL): 25769,
        (9, Quest.MEDIUM): 51537,
        (9, Quest.LARGE): 103074,
        (9, Quest.EXTRA_LARGE): 154611,

        (15, Quest.SMALL): 137279,
        (15, Quest.MEDIUM): 274557,
        (15, Quest.LARGE): 549114,
        (15, Quest.EXTRA_LARGE): 823671,

        (20, Quest.SMALL): 349560,
        (20, Quest.MEDIUM): 699120,
        (20, Quest.LARGE): 1398240,
        (20, Quest.EXTRA_LARGE): 2097360,
    }
    actual = {}
    for key in expected:
      actual[key] = Quest(name='Test quest',
                          description='A test quest',
                          level=Level(rank=key[0]),
                          size=key[1]).xp();
    self.assertEqual(actual, expected);

