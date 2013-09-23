from django.test import TestCase
from models import *


class LevelTests(TestCase):
  def test_level_hours_needed_in(self):
    expected = {
        0: 0.00,
        1: 0.10,
        4: 6.59,
        9: 17.88,
        15: 31.80,
        20: 43.60,
    }
    actual = {}
    for rank in expected:
      actual[rank] = Level.hours_needed_in(rank)
    self.assertEqual(actual, expected)

  def test_level_xp_per_hours_work_in(self):
    expected = {
        0: 0,
        1: 10,
        4: 42,
        9: 99,
        15: 169,
        20: 227,
    }
    actual = {}
    for rank in expected:
      actual[rank] = Level.xp_per_hours_work_in(rank)
    self.assertEqual(actual, expected)

  def test_level_cumulative_xp_needed_for(self):
    expected = {
        0: 0,
        1: 1,
        4: 461,
        9: 5795,
        15: 28017,
        20: 67904,
    }
    actual = {}
    for rank in expected:
      actual[rank] = Level.cumulative_xp_needed_for(rank)
    self.assertEqual(actual, expected)


class BadgeTests(TestCase):
  def test_badge_hours_needed(self):
    self.maxDiff = None  # Show all diff failures.
    expected = {
        (0, Badge.BRONZE): 0.0,
        (0, Badge.SILVER): 0.0,
        (0, Badge.GOLD): 0.0,
        (0, Badge.DIAMOND): 0.0,

        (1, Badge.BRONZE): 0.4,
        (1, Badge.SILVER): 0.8,
        (1, Badge.GOLD): 1.6,
        (1, Badge.DIAMOND): 2.4,

        (4, Badge.BRONZE): 1.6,
        (4, Badge.SILVER): 3.2,
        (4, Badge.GOLD): 6.4,
        (4, Badge.DIAMOND): 9.6,

        (9, Badge.BRONZE): 3.6,
        (9, Badge.SILVER): 7.2,
        (9, Badge.GOLD): 14.4,
        (9, Badge.DIAMOND): 21.6,

        (15, Badge.BRONZE): 6.0,
        (15, Badge.SILVER): 12.0,
        (15, Badge.GOLD): 24.0,
        (15, Badge.DIAMOND): 36.0,

        (20, Badge.BRONZE): 8.0,
        (20, Badge.SILVER): 16.0,
        (20, Badge.GOLD): 32.0,
        (20, Badge.DIAMOND): 48.0,
    }
    actual = {}
    for key in expected:
      actual[key] = Badge(
          requirement=Requirement(level=Level(rank=key[0]), order=0),
          name='Test badge',
          description='A test badge',
          training='Test training',
          grade=key[1],
          requires_verification=False).hours_needed()
    self.assertEqual(actual, expected)

  def test_badge_xp(self):
    self.maxDiff = None  # Show all diff failures.
    expected = {
        (0, Badge.BRONZE): 0,
        (0, Badge.SILVER): 0,
        (0, Badge.GOLD): 0,
        (0, Badge.DIAMOND): 0,

        (1, Badge.BRONZE): 4,
        (1, Badge.SILVER): 8,
        (1, Badge.GOLD): 16,
        (1, Badge.DIAMOND): 24,

        (4, Badge.BRONZE): 67,
        (4, Badge.SILVER): 134,
        (4, Badge.GOLD): 269,
        (4, Badge.DIAMOND): 403,

        (9, Badge.BRONZE): 356,
        (9, Badge.SILVER): 713,
        (9, Badge.GOLD): 1426,
        (9, Badge.DIAMOND): 2138,

        (15, Badge.BRONZE): 1014,
        (15, Badge.SILVER): 2028,
        (15, Badge.GOLD): 4056,
        (15, Badge.DIAMOND): 6084,

        (20, Badge.BRONZE): 1816,
        (20, Badge.SILVER): 3632,
        (20, Badge.GOLD): 7264,
        (20, Badge.DIAMOND): 10896,
    }
    actual = {}
    for key in expected:
      actual[key] = Badge(
          requirement=Requirement(level=Level(rank=key[0]), order=0),
          name='Test badge',
          description='A test badge',
          training='Test training',
          grade=key[1],
          requires_verification=False).xp()
    self.assertEqual(actual, expected)
