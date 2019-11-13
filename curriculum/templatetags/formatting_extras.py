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
def format_duration(td, singular=False):
    result = ''

    hours = td.seconds // 60 // 60
    if hours > 0:
        hr_separator = ' hour' if not singular else '-hour'
        plural = 's' if hours > 1 and not singular else ''
        result = result + str(hours) + hr_separator + plural

    minutes = (td.seconds - hours * 3600) // 60
    if minutes > 0:
        hr_min_separator = ' and ' if hours > 0 else '' 
        min_separator = ' minute' if not singular else '-minute'
        plural = 's' if minutes > 0 and not singular else ''
        result = result + str(minutes) + hr_min_separator + min_separator + plural
  
    return result
