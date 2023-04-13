from backend.models import Note


def get_all_notes():
    return Note.Note.objects.all()


def get_all_notes_count():
    return Note.Note.objects.count()


def get_all_lost_notes_count():
    return Note.Note.objects.filter(deadline_lost=False).count()


def get_all_department_notes(department):
    return Note.Note.objects.filter(employee__department=department).count()


def get_all_lost_department_notes(department):
    return Note.Note.objects.filter(employee__department=department, deadline_lost=False).count()


def count_of_not_filled():
    return Note.Note.objects.filter(datetime_fill=None).count()


def count_of_ill():
    return Note.Note.objects.filter(is_ill=True).count()
