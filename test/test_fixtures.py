
import pytest

class Student:
    def __init__(self, name, age, major, years):
        self.name = name
        self.age = age
        self.major = major
        self.years = years

def test_Student_init():
    student = Student("John", 20, "Computer Science", 3)
    assert student.name == "John"
    assert student.age == 20
    assert student.major == "Computer Science"
    assert student.years == 3

@pytest.fixture
def default_Student():
    return Student("John", 20, "Computer Science", 3)

def test_Student_init_with_defaults(default_Student):
    assert default_Student.name == "John"
    assert default_Student.age == 20
    assert default_Student.major == "Computer Science"
    assert default_Student.years == 3
