from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect


class SuperuserCheckMixin():
    form = None
    template = None
    
    def get(self, request):
        if not request.user.is_superuser:
            return HttpResponseRedirect('/login/')
        form = self.form
        context = {}
        if form:
            context = {'form': form}
        return render(request, self.template, context)