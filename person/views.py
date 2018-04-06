from django.views import generic
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Person
from .serializers import PersonSerializer
import os


def load_data(request):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'static/person/data.txt')
    with open(file_path) as f:
        lines = [x.strip().split(';') for x in f.readlines()]
        f.close()

    persons = {}
    p_objects = []

    for line in lines:
        id = int(line[0])
        persons[id] = { 'firstname' : line[1],
                        'lastname'  : line[2],
                        'age'       : int(line[3] if line[3] else 0),
                        'sex'       : line[4],
                        'friends'   : [int(x) for x in line[5].split(',')]}

        p = Person(id, line[1], line[2], int(line[3] if line[3] else 0), line[4])
        p_objects.append(p)
        p.save()

    for p in p_objects:
        [p.friends.add(x) for x in p_objects if x.id in persons[p.id]['friends']]
        p.save()

    return redirect('person:index')


class PersonList(APIView):

    def get(self, request):
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IndexView(generic.ListView):
    template_name = 'person/index.html'
    context_object_name = 'persons'

    def get_queryset(self):
        return Person.objects.all()


class DetailView(generic.DetailView):
    model = Person
    template_name = 'person/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        selected_person = self.get_object()

        friend_ids = selected_person.friends.values_list('id', flat=True)

        pf = Person.objects.prefetch_related('friends')
        fofs = [list(x.friends.all()) for x in pf if x.id in friend_ids] # friends of friends
        fofs_flat = [item for sublist in fofs for item in sublist if item.id != selected_person.id and item.id not in friend_ids]
        fofs_flat = list(set(fofs_flat))

        context['fofs'] = fofs_flat

        sf = []
        for friend in fofs_flat:
            counter = 0
            for fof in fofs:
                if friend in fof:
                    counter += 1
                    if counter == 2:
                        sf.append(friend)
                        break

        context['sf'] = sf

        return context
