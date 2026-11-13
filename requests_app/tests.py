from django.test import TestCase
from django.urls import reverse
from .models import RepairRequest
from accounts.models import User, Branch

class RepairRequestTests(TestCase):

    def setUp(self):
        self.a = Branch.objects.create(name="Точка А")
        self.b = Branch.objects.create(name="Точка Б")

        self.employee_a = User.objects.create_user(
            phone="100", password="test123",
            role="employee", branch=self.a
        )

        self.employee_b = User.objects.create_user(
            phone="200", password="test123",
            role="employee", branch=self.b
        )

        self.manager_a = User.objects.create_user(
            phone="300", password="test123",
            role="manager", branch=self.a
        )

        self.manager_b = User.objects.create_user(
            phone="400", password="test123",
            role="manager", branch=self.b
        )

        self.owner = User.objects.create_user(
            phone="500", password="test123",
            role="owner"
        )

        self.request_a = RepairRequest.objects.create(
            created_by=self.employee_a,
            branch=self.a,
            description="Поломка в точке А",
            urgency="high",
            photo="requests/test.jpg"
        )

        self.request_b = RepairRequest.objects.create(
            created_by=self.employee_b,
            branch=self.b,
            description="Поломка в точке Б",
            urgency="medium",
            photo="requests/test.jpg"
        )

    def test_employee_sees_only_own_requests(self):
        self.client.force_login(self.employee_a)
        response = self.client.get(reverse("request_list"))

        self.assertContains(response, "Поломка в точке А")
        self.assertNotContains(response, "Поломка в точке Б")

    def test_manager_sees_only_own_branch(self):
        self.client.force_login(self.manager_a)
        response = self.client.get(reverse("request_list"))

        self.assertContains(response, "Поломка в точке А")
        self.assertNotContains(response, "Поломка в точке Б")

    def test_manager_cannot_open_other_branch_request(self):
        self.client.force_login(self.manager_a)

        response = self.client.get(
            reverse("request_detail", args=[self.request_b.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_owner_sees_all_requests(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("request_list"))

        self.assertContains(response, "Поломка в точке А")
        self.assertContains(response, "Поломка в точке Б")

    def test_only_manager_can_change_status(self):
        self.client.force_login(self.employee_a)

        response = self.client.post(
            reverse("update_status", args=[self.request_a.pk]),
            {"status": "in_progress"}
        )

        self.assertEqual(response.status_code, 403)

    def test_manager_can_change_status(self):
        self.client.force_login(self.manager_a)

        response = self.client.post(
            reverse("update_status", args=[self.request_a.pk]),
            {"status": "in_progress"}
        )

        self.assertEqual(response.status_code, 302)

        self.request_a.refresh_from_db()
        self.assertEqual(self.request_a.status, "in_progress")