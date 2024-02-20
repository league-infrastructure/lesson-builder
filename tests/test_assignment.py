import pytest
from lesson_builder.lesson import *
from pathlib import Path

lessons_dir = Path(__file__).parent / 'lessons'

def test_load_lesson():
    basic_lesson_dir = lessons_dir / 'basic'
    lesson = LessonPlan(basic_lesson_dir)
