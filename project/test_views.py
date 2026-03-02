from django.test import Client, TestCase
from django.urls import reverse
from django.utils import translation

from project.models import PlantProfile, ProjectUser


class SearchPlantNameTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.plant1 = PlantProfile.objects.create(
            latin_name="Abies balsamea", seed_availability=True
        )
        self.plant2 = PlantProfile.objects.create(latin_name="Betula papyrifera")
        self.search_url = reverse("search-plant-name")

    def test_empty_search_returns_no_results(self):
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 0)
        self.assertTemplateUsed(response, "project/plant-catalog.html")

    def test_search_returns_correct_plant(self):
        response = self.client.get(
            self.search_url + "?seed_availability=available-seed"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 1)
        plant = response.context["object_list"][0]
        self.assertEqual(plant.latin_name, "Abies balsamea")

    def test_search_returns_all_plants_ordered(self):
        response = self.client.get(self.search_url + "?any_name=")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 2)
        plants = list(response.context["object_list"])
        self.assertEqual(plants[0].latin_name, "Abies balsamea")
        self.assertEqual(plants[1].latin_name, "Betula papyrifera")

    def test_htmx_request_uses_different_template(self):
        response = self.client.get(self.search_url, headers={"hx-request": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project/plant-search-results.html")

    def test_context_contains_required_data(self):
        response = self.client.get(self.search_url)
        self.assertIn("search_filter", response.context)
        self.assertIn("object_list", response.context)
        self.assertEqual(response.context["url_name"], "index")
        self.assertEqual(response.context["title"], "Plant Profile Filter")


class DiscussionViewsTest(TestCase):
    def setUp(self):
        translation.activate("en")
        self.client = Client()
        self.user = ProjectUser.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.other_user = ProjectUser.objects.create_user(
            username="otheruser", password="testpass123"
        )
        from project.models import Discussion, DiscussionReply
        self.Discussion = Discussion
        self.DiscussionReply = DiscussionReply
        self.discussion = Discussion.objects.create(
            title="Test Discussion",
            body="This is a test discussion body.",
            author=self.user,
        )
        self.list_url = reverse("discussion-list")
        self.detail_url = reverse("discussion-detail", kwargs={"pk": self.discussion.pk})
        self.create_url = reverse("discussion-create")
        self.delete_url = reverse("discussion-delete", kwargs={"pk": self.discussion.pk})

    def tearDown(self):
        translation.deactivate()

    def test_discussion_list_returns_200(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project/discussion-list.html")

    def test_discussion_list_shows_discussions(self):
        response = self.client.get(self.list_url)
        self.assertIn(self.discussion, response.context["discussions"])

    def test_discussion_detail_returns_200(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project/discussion-detail.html")

    def test_discussion_detail_shows_correct_discussion(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.context["discussion"], self.discussion)

    def test_discussion_create_requires_login(self):
        response = self.client.get(self.create_url)
        self.assertNotEqual(response.status_code, 200)

    def test_discussion_create_authenticated(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

    def test_discussion_create_post(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(self.create_url, {
            "title": "New Discussion",
            "body": "New discussion body",
        })
        self.assertEqual(self.Discussion.objects.count(), 2)
        new = self.Discussion.objects.get(title="New Discussion")
        self.assertRedirects(response, reverse("discussion-detail", kwargs={"pk": new.pk}))

    def test_discussion_reply_requires_login(self):
        reply_url = reverse("discussion-reply-create", kwargs={"pk": self.discussion.pk})
        response = self.client.post(reply_url, {"body": "A reply"})
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(self.DiscussionReply.objects.count(), 0)

    def test_discussion_reply_create(self):
        self.client.login(username="testuser", password="testpass123")
        reply_url = reverse("discussion-reply-create", kwargs={"pk": self.discussion.pk})
        response = self.client.post(reply_url, {"body": "A reply"})
        self.assertEqual(self.DiscussionReply.objects.count(), 1)
        self.assertRedirects(response, self.detail_url)

    def test_discussion_delete_requires_login(self):
        response = self.client.post(self.delete_url)
        self.assertEqual(self.Discussion.objects.count(), 1)

    def test_discussion_delete_by_author(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(self.delete_url)
        self.assertEqual(self.Discussion.objects.count(), 0)
        self.assertRedirects(response, self.list_url)

    def test_discussion_delete_by_non_author_forbidden(self):
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.post(self.delete_url)
        self.assertEqual(self.Discussion.objects.count(), 1)
        self.assertRedirects(response, self.detail_url)
