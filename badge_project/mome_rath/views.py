from django.views.generic import TemplateView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import get_user_model

from .models import Badge, Award
from .forms import BadgeCreateForm, BadgeEditForm



class BadgeIndex(TemplateView):
    pass


	# same a 'badge view' in wiki?
class BadgeDetail(TemplateView):
    template_name = "mome_rath/badge_detail.html"

    def get(self, request, slug):
        badge = get_object_or_404(Badge, slug__exact=slug)
        return render(request, self.template_name, {"badge": badge})


class BadgeCreate(CreateView):
    model = Badge
    template_name = "mome_rath/badge_create.html"
    form_class = BadgeCreateForm
 #   success_url = reverse('mome_rath.index')
    #TODO - save current user as 'creator'
'''
    def post(self, request):
        if request.method == 'POST':
            form = BadgeCreateForm(request.POST)
            if form.is_valid():
                form.instance.creator = request.user
                form.save()
                obj = {'posted': True}
                return HttpResponse(json.dumps(obj), mimetype='application/json')
            else:
              return render_to_response('planner/editor.html',
                  form, context_instance=RequestContext(request),)
'''


class BadgeEdit(UpdateView):
    model = Badge
    template_name = "mome_rath/badge_edit.html"
    form_class = BadgeEditForm
#    success_url = reverse('mome_rath.index')


# is this the same as 'Awards view': /user/<username>?
# Shows just the badges a user has earned. Include progresses and nominations? (according to wiki)
class AwardsByUser(TemplateView):
    template_name = "mome_rath/awards_by_user.html"

    def get(self, request, username):
        user = get_object_or_404(get_user_model(), username__exact=username)
        awards = Award.objects.filter(user=user)
        return render(request, self.template_name, {'user': user, 'award_list': awards})


class AwardDetail(TemplateView):
    template_name = "mome_rath/award_detail.html"

    def get(self, request, slug, id):
        badge = get_object_or_404(Badge, slug=slug)
        award = get_object_or_404(Award, badge=badge, pk=id)
        return render(request, self.template_name, {"badge": badge, "award": award})
		
''' untested views from Tyson (troubles simulating server) 15/1/2014 '''
class AwardsByBadge(TemplateView):
	
	# renamed/edited from 'momerath/awards_list.html'
    template_name = "mome_rath/awards_by_badge.html"
		 
	# assumes all awards are visible to all users
	# in urls.py, this requires login (since AwardDetail does)
	def get(self, request, slug):
	    badge = get_object_or_404(Badge, slug=slug)
		awards = Award.objects.filter(badge=badge)
		return render(request, self.template_name, {"badge": badge, "award_list": awards})
		 
''' end of untested views from Tyson '''


#class AwardBadge()