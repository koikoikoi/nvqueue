import json

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from nvqueue.models import Queue, Printjob


class QueueTest(APITestCase):

    def test_create_queue(self):
        """
        Test queue creation and look up
        """

        TEST_QUEUE_NAME = 'Test queue 1'

        url = reverse('queue-list')
        data = {'name': TEST_QUEUE_NAME}
        response = self.client.post(url, data, format='json')


        # check for success status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # verify that it is in the database
        self.assertEqual(Queue.objects.count(), 1)
        self.assertEqual(Queue.objects.get().name, TEST_QUEUE_NAME)

        # check response
        queue_name = response.data['name']
        self.assertEqual(queue_name, TEST_QUEUE_NAME)

        queue_url = response.data['url']  # URL of queue instance
        response = self.client.get(queue_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], TEST_QUEUE_NAME)

