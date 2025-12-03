from django import template

register = template.Library()

@register.simple_tag
def has_complated(user, course_part):
    return user.completed_parts.filter(user=user, course_part=course_part, complated=True).exists()
