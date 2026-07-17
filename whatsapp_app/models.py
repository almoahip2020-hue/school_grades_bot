from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True, verbose_name="الرقم الأكاديمي")
    name = models.CharField(max_length=100, verbose_name="اسم الطالب")
    parent_phone = models.CharField(max_length=20, verbose_name="رقم هاتف ولي الأمر (بصيغة دولية)")

    def __str__(self):
        return f"{self.name} ({self.student_id})"

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades', verbose_name="الطالب")
    subject = models.CharField(max_length=50, verbose_name="المادة الدراسية")
    score = models.DecimalField(max_length=5, max_digits=5, decimal_places=2, verbose_name="الدرجة")
    max_score = models.DecimalField(max_length=5, max_digits=5, decimal_places=2, default=100.00, verbose_name="الدرجة الكبرى")

    def __str__(self):
        return f"{self.subject}: {self.score}/{self.max_score} - {self.student.name}"