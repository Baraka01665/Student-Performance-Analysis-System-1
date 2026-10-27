
import csv
from abc import ABC, abstractmethod
from pathlib import Path


# TASK 2: Abstraction and encapsulation
class Student(ABC):
    def __init__(self, student_id, first_name, last_name,
                 programme, marks):
        self.__student_id = student_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__programme = programme
        self.__marks = self._validate_marks(marks)

    @staticmethod
    def _validate_marks(marks):
        if not marks:
            raise ValueError("Marks cannot be empty.")

        result = {}
        for subject, mark in marks.items():
            mark = float(mark)
            if not 0 <= mark <= 100:
                raise ValueError("Marks must be between 0 and 100.")
            result[subject] = mark
        return result

    @property
    def student_id(self):
        return self.__student_id

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def full_name(self):
        return f"{self.__first_name} {self.__last_name}"

    @property
    def programme(self):
        return self.__programme

    @property
    def marks(self):
        return self.__marks.copy()

    def update_mark(self, subject, mark):
        mark = float(mark)
        if not 0 <= mark <= 100:
            raise ValueError("Mark must be between 0 and 100.")
        self.__marks[subject] = mark

    def calculate_average(self):
        return sum(self.__marks.values()) / len(self.__marks)

    def determine_grade(self):
        average = self.calculate_average()
        if average >= 80:
            return "A"
        elif average >= 70:
            return "B"
        elif average >= 60:
            return "C"
        elif average >= 50:
            return "D"
        return "F"

    # TASK 6: Flexible method interface
    @staticmethod
    def flexible_average(*marks):
        """Average separate marks or a single iterable of marks."""
        if len(marks) == 1 and not isinstance(
                marks[0], (int, float)):
            marks = tuple(marks[0])

        if not marks:
            raise ValueError("At least one mark is required.")

        values = [float(mark) for mark in marks]

        if any(mark < 0 or mark > 100 for mark in values):
            raise ValueError("Marks must be between 0 and 100.")

        return sum(values) / len(values)

    @abstractmethod
    def student_information(self):
        pass


# TASK 2: Inheritance
class AIUStudent(Student):
    def student_information(self):
        return f"AIU Student: {self.full_name}"


# TASK 4: Inheritance and method overriding
class ScholarshipStudent(AIUStudent):
    def __init__(self, student_id, first_name, last_name,
                 programme, marks, scholarship_amount=50000):
        super().__init__(
            student_id, first_name, last_name, programme, marks
        )
        self.scholarship_amount = float(scholarship_amount)

        if self.scholarship_amount < 0:
            raise ValueError("Scholarship cannot be negative.")

    def is_eligible(self):
        return self.calculate_average() >= 85

    # Overridden method
    def student_information(self):
        status = "Eligible" if self.is_eligible() else "Not eligible"
        return (
            f"Scholarship Student: {self.full_name} | "
            f"Status: {status} | "
            f"Amount: KSh {self.scholarship_amount:,.2f}"
        )


# TASK 3: Composition
class PerformanceAnalyzer:
    def __init__(self, students):
        self.students = list(students)

        if not self.students:
            raise ValueError("No student records were provided.")

    def highest_average(self):
        return max(
            self.students,
            key=lambda student: student.calculate_average()
        )

    def lowest_average(self):
        return min(
            self.students,
            key=lambda student: student.calculate_average()
        )

    def class_average(self):
        return sum(
            student.calculate_average()
            for student in self.students
        ) / len(self.students)

    def generate_report(self):
        print("\nSTUDENT PERFORMANCE ANALYSIS REPORT")
        print("=" * 50)

        for student in self.students:
            print(f"\nStudent ID: {student.student_id}")
            print(f"Name: {student.full_name}")
            print(f"Programme: {student.programme}")

            print("Subject marks:")
            for subject, mark in student.marks.items():
                print(f"  {subject}: {mark:.1f}")

            print(f"Average: {student.calculate_average():.2f}%")
            print(f"Grade: {student.determine_grade()}")

            if isinstance(student, ScholarshipStudent):
                status = (
                    "Eligible" if student.is_eligible()
                    else "Not eligible"
                )
                print(f"Scholarship eligibility: {status}")
                print(
                    f"Scholarship amount: "
                    f"KSh {student.scholarship_amount:,.2f}"
                )
            else:
                print("Scholarship eligibility: Not assessed")

            # The overridden method runs according to each object's type.
            print(student.student_information())
            print("-" * 50)

        highest = self.highest_average()
        lowest = self.lowest_average()

        print("\nCLASS PERFORMANCE SUMMARY")
        print(
            f"Highest average: {highest.full_name} - "
            f"{highest.calculate_average():.2f}%"
        )
        print(
            f"Lowest average: {lowest.full_name} - "
            f"{lowest.calculate_average():.2f}%"
        )
        print(f"Class average: {self.class_average():.2f}%")


def load_students(filename):
    students = []

    with open(filename, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        required = {
            "StudentID", "FName", "LName", "Programme",
            "Math", "English", "Science"
        }

        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError("CSV columns are missing.")

        for row in reader:
            marks = {
                "Math": float(row["Math"]),
                "English": float(row["English"]),
                "Science": float(row["Science"])
            }

            average = Student.flexible_average(*marks.values())

            if average >= 85:
                student = ScholarshipStudent(
                    row["StudentID"], row["FName"], row["LName"],
                    row["Programme"], marks
                )
            else:
                student = AIUStudent(
                    row["StudentID"], row["FName"], row["LName"],
                    row["Programme"], marks
                )

            students.append(student)

    if not students:
        raise ValueError("The CSV file contains no records.")

    return students


def main():
    filename = Path(__file__).with_name("students.csv")
    students = load_students(filename)

    analyzer = PerformanceAnalyzer(students)
    analyzer.generate_report()

    print("\nFLEXIBLE METHOD INTERFACE")
    print(Student.flexible_average(70, 80, 90))
    print(Student.flexible_average([70, 80, 90]))

    print("\nPOLYMORPHISM DEMONSTRATION")
    for student in students:
        print(student.student_information())


if __name__ == "__main__":
    main()
