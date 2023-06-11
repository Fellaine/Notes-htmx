from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
# from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.db.models import Q
from django.urls import reverse

from .models import Note
from .forms import Note_form

# from .forms import NoteForm, DeleteForm

# class Notes_view(ListView):
#     model = Note
#     form = Note_form
#     template_name = "main/notes_list.html"
#
# class Note_view(DetailView):
#     model = Note
#     form = Note_form
#     template_name = "main/note_view.html"
#
# class Note_create_view(CreateView):
#     model = Note
#     form = Note_form
#     # fields = ['title', 'content']
#     template_name = "main/create.html"
#     success_url = '/'
#
# class Note_delete_view(DeleteView):
#     model = Note
#     form = Note_form
#     # fields = ['title', 'content']
#     template_name = "main/delete.html"
#     success_url = '/'

@login_required(redirect_field_name=None)
def home_view(request):
    notes = Note.objects.filter(user=request.user)
    context = \
        {
            "notes": notes[::-1]
        }
    template_name = "main/notes_list.html"
    return render(request, template_name, context)


@login_required(redirect_field_name=None)
def create_view(request):
    template_name = "main/create.html"
    if request.method == "POST":
        form = Note_form(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            # form = Note_form()
            messages.success(request, "Note added successfully")
            # context = \
            #     {
            #         "form": form
            #     }
            return redirect('index')
            # return render(request, template_name, context)
    else:
        form = Note_form()
        form.helper.form_action = "create"
        context = \
            {
                "form": form
            }
    return render(request, template_name, context)


@login_required(redirect_field_name=None)
def edit_view(request, id):
    note = get_object_or_404(Note, id=id)
    if note.user != request.user:
        messages.error(request, "You are not allowed to access this page")
        return redirect('/')
    if request.method == "POST":
        form = Note_form(request.POST, instance=note)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            form = Note_form()
            messages.success(request, "Note edited successfully")
            return redirect('index')
    else:
        initial_data = {'title': note.title, 'content': note.content}
        form = Note_form(initial=initial_data, instance=note)
        form.helper.form_action = f"/notes/{ id }/"
        context = \
            {
                "form": form,
                "id": id
            }
        return render(request, "main/edit.html", context)


class HTTPResponseHXRedirect(HttpResponseRedirect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["HX-Redirect"] = self["Location"]

    status_code = 200

@login_required(redirect_field_name=None)
def delete_view(request, id):
    note = get_object_or_404(Note, id=id)
    if note.user != request.user:
        messages.error(request, "You are not allowed to access this page")
        return redirect('index')
    # if request.method == "POST":
    #     note.delete()
    #     messages.success(request, "Note deleted successfully")
    #     return redirect('index')
    if request.method == "DELETE":
        note.delete()
        messages.success(request, "Note deleted successfully")
        return HTTPResponseHXRedirect(redirect_to=reverse("index"))
    else:
        context = \
            {
                "title": note.title,
                "id": id
            }
        if len(context["title"]) >= 13:
            context["title"] = context["title"][:10] + "..."
        return render(request, "main/delete.html", context)


def empty_view(request):
    return HttpResponse("")


def search_view(request):
    search_data = request.POST.get('search')
    if search_data:
        #print(search_data)
        # res = Note.objects.filter(title__icontains=search_data, content__icontains=search_data)
        # ress = Note.objects.filter(Q(user=request.user) & Q(title__icontains=search_data) | Q(content__icontains=search_data))
        res = Note.objects.filter((Q(title__icontains=search_data) & Q(user=request.user))
                                  | (Q(content__icontains=search_data) & Q(user=request.user)))

        if not res:
            return HttpResponse("<p>Not found</p>")
        #res = Note.objects.annotate(search=SearchVector('title', 'content')).filter(search=search_data)
        context = \
            {
                "results": res
            }
        return render(request, "main/search.html", context)
