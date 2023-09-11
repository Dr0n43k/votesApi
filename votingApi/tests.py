from .models import Voting, PersonVotes
from rest_framework.test import APITestCase
from django.urls import reverse
from .views import voting_list, voting, persons, winners, send_vote
from django.utils import timezone

class VotingListTests(APITestCase):
    url = reverse(voting_list)

    def test_empty_get(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_get(self):
        voting = Voting.objects.create(title="title1", start=timezone.now(),
                              stop=timezone.now()+timezone.timedelta(2),
                              max_votes=100)
        voting.persons.create(fullname="123", photo="", age=21, biography="wewqweqeqeqe")
        voting.persons.create(fullname="1223", photo="", age=23, biography="wewqfqeqe")
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)


class VotingTests(APITestCase):
    url = reverse(voting)

    def test_empty(self):
        response = self.client.get(self.url)
        self.assertEqual(404, response.status_code)

    def test_get(self):
        voting = Voting.objects.create(title="title1", start=timezone.now(),
                                       stop=timezone.now() + timezone.timedelta(2),
                                       max_votes=100)
        voting.persons.create(fullname="123", photo="", age=21, biography="wewqweqeqeqe")
        voting.persons.create(fullname="1223", photo="", age=23, biography="wewqfqeqe")
        id = Voting.objects.all()[0].id
        response = self.client.get(self.url+f"?voting_id={id}")
        self.assertEqual(200, response.status_code)


class PersonTests(APITestCase):
    url = reverse(persons)

    def test_empty(self):
        response = self.client.get(self.url)
        self.assertEqual(404, response.status_code)

    def test_get(self):
        voting = Voting.objects.create(title="title1", start=timezone.now(),
                                       stop=timezone.now() + timezone.timedelta(2),
                                       max_votes=100)
        voting.persons.create(fullname="123", photo="media/1.jpg", age=21, biography="wewqweqeqeqe")
        voting.persons.create(fullname="1223", photo="media/1.jpg", age=23, biography="wewqfqeqe")
        id = Voting.objects.all()[0].id
        response = self.client.get(self.url + f"?voting_id={id}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))


class winnners(APITestCase):
    url = reverse(winners)

    def test_empty(self):
        response = self.client.get(self.url)
        self.assertEqual(404, response.status_code)

    def test_get(self):
        voting = Voting.objects.create(title="title1", start=timezone.now(),
                                       stop=timezone.now(),
                                       max_votes=100)
        voting.persons.create(fullname="123", photo="media/1.jpg", age=21, biography="wewqweqeqeqe")
        voting.persons.create(fullname="1223", photo="media/1.jpg", age=23, biography="wewqfqeqe")
        voting = Voting.objects.create(title="title1", start=timezone.now(),
                                       stop=timezone.now() + timezone.timedelta(2),
                                       max_votes=100)
        voting.persons.create(fullname="123", photo="media/1.jpg", age=21, biography="wewqweqeqeqe")
        voting.persons.create(fullname="1223", photo="media/1.jpg", age=23, biography="wewqfqeqe")
        id = Voting.objects.all()[0].id
        response = self.client.get(self.url)
        self.assertEqual(1, len(response.data))

class SendVote(APITestCase):

    url = reverse(send_vote)

    def test_empty(self):
        response = self.client.post(self.url)
        self.assertEqual(400, response.status_code)

    def test_send(self):
        voting = Voting.objects.create(title="title1", start=timezone.now(),
                                       stop=timezone.now(),
                                       max_votes=100)
        voting.persons.create(fullname="123", photo="media/1.jpg", age=21, biography="wewqweqeqeqe")
        voting.persons.create(fullname="1223", photo="media/1.jpg", age=23, biography="wewqfqeqe")
        data = {'voting_id': 1, 'person_id': 2}
        response = self.client.post(self.url, data, format='json')
        votes = PersonVotes.objects.filter(voting_id=1, person_id=2)[0].votes
        self.assertEqual(1, len(response.data))

    def test_max_votes(self):
        voting = Voting.objects.create(title="title1", start=timezone.now(),
                                       stop=timezone.now(),
                                       max_votes=4)
        voting.persons.create(fullname="123", photo="media/1.jpg", age=21, biography="wewqweqeqeqe")
        voting.persons.create(fullname="1223", photo="media/1.jpg", age=23, biography="wewqfqeqe")
        data = {'voting_id': 1, 'person_id': 2}
        for i in range(4):
            response = self.client.post(self.url, data, format='json')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(400, response.status_code)

