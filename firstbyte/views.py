from django.shortcuts import get_object_or_404, redirect

def slug_redirect_view(klass, to=None, permanent=True, *args, **kwargs):
    def view_fn(request, pk):
        obj = get_object_or_404(klass, id=pk)
        return redirect(obj, *args, pk=pk, slug=obj.slug, permanent=permanent, **kwargs)
    return view_fn

