from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Simulation, Run

User = get_user_model()


class SimulationModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="grace", password="pw12345")
        cls.sim = Simulation.objects.create(
            title="EV Adoption v 1.0",
            description="30% HGVs electrified",
            mode="road",
            is_baseline=False,
            author=cls.user,
        )

    def test_str(self):
        self.assertEqual(str(self.sim), "EV Adoption v 1.0")

    def test_ordering(self):
        older = self.sim
        newer = Simulation.objects.create(
            title="Baseline 2025 v.1",
            description="Baseline",
            mode="road",
            is_baseline=True,
            author=self.user,
        )
        sims = list(Simulation.objects.all())
        self.assertEqual(sims[0], newer)
        self.assertEqual(sims[1], older)


class RunModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="sam", password="pw12345")
        cls.sim = Simulation.objects.create(
            title="Rail Baseline",
            description="Rail baseline case",
            mode="rail",
            is_baseline=True,
            author=cls.user,
        )
        cls.run_obj = Run.objects.create(
            simulation=cls.sim,
            label="baseline-run",
            git_commit="abc123def",
            co2_emissions=12.5,
            author=cls.user,
        )

    def test_str(self):
        self.assertIn("baseline-run", str(self.run_obj))
        self.assertIn("12.5", str(self.run_obj))


class TestViews(TestCase):  # <— renamed so discovery always picks it up
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="grace", password="pw12345")
        self.sim = Simulation.objects.create(
            title="EV Adoption v 1.0",
            description="30% HGVs electrified",
            mode="road",
            is_baseline=False,
            author=self.user,
        )

    # ---- list & detail ----
    def test_simulation_list_ok(self):
        self.client.login(username="grace", password="pw12345")  # if view is protected
        url = reverse("simulation_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Simulations")
        self.assertContains(resp, "EV Adoption v 1.0")

    def test_simulation_detail_ok(self):
        self.client.login(username="grace", password="pw12345")  # if view is protected
        url = reverse("simulation_detail", args=[self.sim.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.sim.title)

    # ---- auth requirements ----
    def test_simulation_create_requires_login(self):
        url = reverse("simulation_create")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login/", resp["Location"])

    def test_run_create_requires_login(self):
        url = reverse("run_create_for_sim", args=[self.sim.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login/", resp["Location"])

    # ---- create flows set author and redirect ----
    def test_create_simulation_sets_author(self):
        self.client.login(username="grace", password="pw12345")
        url = reverse("simulation_create")
        data = {
            "title": "New Scenario",
            "description": "desc",
            "mode": "road",
            "is_baseline": False,
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        sim = Simulation.objects.get(title="New Scenario")
        self.assertEqual(sim.author, self.user)

    def test_create_run_sets_author_and_links_simulation(self):
        self.client.login(username="grace", password="pw12345")
        url = reverse("run_create_for_sim", args=[self.sim.pk])
        data = {
            "simulation": self.sim.pk,
            "label": "run-1",
            "git_commit": "deadbeef",
            "co2_emissions": 9.87,
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        run_obj = Run.objects.get(label="run-1")
        self.assertEqual(run_obj.author, self.user)
        self.assertEqual(run_obj.simulation, self.sim)

    # ---- update flows keep/assign author ----
    def test_update_simulation_keeps_author(self):
        self.client.login(username="grace", password="pw12345")
        url = reverse("simulation_update", args=[self.sim.pk])
        data = {
            "title": "EV Adoption v 1.1",
            "description": "updated",
            "mode": "road",
            "is_baseline": False,
        }
        self.client.post(url, data, follow=True)
        self.sim.refresh_from_db()
        self.assertEqual(self.sim.author.username, "grace")
        self.assertEqual(self.sim.title, "EV Adoption v 1.1")
