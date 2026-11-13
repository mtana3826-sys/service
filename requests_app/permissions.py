from .models import RepairRequest

def get_visible_requests(user):
    if not user.is_authenticated:
        return RepairRequest.objects.none()

    if user.role == "owner":
        return RepairRequest.objects.all()

    if user.role == "manager":
        if user.branch:
            return RepairRequest.objects.filter(branch=user.branch)
        return RepairRequest.objects.none()

    if user.role == "employee":
        return RepairRequest.objects.filter(created_by=user)

    return RepairRequest.objects.none()