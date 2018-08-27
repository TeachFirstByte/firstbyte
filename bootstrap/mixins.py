from .errorlist import BootstrapErrorList


class FormBootstrapErrorListMixin:
    def get_form_kwargs(self):
        obj = super().get_form_kwargs()
        obj['error_class'] = BootstrapErrorList
        return obj