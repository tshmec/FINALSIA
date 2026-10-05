from django.test import TestCase
from django.urls import reverse

from .models import Student

VALID_STUDENT = {
    "student_id": "2024-001",
    "first_name": "Juan",
    "last_name": "Dela Cruz",
    "course": "BS Information Technology",
    "year_level": "3rd Year",
    "email": "juan@email.com",
    "contact_number": "09171234567",
}


def make_student(**overrides):
    data = {**VALID_STUDENT, **overrides}
    return Student.objects.create(**data)


class StudentModelTests(TestCase):
    def test_get_full_name(self):
        student = make_student()

        self.assertEqual(student.get_full_name(), "Juan Dela Cruz")
        self.assertEqual(str(student), "Juan Dela Cruz")


class DashboardTests(TestCase):
    def test_dashboard_shows_empty_state(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_students"], 0)
        self.assertContains(response, "No students found")

    def test_dashboard_shows_existing_records_and_stats(self):
        make_student()
        make_student(
            student_id="2024-002",
            first_name="Maria",
            last_name="Santos",
            course="BS Nursing",
            year_level="1st Year",
            email="maria@email.com",
        )

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2024-001")
        self.assertContains(response, "Juan")
        self.assertContains(response, "2024-002")
        self.assertContains(response, "Maria")
        self.assertEqual(response.context["total_students"], 2)
        self.assertEqual(response.context["total_courses"], 2)
        self.assertEqual(response.context["total_year_levels"], 2)

    def test_search_filters_the_table(self):
        # IDs deliberately differ from the form placeholder text.
        make_student(student_id="2025-100")
        make_student(
            student_id="2025-200",
            first_name="Maria",
            last_name="Santos",
            course="BS Nursing",
            year_level="1st Year",
            email="maria@email.com",
        )

        response = self.client.get(reverse("dashboard"), {"q": "maria"})

        self.assertContains(response, "2025-200")
        self.assertNotContains(response, "2025-100")
        self.assertEqual(len(response.context["students"]), 1)


class AddStudentTests(TestCase):
    def test_add_student_saves_record_and_it_shows_in_the_table(self):
        response = self.client.post(reverse("dashboard"), VALID_STUDENT)

        # A successful add redirects back to the dashboard (PRG pattern).
        # fetch_redirect_response=False keeps the flash message in the
        # session for the assertion below.
        self.assertRedirects(
            response, reverse("dashboard"), fetch_redirect_response=False
        )

        student = Student.objects.get(student_id="2024-001")
        self.assertEqual(student.first_name, "Juan")
        self.assertEqual(student.email, "juan@email.com")

        # The new student pops up in the Student Records table.
        response = self.client.get(reverse("dashboard"))
        self.assertContains(response, "2024-001")
        self.assertContains(response, "Dela Cruz")
        self.assertContains(response, "BS Information Technology")
        self.assertContains(response, "09171234567")
        self.assertContains(response, "was added successfully")
        self.assertEqual(response.context["total_students"], 1)

    def test_missing_fields_redisplays_the_form_with_errors(self):
        response = self.client.post(
            reverse("dashboard"),
            {"student_id": "", "first_name": "Juan", "last_name": "Dela Cruz"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.count(), 0)

        form = response.context["form"]
        self.assertIn("student_id", form.errors)
        self.assertIn("course", form.errors)
        self.assertContains(response, "Please fix the errors")
        self.assertContains(response, "This field is required.")

    def test_duplicate_student_id_is_rejected(self):
        make_student()

        response = self.client.post(reverse("dashboard"), VALID_STUDENT)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.count(), 1)
        self.assertIn("student_id", response.context["form"].errors)

    def test_duplicate_email_is_rejected(self):
        make_student()

        response = self.client.post(
            reverse("dashboard"), {**VALID_STUDENT, "student_id": "2024-999"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.count(), 1)
        self.assertIn("email", response.context["form"].errors)


class DeleteStudentTests(TestCase):
    def test_delete_student_removes_the_record(self):
        student = make_student()

        response = self.client.post(
            reverse("delete_student", args=[student.pk])
        )

        self.assertRedirects(
            response, reverse("dashboard"), fetch_redirect_response=False
        )
        self.assertEqual(Student.objects.count(), 0)
        self.assertContains(
            self.client.get(reverse("dashboard")), "was deleted"
        )

