from django.forms.utils import ErrorList


class BootstrapErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return '<ul class="list-unstyled">%s</ul>' % ''.join(['<li>%s</li>' % e for e in self])

