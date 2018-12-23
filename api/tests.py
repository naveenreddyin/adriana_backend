import os

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from api.models import Topic


class ApiTestCases(APITestCase):

    def test_topic_model(self):
        """
        This will test the Topic model
        """
        self.assertEqual(self.check_count(), 0)
        # Insert parent node and also check if parent could be null
        parent_node = Topic.objects.create(text="Are you hungry?")
        self.assertEqual(parent_node.pk, 1)
        self.assertEqual(self.check_count(), 1)

        # Now test adding the children
        child_yes = Topic.objects.create(text="Yes", parent=parent_node)
        self.assertEqual(child_yes.pk, 2)
        self.assertEqual(self.check_count(), 2)

        child_no = Topic.objects.create(text="No", parent=parent_node)
        self.assertEqual(child_no.pk, 3)
        self.assertEqual(self.check_count(), 3)

        child_no_child = Topic.objects.create(
            text="Ok. Call me when you're hungry.", parent=child_no)
        self.assertEqual(child_no_child.pk, 4)
        self.assertEqual(self.check_count(), 4)

    def check_count(self):
        """
        Simple util method to get count of Topic model
        """
        topics = Topic.objects.all()
        return len(topics)

    def create_topics(self):
        parent_node = Topic.objects.create(text="Are you hungry?")
        child_yes = Topic.objects.create(text="Yes", parent=parent_node)
        child_no = Topic.objects.create(text="No", parent=parent_node)
        child_no_child = Topic.objects.create(
            text="Ok. Call me when you're hungry.", parent=child_no)

    def test_topic_list_api_view(self):
        """
        This will test the api view
        """
        # call method to create topics on demand
        self.create_topics()
        client = APIClient()
        # call the api and should return only 1 as response data if no other kwargs are provided.
        response = client.get('/api/v1/topic/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        # Now calling with only one more param, i.e parent_id should return 404 as status code
        response = client.get('/api/v1/topic/1/')
        self.assertEqual(response.status_code, 404)

        # Now calling with other two params, namely parent_id and text and it should return one object and status 200
        response = client.get('/api/v1/topic/1/Yes/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_not_more_than_5_answers(self):
        """
        One of the condition is to not have more than 5 answers or children for a question or topic.
        This has to be done overriding the save method of model. We can test it here.
        """
        parent_node = Topic.objects.create(text="Are you hungry?")
        child_1 = Topic.objects.create(text="1", parent=parent_node)
        child_2 = Topic.objects.create(text="2", parent=parent_node)
        child_3 = Topic.objects.create(text="3", parent=parent_node)
        child_4 = Topic.objects.create(text="4", parent=parent_node)
        child_5 = Topic.objects.create(text="5", parent=parent_node)
        child_6 = Topic.objects.create(text="6", parent=parent_node)
        child_7 = Topic.objects.create(text="7", parent=parent_node)
        # We trying to create 7 children for parent_node but only 5 should be saved.
        count = Topic.objects.filter(parent=parent_node).count()
        self.assertEqual(count, 5)

    def test_load_json_file_using_api_view(self):
        """
        Test to ensure json data and file is getting loaded, by calling a url
        """
        client = APIClient()
        response = client.get('/api/v1/load/')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 1)
