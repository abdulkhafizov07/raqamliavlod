from django import template

register = template.Library()

@register.simple_tag
def course_process(user, course_id):
    try:
        course_relation = user.related_courses.get(course__id=course_id)
        complated_parts = user.completed_parts.filter(course_part__course_id=course_id, complated=True).count()
        course_parts = course_relation.course.parts.count()
        if course_parts == 0:
            return 0
        return int(complated_parts / (course_parts / 100))
    except Exception as e:
        print(e)
        return 0  # or optionally: return f"Error: {str(e)}"
