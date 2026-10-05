from django import forms

from .models import Student


class StudentForm(forms.ModelForm):
    """Form used by the dashboard to create a new student record."""

    class Meta:
        model = Student
        fields = [
            "student_id",
            "first_name",
            "last_name",
            "course",
            "year_level",
            "email",
            "contact_number",
        ]
        widgets = {
            "student_id": forms.TextInput(
                attrs={"placeholder": "e.g. 2024-001", "autofocus": True}
            ),
            "first_name": forms.TextInput(attrs={"placeholder": "e.g. Juan"}),
            "last_name": forms.TextInput(attrs={"placeholder": "e.g. Dela Cruz"}),
            "course": forms.TextInput(
                attrs={"placeholder": "e.g. BS Information Technology"}
            ),
            "year_level": forms.Select(),
            "email": forms.EmailInput(attrs={"placeholder": "e.g. juan@email.com"}),
            "contact_number": forms.TextInput(
                attrs={"placeholder": "e.g. 09171234567"}
            ),
        }
        labels = {
            "student_id": "Student ID",
            "first_name": "First Name",
            "last_name": "Last Name",
            "course": "Course",
            "year_level": "Year Level",
            "email": "Email Address",
            "contact_number": "Contact Number",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Student.year_level is a plain CharField, so a Select widget alone
        # would render an empty dropdown. Swap in a real choice field so the
        # year level dropdown actually has options.
        year_levels = ["1st Year", "2nd Year", "3rd Year", "4th Year"]

        self.fields["year_level"] = forms.TypedChoiceField(
            label=self.fields["year_level"].label,
            required=True,
            choices=[("", "Select year level")]
            + [(level, level) for level in year_levels],
            widget=forms.Select(),
        )

