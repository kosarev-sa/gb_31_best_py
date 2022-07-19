import json

from django.core.management import BaseCommand

from approvals.models import ApprovalStatus
from relations.models import RelationStatus, RelationHistory, Relations
from search.models import Languages, LanguageLevels, MainSkills, Category, WorkSchedules, Employments
from users.models import Role

JSON_PATH_SEARCH = 'search/fixtures/'
JSON_PATH_APPROVAL = 'approvals/fixtures/'
JSON_PATH_ROLES = 'users/fixtures/'
JSON_PATH_RELATIONS = 'relations/fixtures/'


def load_from_json(file_name):
    with open(file_name, mode='r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):

        # Роли раскомитить на проде. На dev роли создаются в fill_test_user.
        roles = load_from_json(JSON_PATH_ROLES + 'roles.json')
        Role.objects.all().delete()

        for role in roles:
            new_role = Role(pk=role['pk'],
                            role_name=role['role_name'])
            new_role.save()

        languages = load_from_json(JSON_PATH_SEARCH + 'languages.json')
        Languages.objects.all().delete()

        for l in languages:
            j_lang = {}
            j_lang['code'] = l.get('code')
            j_lang['language'] = l.get('language')
            new_lang = Languages(**j_lang)
            new_lang.save()

        levels = load_from_json(JSON_PATH_SEARCH + 'languagelevel.json')
        LanguageLevels.objects.all().delete()

        for l in levels:
            j_level = {}
            j_level['code'] = l.get('code')
            j_level['level'] = l.get('level')
            new_level = LanguageLevels(**j_level)
            new_level.save()

        employments = load_from_json(JSON_PATH_SEARCH + 'employments.json')
        Employments.objects.all().delete()

        for e in employments:
            j_empl = {}
            j_empl['code'] = e.get('code')
            j_empl['employment'] = e.get('employment')
            new_empl = Employments(**j_empl)
            new_empl.save()

        schedules = load_from_json(JSON_PATH_SEARCH + 'work_schedules.json')
        WorkSchedules.objects.all().delete()

        for sch in schedules:
            j_sch = {}
            j_sch['code'] = sch.get('code')
            j_sch['schedule'] = sch.get('schedule')
            new_sch = WorkSchedules(**j_sch)
            new_sch.save()

        skills = load_from_json(JSON_PATH_SEARCH + 'main_skills.json')
        MainSkills.objects.all().delete()

        for s in skills:
            j_skill = {}
            j_skill['code'] = s.get('code')
            j_skill['skill'] = s.get('skill')
            new_skill = MainSkills(**j_skill)
            new_skill.save()

        categories = load_from_json(JSON_PATH_SEARCH + 'categories.json')
        Category.objects.all().delete()

        for c in categories:
            j_cat = {}
            j_cat['code'] = c.get('code')
            j_cat['name'] = c.get('name')
            new_cat = Category(**j_cat)
            new_cat.save()

        approvals = load_from_json(JSON_PATH_APPROVAL + 'status.json')
        ApprovalStatus.objects.all().delete()

        for approval in approvals:
            appr = approval.get('fields')
            appr['id'] = approval.get('pk')
            new_appr = ApprovalStatus(**appr)
            new_appr.save()

        relations = load_from_json(JSON_PATH_RELATIONS + 'relationrtatus.json')
        RelationHistory.objects.all().delete()
        Relations.objects.all().delete()
        RelationStatus.objects.all().delete()

        for relation in relations:
            rel = relation.get('fields')
            rel['id'] = relation.get('pk')
            new_rel = RelationStatus(**rel)
            new_rel.save()
