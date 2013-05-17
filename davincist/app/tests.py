from django.test import TestCase
from models import *


class QuestTests(TestCase):
  def init_quest(self, level, size):
    return Quest(name='Test quest',
                 description='A test quest',
                 level=Level(rank=level),
                 size=size);

  def test_level_hours_needed(self):
    self.assertEqual(Level(rank=0).hours_needed(), 0)
    self.assertEqual(Level(rank=1).hours_needed(), 1)
    self.assertEqual(Level(rank=4).hours_needed(), 42)
    self.assertEqual(Level(rank=9).hours_needed(), 255)
    self.assertEqual(Level(rank=15).hours_needed(), 788)
    self.assertEqual(Level(rank=20).hours_needed(), 1485)

  def test_quest_hours_needed(self):
    self.assertEqual(self.init_quest(0, Quest.SMALL).hours_needed(), 0.0);
    self.assertEqual(self.init_quest(0, Quest.MEDIUM).hours_needed(), 0.0);
    self.assertEqual(self.init_quest(0, Quest.LARGE).hours_needed(), 0.0);
    self.assertEqual(self.init_quest(0, Quest.EXTRA_LARGE).hours_needed(), 0.0);

    self.assertEqual(self.init_quest(1, Quest.SMALL).hours_needed(), 0.25);
    self.assertEqual(self.init_quest(1, Quest.MEDIUM).hours_needed(), 0.5);
    self.assertEqual(self.init_quest(1, Quest.LARGE).hours_needed(), 1.0);
    self.assertEqual(self.init_quest(1, Quest.EXTRA_LARGE).hours_needed(), 1.5);

    self.assertEqual(self.init_quest(4, Quest.SMALL).hours_needed(), 4.0);
    self.assertEqual(self.init_quest(4, Quest.MEDIUM).hours_needed(), 8.0);
    self.assertEqual(self.init_quest(4, Quest.LARGE).hours_needed(), 16.0);
    self.assertEqual(self.init_quest(4, Quest.EXTRA_LARGE).hours_needed(), 24.0);

    self.assertEqual(self.init_quest(9, Quest.SMALL).hours_needed(), 10.25);
    self.assertEqual(self.init_quest(9, Quest.MEDIUM).hours_needed(), 20.5);
    self.assertEqual(self.init_quest(9, Quest.LARGE).hours_needed(), 41.0);
    self.assertEqual(self.init_quest(9, Quest.EXTRA_LARGE).hours_needed(), 61.5);

    self.assertEqual(self.init_quest(15, Quest.SMALL).hours_needed(), 17.75);
    self.assertEqual(self.init_quest(15, Quest.MEDIUM).hours_needed(), 35.5);
    self.assertEqual(self.init_quest(15, Quest.LARGE).hours_needed(), 71.0);
    self.assertEqual(self.init_quest(15, Quest.EXTRA_LARGE).hours_needed(), 106.5);

    self.assertEqual(self.init_quest(20, Quest.SMALL).hours_needed(), 24.0);
    self.assertEqual(self.init_quest(20, Quest.MEDIUM).hours_needed(), 48.0);
    self.assertEqual(self.init_quest(20, Quest.LARGE).hours_needed(), 96.0);
    self.assertEqual(self.init_quest(20, Quest.EXTRA_LARGE).hours_needed(), 144.0);

  def test_quest_xp(self):
    self.assertEqual(self.init_quest(0, Quest.SMALL).xp(), 0);
    self.assertEqual(self.init_quest(0, Quest.MEDIUM).xp(), 0);
    self.assertEqual(self.init_quest(0, Quest.LARGE).xp(), 0);
    self.assertEqual(self.init_quest(0, Quest.EXTRA_LARGE).xp(), 0);

    self.assertEqual(self.init_quest(1, Quest.SMALL).xp(), 5);
    self.assertEqual(self.init_quest(1, Quest.MEDIUM).xp(), 10);
    self.assertEqual(self.init_quest(1, Quest.LARGE).xp(), 20);
    self.assertEqual(self.init_quest(1, Quest.EXTRA_LARGE).xp(), 30);

    self.assertEqual(self.init_quest(4, Quest.SMALL).xp(), 1688);
    self.assertEqual(self.init_quest(4, Quest.MEDIUM).xp(), 3376);
    self.assertEqual(self.init_quest(4, Quest.LARGE).xp(), 6752);
    self.assertEqual(self.init_quest(4, Quest.EXTRA_LARGE).xp(), 10128);

    self.assertEqual(self.init_quest(9, Quest.SMALL).xp(), 25769);
    self.assertEqual(self.init_quest(9, Quest.MEDIUM).xp(), 51537);
    self.assertEqual(self.init_quest(9, Quest.LARGE).xp(), 103074);
    self.assertEqual(self.init_quest(9, Quest.EXTRA_LARGE).xp(), 154611);

    self.assertEqual(self.init_quest(15, Quest.SMALL).xp(), 137279);
    self.assertEqual(self.init_quest(15, Quest.MEDIUM).xp(), 274557);
    self.assertEqual(self.init_quest(15, Quest.LARGE).xp(), 549114);
    self.assertEqual(self.init_quest(15, Quest.EXTRA_LARGE).xp(), 823671);

    self.assertEqual(self.init_quest(20, Quest.SMALL).xp(), 349560);
    self.assertEqual(self.init_quest(20, Quest.MEDIUM).xp(), 699120);
    self.assertEqual(self.init_quest(20, Quest.LARGE).xp(), 1398240);
    self.assertEqual(self.init_quest(20, Quest.EXTRA_LARGE).xp(), 2097360);
