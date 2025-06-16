
from django.views.generic import TemplateView,ListView,FormView
from django.shortcuts import get_object_or_404,render
from datetime import datetime
from scmtracker.forms import PostModerationForm
from scmtracker.models import APPROVE_LABEL_CHOICES, REJECT_LABEL_CHOICES, ModerationStream, PostModeration
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.dateparse import parse_time
from django.utils import timezone
from datetime import datetime, timedelta, time as dtime
from django.db.models import Q

class HomePageView(TemplateView):
    template_name = "scm/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year"] = datetime.now().year
        return context
    
class StreamListView(ListView):
    model=ModerationStream
    template_name='scm/streamlist.html'
    context_object_name= 'streams'

class ModerationFormView(LoginRequiredMixin, FormView):
    form_class = PostModerationForm
    template_name = "scm/moderation-form.html"

    def dispatch(self, request, *args, **kwargs):
        self.stream = get_object_or_404(ModerationStream, pk=self.kwargs["stream_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial["moderation_stream"] = self.stream
        return initial

    def form_valid(self, form):
        # Get IDs from form.cleaned_data
        curalate_image_id = form.cleaned_data.get('curalate_image_id')
        curalate_post_id = form.cleaned_data.get('curalate_post_id')

        # Check for duplicates in PostModeration
        duplicates = PostModeration.objects.filter(
            Q(curalate_image_id=curalate_image_id) | Q(curalate_post_id=curalate_post_id)
        ).exists()

        if duplicates:
            # Add non-field error to form and re-render with errors
            form.add_error(None, "Duplicate entry found for curalate_image_id or curalate_post_id.")
            return self.form_invalid(form)

        # No duplicates found, proceed to save
        moderation = form.save(commit=False)
        moderation.moderation_stream = self.stream
        moderation.agent_name = (
            self.request.user.get_full_name() or self.request.user.username
        )

        # Parse start_time and end_time from POST (hidden inputs)
        start_time_str = self.request.POST.get("start_time")
        end_time_str = self.request.POST.get("end_time")

        if start_time_str:
            moderation.start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
        if end_time_str:
            moderation.end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()

        moderation.save()
        form.save_m2m()

        # Define moderation window: today 14:00 to tomorrow 12:00
        now = timezone.localtime()
        today = now.date()
        start_datetime = timezone.make_aware(datetime.combine(today, dtime(hour=14, minute=0)))
        end_datetime = timezone.make_aware(datetime.combine(today + timedelta(days=1), dtime(hour=12, minute=0)))

        # If current time is before 14:00, move window back by 1 day
        if now < start_datetime:
            start_datetime -= timedelta(days=1)
            end_datetime -= timedelta(days=1)

        total_moderations = PostModeration.objects.filter(
            agent_name=moderation.agent_name,
            moderation_date__range=(start_datetime, end_datetime)
        ).count()

        return render(
            self.request,
            "scm/post-moderation-success.html",
            {
                "moderation": moderation,
                "stream": self.stream,
                "current_datetime": now,
                "total_moderations": total_moderations,
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stream"] = self.stream
        context["approve_choices"] = [[v, v] for v in APPROVE_LABEL_CHOICES]
        context["reject_choices"] = [[v, v] for v in REJECT_LABEL_CHOICES]
        return context
    
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy    
class RegisterView(FormView):
    template_name = 'scm/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login') 

    def form_valid(self, form):
        form.save()
        return super().form_valid(form) 

def tracker_table(request):
    # Query all records — add filtering here if needed later
    records = PostModeration.objects.all().order_by('-moderation_date')

    return render(request, 'scm/datatable.html', {
        'records': records,
    })

class PostSearchView(ListView):
    model = PostModeration
    template_name = 'scm/search-post.html'
    context_object_name = 'records'

    def get_queryset(self):
        query = self.request.GET.get('curalate_post_id', '').strip()
        if query:
            return PostModeration.objects.filter(curalate_post_id=query)
        return PostModeration.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('curalate_post_id', '').strip()
        return context

       