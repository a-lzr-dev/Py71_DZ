from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.db.transaction import atomic
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from notes.filters import filter_notes_list
from notes.forms import CreateNoteForm, CommentForm, NotesSearchForm, NoteReactionForm
from notes.models import Note, Comment, NoteReaction
from notes.services import set_note_reaction


def home_view(request):
    return render(request, "index.html")


def about_view(request):
    return render(request, "about.html")


# --------------------------------------- NOTES LIST ---------------------------------------


def notes_list_view(request):
    search = request.GET.get("search", "")
    page_number = request.GET.get("page", "1")
    per_page = 10

    notes_qs = filter_notes_list(search)

    paginator = Paginator(notes_qs, per_page)
    page = paginator.get_page(page_number)

    return render(
        request,
        "posts/list.html",
        context={"page": page, "search_form": NotesSearchForm()},
    )


class NotesListView(ListView):
    paginate_by = 10
    template_name = "posts/list.html"

    def get_queryset(self):
        form = NotesSearchForm(self.request.GET)
        if form.is_valid():
            return filter_notes_list(
                search=form.cleaned_data["search"],
                user=form.cleaned_data["user"],
                tags=form.cleaned_data["tags"],
                time_gt=form.cleaned_data["time_gt"],
            )
        return filter_notes_list()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({"search_form": NotesSearchForm(self.request.GET)})
        return context


# --------------------------------------- CREATE NOTE ---------------------------------------


@login_required
def note_create_view(request):
    form = CreateNoteForm()

    if request.method == "POST":
        form = CreateNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = Note.objects.create(
                title=form.cleaned_data["title"],
                content=form.cleaned_data["content"],
                image=form.cleaned_data["image"],
                user=request.user,
            )
            note.tags.set(form.cleaned_data["tags"])
            return redirect(resolve_url("notes:detail", note_id=note.id))

    return render(request, "posts/create.html", context={"form": form})


@method_decorator(login_required, name="dispatch")
class NoteCreateView(CreateView):
    template_name = "posts/create.html"
    form_class = CreateNoteForm

    def form_valid(self, form):
        with atomic():
            self.object = Note.objects.create(
                title=form.cleaned_data["title"],
                content=form.cleaned_data["content"],
                image=form.cleaned_data["image"],
                user=self.request.user,
            )
            self.object.tags.set(form.cleaned_data["tags"])

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return resolve_url("notes:detail", note_id=self.object.id)


# --------------------------------------- DETAIL NOTE ---------------------------------------


def note_detail_view(request, note_id: int):
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        raise Http404("Note does not exist")

    page_number = request.GET.get("page", "1")
    per_page = 5

    paginator = Paginator(Comment.objects.filter(note=note), per_page)
    page = paginator.get_page(page_number)

    if request.user.is_authenticated:
        reaction = NoteReaction.objects.filter(note=note, user=request.user).first()
    else:
        reaction = None

    reaction_stats = NoteReaction.objects.filter(note=note).aggregate(
        likes_count=Count("reaction", filter=Q(reaction="LIKE")),
        dislikes_count=Count("reaction", filter=Q(reaction="DISLIKE")),
    )

    # ============= Просмотренные =================
    session_key = "read_notes"
    if not request.session.get(session_key):
        request.session[session_key] = []

    if note.id in request.session[session_key]:
        request.session[session_key].remove(note.id)

    request.session[session_key].append(note.id)
    request.session.modified = True
    # =============================================

    return render(
        request,
        "posts/detail.html",
        context={
            "note": note,
            "comment_form": CommentForm(),
            "comments_page": page,
            "reaction": reaction,
            "reactions_stats": reaction_stats,
        },
    )


# --------------------------------------- COMMENTS ---------------------------------------


@login_required
def create_note_comment_view(request, note_id: int):
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        raise Http404("Note does not exist")

    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                user=request.user,
                note=note,
                text=form.cleaned_data["text"],
            )

            return redirect(resolve_url("notes:detail", note_id=note.id) + "#comments")

    return render(
        request,
        "posts/detail.html",
        context={"note": note, "comment_form": form},
    )


# --------------------------------------- NOTE REACTION ---------------------------------------


@login_required
def set_note_reaction_view(request, note_id: int):
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        raise Http404("Note does not exist")

    if request.method != "POST":
        return redirect(resolve_url("notes:detail", note_id=note.id))

    form = NoteReactionForm(request.POST)
    if form.is_valid():
        set_note_reaction(note, request.user, form.cleaned_data["reaction"])

    return redirect(resolve_url("notes:detail", note_id=note.id))
