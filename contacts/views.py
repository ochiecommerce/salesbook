from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Contact, Invite
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import InteractionForm, ContactForm, GroupForm, InviteForm


def register(request: HttpRequest):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("contact_list")

    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def login(request: HttpRequest):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print('username:',email,'password:',password)
        if email and password:
            user = authenticate(request,username=email,password=password)
            if user:
                return redirect("contact_list")
            

    else:
        form = CustomUserForm()
    return render(request, "registration/login.html")


@login_required()
def contact_list(request: HttpRequest):
    query = request.GET.get("q")
    page_number = request.GET.get("page")
    if query:
        contacts = Contact.contacts.filter(
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
        {"query": query, "page_obj": page, "contact_list_active": "active"},
    )


@login_required
def contact_detail(request: HttpRequest, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    interactions = contact.interactions.all().order_by("-timestamp")  # type: ignore
    page_number = request.GET.get("page")
    pagination = Paginator(interactions, 50)
    page = pagination.get_page(page_number)
    return render(
        request,
        "contacts/contact_detail.html",
        {"contact": contact, "page_obj": page},
    )


@login_required
def add_interaction(request: HttpRequest, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    if request.method == "POST":
        form = InteractionForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.contact = contact
            interaction.user = request.user
            interaction.save()
            return redirect("contact_detail", contact_id=contact.id)  # type: ignore
    else:
        form = InteractionForm()
    return render(
        request, "contacts/add_interaction.html", {"form": form, "contact": contact}
    )


@login_required
def add_contact(request: HttpRequest):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=True)

            return redirect("contact_detail", contact_id=contact.id)
    else:
        form = ContactForm()
    return render(request, "contacts/add_contact.html", {"form": form})


@login_required
def group(request: HttpRequest):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.admin_email = request.user.email  # type: ignore
            company.save()
            request.user.company = company  # type: ignore

            request.user.save()
            return redirect("group")
    elif not request.user.company:  # type: ignore
        form = GroupForm()
        return render(
            request, "contacts/group.html", {"group_active": "active", "form": form}
        )

    members = request.user.company.members.all()  # type: ignore
    invites = request.user.invites.all()  # type: ignore
    form = InviteForm()
    return render(
        request,
        "contacts/group.html",
        {
            "group_active": "active",
            "members": members,
            "invites": invites,
            "form": form,
        },
    )


@login_required
def group_invite(request: HttpRequest):
    if request.method == "POST":
        form = InviteForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(CustomUser, form.data.get("username"))
            invite = form.save(commit=False)
            invite.company = request.user.company # type: ignore
            invite.save()

    return render(request, "contacts/group.html", {})


@login_required
def accept_invite(request: HttpRequest, invite_id):
    if request.method == "POST":
        invite = get_object_or_404(Invite, invite_id)
        if invite.user == request.user:
            request.user.company = invite.company  # type: ignore

        return redirect("group")
    return render(request, "create_group.html", {})
