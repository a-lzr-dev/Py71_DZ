from django.contrib.auth.decorators import login_required, login_not_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import ListView

from project import settings
from table_reservation.forms import ReservationForm
from table_reservation.models import Reservation, Table

MAX_RESERVATIONS_PER_USER_PER_DAY = getattr(settings, 'MAX_RESERVATIONS_PER_USER_PER_DAY', 1) # Лимит броней на пользователя в день

def home_view(request):
    return render(request, "index.html")

def about_view(request):
    return render(request, "about.html")

# def tables_list_view(request):
#     search = request.GET.get("search", "")
#     page_number = request.GET.get("page", 1)
#     per_page = 2
#
#     table_qs = Table.objects.all()
#     if search:
#         table_qs = table_qs.filter(seats__name__icontains=search)
#     table_qs = table_qs.only("id", "number", "image", "seats")
#
#     paginator = Paginator(table_qs, per_page)
#     page = paginator.get_page(page_number)
#
#     return render(request, "table_reservation/tables_list.html", context={"page": page})

class TablesListView(ListView):
    paginate_by = 10
    template_name = "table_reservation/tables_list.html"

    def get_queryset(self):
        search = self.request.GET.get("search", "")

        table_qs = Table.objects.all()
        if search:
            table_qs = table_qs.filter(date__icontains=search)
        table_qs = table_qs.only("id", "number", "image", "seats")

        return table_qs

# @login_required
# def reservations_list_view(request):
#     search = request.GET.get("search", "")
#     page_number = request.GET.get("page", 1)
#     per_page = 2
#
#     reservation_qs = Reservation.objects.all()
#     if search:
#         reservation_qs = reservation_qs.filter(date__icontains=search)
#
#     reservation_qs = reservation_qs.select_related("user")  # JOIN с users только для FK.
#     reservation_qs = reservation_qs.order_by("-created_at")
#     reservation_qs = reservation_qs.only("id", "date", "hour_start", "hour_end", "created_at", "table__number",
#                                          "user__username")
#
#     paginator = Paginator(reservation_qs, per_page)
#     page = paginator.get_page(page_number)
#
#     return render(request, "table_reservation/reservation_list.html", context={"page": page})

class ReservationsListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    template_name = "table_reservation/reservation_list.html"
    login_url = '/login' # если пользователь не авторизован, его перенаправит на страницу логина

    def get_queryset(self):
        search = self.request.GET.get("search", "")

        reservation_qs = Reservation.objects.all()
        if search:
            reservation_qs = reservation_qs.filter(date__icontains=search)
        reservation_qs = reservation_qs.select_related("user")  # JOIN с users только для FK.
        reservation_qs = reservation_qs.order_by("-created_at")
        reservation_qs = reservation_qs.only("id", "date", "hour_start", "hour_end", "created_at", "table__number",
                                             "user__username")
        return reservation_qs


@login_required
def reservation_create_view(request, table_id: int = None):
    if table_id:
        try:
            table = Table.objects.get(id=table_id)
        except Table.DoesNotExist:
            raise Http404("Table does not exist")

        initial_data = {'table': table}  # передаём объект или его id
    else:
        initial_data = None

    form = ReservationForm(initial=initial_data)

    if request.method == "POST":
        form = ReservationForm(request.POST, request.FILES)
        if form.is_valid():
            table = form.cleaned_data["table"]
            date = form.cleaned_data["date"]
            hour_start = form.cleaned_data["hour_start"]
            hour_end = form.cleaned_data["hour_end"]

            # Проверка на наличие брони для пользователя на указанный день
            user_reservations_count = Reservation.objects.filter(
                user=request.user,
                date=date
            ).count()
            if user_reservations_count >= MAX_RESERVATIONS_PER_USER_PER_DAY:
                form.add_error(
                    None,
                    f"Вы не можете забронировать более {MAX_RESERVATIONS_PER_USER_PER_DAY} столика(ов) на один день."
                )
                return render(request, "table_reservation/create.html", context={"form": form})

            # Проверка на занятость столика в указанное время
            conflicting_reservations = Reservation.objects.filter(
                table=table,
                date=date,
                hour_start__lt=hour_end,  # начинается до окончания новой брони
                hour_end__gt=hour_start  # заканчивается после начала новой брони
            )
            if conflicting_reservations.exists():
                form.add_error(
                    None,  # некорректная ошибка для всего forms.NonFieldErrors
                    "Этот столик уже забронирован на выбранную дату и время."
                )
                return render(request, "table_reservation/create.html", context={"form": form})

            Reservation.objects.create(
                table=form.cleaned_data["table"],
                date=form.cleaned_data["date"],
                hour_start=form.cleaned_data["hour_start"],
                hour_end=form.cleaned_data["hour_end"],
                user=request.user,
            )
            return redirect(resolve_url("reservations-list"))

    return render(request, "table_reservation/create.html", context={"form": form})


@login_required
def reservation_detail_view(request, reservation_id: int):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        raise Http404("Reservation does not exist")

    if request.user != reservation.user:
        raise Http404("Reservation does not exist")

    return render(request, "table_reservation/detail.html", context={"reservation": reservation})