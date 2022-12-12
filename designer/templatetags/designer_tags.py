from django import template
from tests.models import TestsSection

register = template.Library()

@register.simple_tag()
def get_num_section_in_test(test_slug):
    return len(TestsSection.objects.filter(test__slug=test_slug))
