from pathlib import Path

from lesson_builder.lesson_plan import LessonPlan

lessons_dir = Path(__file__).parent / 'lessons'
docs_dir = Path(__file__).parent / 'docs'

def test_load_lesson():
    basic_lesson_dir = lessons_dir / 'basic'
    plan = LessonPlan(basic_lesson_dir, docs_dir)
    for i, l in enumerate(plan.lessons):
        print("Lesson", i, l.name)
        for a in l.assignments:
            print("  ", a.name)

def test_load_assignment():
    basic_lesson_dir = lessons_dir / 'basic'
    plan = LessonPlan(basic_lesson_dir, docs_dir)
    for i, l in enumerate(plan.lessons):
        pass # We just want the last lesson

    print(l.name)

    from lesson_builder.assignment import Assignment

    a = Assignment(l, l.src_dir / 'basic_dir')
    print(a.title)

    a = Assignment(l, l.src_dir / 'basic_file.md')
    print(a.title, a.name)


if __name__ == '__main__':
    test_load_assignment()
