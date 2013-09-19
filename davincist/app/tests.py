from django.test import TestCase
from models import *


class LevelTests(TestCase):
  def test_level_hours_needed_in(self):
    expected = {
        0: 0,
        1: 1,
        4: 42,
        9: 255,
        15: 788,
        20: 1485,
    }
    actual = {}
    for rank in expected:
      actual[rank] = Level.hours_needed_in(rank)
    self.assertEqual(actual, expected)

  def test_level_xp_per_hours_work_in(self):
    expected = {
        0: 0,
        1: 20,
        4: 422,
        9: 2514,
        15: 7734,
        20: 14565,
    }
    actual = {}
    for rank in expected:
      actual[rank] = Level.xp_per_hours_work_in(rank)
    self.assertEqual(actual, expected)

  def test_level_cumulative_xp_needed_for(self):
    expected = {
        0: 0,
        1: 20,
        4: 23408,
        9: 1412504,
        15: 20110321,
        20: 91253113,
    }
    actual = {}
    for rank in expected:
      actual[rank] = Level.cumulative_xp_needed_for(rank)
    self.assertEqual(actual, expected)


class BadgeTests(TestCase):
  def test_badge_hours_needed(self):
    expected = {
        (0, Badge.BRONZE): 0.0,
        (0, Badge.SILVER): 0.0,
        (0, Badge.GOLD): 0.0,
        (0, Badge.DIAMOND): 0.0,

        (1, Badge.BRONZE): 0.25,
        (1, Badge.SILVER): 0.5,
        (1, Badge.GOLD): 1.0,
        (1, Badge.DIAMOND): 1.5,

        (4, Badge.BRONZE): 4.0,
        (4, Badge.SILVER): 8.0,
        (4, Badge.GOLD): 16.0,
        (4, Badge.DIAMOND): 24.0,

        (9, Badge.BRONZE): 10.25,
        (9, Badge.SILVER): 20.5,
        (9, Badge.GOLD): 41.0,
        (9, Badge.DIAMOND): 61.5,

        (15, Badge.BRONZE): 17.75,
        (15, Badge.SILVER): 35.5,
        (15, Badge.GOLD): 71.0,
        (15, Badge.DIAMOND): 106.5,

        (20, Badge.BRONZE): 24.0,
        (20, Badge.SILVER): 48.0,
        (20, Badge.GOLD): 96.0,
        (20, Badge.DIAMOND): 144.0,
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
    expected = {
        (0, Badge.BRONZE): 0,
        (0, Badge.SILVER): 0,
        (0, Badge.GOLD): 0,
        (0, Badge.DIAMOND): 0,

        (1, Badge.BRONZE): 5,
        (1, Badge.SILVER): 10,
        (1, Badge.GOLD): 20,
        (1, Badge.DIAMOND): 30,

        (4, Badge.BRONZE): 1688,
        (4, Badge.SILVER): 3376,
        (4, Badge.GOLD): 6752,
        (4, Badge.DIAMOND): 10128,

        (9, Badge.BRONZE): 25769,
        (9, Badge.SILVER): 51537,
        (9, Badge.GOLD): 103074,
        (9, Badge.DIAMOND): 154611,

        (15, Badge.BRONZE): 137279,
        (15, Badge.SILVER): 274557,
        (15, Badge.GOLD): 549114,
        (15, Badge.DIAMOND): 823671,

        (20, Badge.BRONZE): 349560,
        (20, Badge.SILVER): 699120,
        (20, Badge.GOLD): 1398240,
        (20, Badge.DIAMOND): 2097360,
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
