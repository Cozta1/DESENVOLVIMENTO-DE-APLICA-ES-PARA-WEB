from django.contrib import admin

from .models import Curso, Professor, Aluno, Disciplina, Turma


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'carga_horaria')
@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'titulacao')

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'curso')

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'carga_horaria')

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('ano', 'semestre', 'disciplina')