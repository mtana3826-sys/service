from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST

from .models import RepairRequest
from .forms import RepairRequestForm
from .permissions import get_visible_requests

@login_required
def request_list(request):
    requests = get_visible_requests(request.user)
    return render(request, "requests_app/list.html", {"requests": requests})

@login_required
def request_detail(request, pk):
    repair_request = get_object_or_404(
        get_visible_requests(request.user),
        pk=pk
    )
    return render(
        request,
        "requests_app/detail.html",
        {"repair_request": repair_request}
    )

@login_required
def request_create(request):
    if request.user.role != "employee" or not request.user.branch:
        return HttpResponseForbidden("Нет доступа")

    if request.method == "POST":
        form = RepairRequestForm(request.POST, request.FILES)
        if form.is_valid():
            repair_request = form.save(commit=False)
            repair_request.created_by = request.user
            repair_request.branch = request.user.branch
            repair_request.save()
            return redirect("request_list")
    else:
        form = RepairRequestForm()

    return render(request, "requests_app/create.html", {"form": form})

@login_required
@require_POST
def update_status(request, pk):
    if request.user.role != "manager":
        return HttpResponseForbidden("Менять статусы может только управляющий")

    repair_request = get_object_or_404(
        get_visible_requests(request.user),
        pk=pk
    )

    next_status = {
        "new": "in_progress",
        "in_progress": "done",
    }

    if request.POST.get("status") != next_status.get(repair_request.status):
        return HttpResponseForbidden("Недопустимый переход статуса")

    repair_request.status = request.POST["status"]
    repair_request.save(update_fields=["status"])

    return redirect("request_detail", pk=pk)