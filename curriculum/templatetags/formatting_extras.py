from django import template
import inflect

register = template.Library()

p = inflect.engine()

@register.simple_tag
def number_to_words(num, capitalize=False):
    word = p.number_to_words(num)
    if capitalize:
        return word.capitalize()
    return word


@register.simple_tag
def format_duration(td):
    result = ''

    hours = td.seconds // 60 // 60
    if hours != 0:
        result = result + str(hours) + 'hr'

    minutes = (td.seconds - hours * 3600) // 60
    if minutes:
        result = result + str(minutes) + 'min'

    return result
