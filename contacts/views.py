from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from .models import Contact
from django.contrib.auth.decorators import login_required
from .forms import InteractionForm, ContactForm


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("contact_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def contact_list(request):
    query = request.GET.get("q")
    page_number = request.GET.get("page")
    if query:
        contacts = Contact.objects.filter(
            Q(name__icontains=query)
            | Q(employment_number__icontains=query)
            | Q(employer_name__icontains=query)
        )

    else:
        contacts = Contact.objects.all()

    query = query if query else ""
    pagination = Paginator(contacts.order_by("name"), 50)
    page = pagination.get_page(page_number)
    return render(
        request,
        "contacts/contact_list.html",
        {"query": query, "page_obj": page},
    )


@login_required
def contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    interactions = contact.interactions.all().order_by("-timestamp")
    page_number = request.GET.get("page")
    pagination = Paginator(interactions, 50)
    page = pagination.get_page(page_number)
    return render(
        request,
        "contacts/contact_detail.html",
        {"contact": contact, "page_obj": page},
    )


@login_required
def add_interaction(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    if request.method == "POST":
        form = InteractionForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.contact = contact
            interaction.user = request.user
            interaction.save()
            return redirect("contact_detail", contact_id=contact.id)
    else:
        form = InteractionForm()
    return render(
        request, "contacts/add_interaction.html", {"form": form, "contact": contact}
    )


@login_required
def add_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=True)

            return redirect("contact_detail", contact_id=contact.id)
    else:
        form = ContactForm()
    return render(request, "contacts/add_contact.html", {"form": form})
