from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Voting, PersonVotes
import rest_framework.status as status
from rest_framework.parsers import JSONParser
from django.utils import timezone


def check_active():
    voting = Voting.objects.all()
    for i in voting:
        i.save()
        if i.start < timezone.now() <= i.stop:
            person_votes = PersonVotes.objects.filter(voting=i).order_by('votes').last().votes
            if person_votes < i.max_votes or i.max_votes == 0:
                Voting.objects.filter(id=i.id).update(active=True)
            else:
                Voting.objects.filter(id=i.id).update(active=False)
        else:
            Voting.objects.filter(id=i.id).update(active=False)


@csrf_exempt
@api_view(["GET"])
def voting_list(request):
    check_active()
    voting_list = Voting.objects.all().order_by('active').values('id', 'title', 'active')
    return Response(voting_list)


@csrf_exempt
@api_view(["GET"])
def voting(request):
    check_active()
    voting_id = request.GET.get('voting_id')
    voting = Voting.objects.filter(id=voting_id)
    if not voting.exists():
        return Response({'message': 'voting not found'}, status=status.HTTP_404_NOT_FOUND)
    results = {"voting": voting[0].title, "active": voting[0].active, "persons": []}
    person = PersonVotes.objects.filter(voting=voting[0])
    for i in person:
        results['persons'] += [{'person': i.person.fullname, 'votes': i.votes}]
    return Response(results)


@csrf_exempt
@api_view(["GET"])
def persons(request):
    voting_id = request.GET.get('voting_id')
    voting = Voting.objects.filter(id=voting_id)
    if not voting.exists():
        return Response({'message': 'voting not found'}, status=status.HTTP_404_NOT_FOUND)
    persons = voting[0].persons.all()
    return Response([{'id': i.id, 'fullname': i.fullname, 'photo': i.photo.url,
                      'age': i.age, 'biography': i.biography} for i in persons])


@csrf_exempt
@api_view(["GET"])
def winners(request):
    check_active()
    voting = Voting.objects.filter(active=False)
    if not voting.exists():
        return Response({'message': 'voting not found'}, status=status.HTTP_404_NOT_FOUND)
    winners = []
    for i in voting:
        person = PersonVotes.objects.filter(voting=i)
        max_votes = person.aggregate(Max('votes'))['votes__max']
        person = person.filter(votes=max_votes)
        winners += [{'voting': i.title, 'winner': [_.person.fullname for _ in person], 'votes': person[0].votes}]
    return Response(winners)


@csrf_exempt
@api_view(["POST"])
def send_vote(request):
    check_active()
    data = JSONParser().parse(request)
    voting_id = data['voting_id']
    person_id = data['person_id']
    voting = Voting.objects.filter(id=voting_id)
    if not voting.exists():
        return Response({'message': 'voting not found'}, status=status.HTTP_404_NOT_FOUND)
    if not voting[0].active:
        if timezone.now() < voting[0].start:
            return Response({'message': 'voting has not started'}, status=status.HTTP_400_BAD_REQUEST)
        elif timezone.now() > voting[0].stop:
            return Response({'message': 'voting is completed'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'maximum number of votes'}, status=status.HTTP_400_BAD_REQUEST)
    person = voting[0].persons.filter(id=person_id)
    if not person.exists():
        return Response({'message': 'person not found'}, status=status.HTTP_404_NOT_FOUND)
    person_votes = PersonVotes.objects.filter(person=person[0], voting=voting[0])[0]
    person_votes.votes += 1
    person_votes.save()
    # if voting[0].max_votes == person_votes.votes:
    #     voting.update(active=False)
    return Response({'person': person[0].fullname, 'votes': person_votes.votes})

