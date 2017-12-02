from __future__ import unicode_literals
from ..login.models import User
from .models import Poke
from django.db.models import Count
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
# Create your views here.
def index(request):
    if 'user_id' in request.session:
        uId = request.session['user_id']
        currentUser = User.objects.get(id=uId)
        # pokerUser = User.objects.get(id=)
        #get poke count

        poked_by = currentUser.pokes_made.all().values("poker_id").annotate(Count('id')).order_by('-id__count')
        poker_list = currentUser.pokes_received.all().values('poker_id').annotate(Count('id')).order_by('-id__count')
        poker_count = len(poker_list)
        # poke_count = User.objects.filter(pokes=pokes_made).count()
        users = User.objects.exclude(id=uId)
        names = User.objects.values_list('name','id')
        poker_id_list = currentUser.pokes_received.values_list('poker_id', flat=True).annotate(Count('id')).order_by('-id__count').distinct()
        # pokes = poker_list.objects.get(id=id)
        # test = User.objects.raw("SELECT * FROM {{user}}_{{poke}}")
        pokes_test = User.objects.filter(pokes_received=uId).values_list('id', flat=True)
        # all_users = User.objects.all().select_related("poker_id")[0:10]
        # poker_ids = [a.poker_id for a in all_users]
        # for user in User.objects.raw('SELECT *, COUNT(DISTINCT user_id) as num_users_poked_by FROM user JOIN pokes ON user.id = pokes.poked_id WHERE user.id=:id'):
        #     print(user)
        # for user in User.objects.raw('SELECT *, COUNT(DISTINCT user_id) as num_users_poked_by FROM login_user JOIN poke_poke ON user.id = pokes.poker_id WHERE user.id=3'):
        #     print(user)
        # for user in User.objects.raw('SELECT id as userid, poker.id FROM login_user JOIN poke_poke'):
        #     print  'raw sql: ', user

        # SELECT user_id, poker.name, count(*) AS times_poked FROM pokes
        #         JOIN users ON poked_id = users.id
        #         JOIN users AS poker ON user_id = poker.id
        #         WHERE users.id = :id
        #         GROUP BY user_id ORDER BY times_poked DESC
        poker_names = []
        for i, x in enumerate(names):
            for j, x in enumerate(poker_list):
                if(poker_list[j]['poker_id'] == names[i][1]):
                    poker_list[j]['name'] = names[i][0]

        print 'poker_names', poker_names
        print 'poker_id_list', poker_id_list
        # print 'poker list INDEX', poker_list[0]['poker_id']

        # for poker in poker_list:
        #     for i, x in enumerate(poker_names):
        #         if poker.id
        #         poker.update({'name':name})



        context = {
            'currentUser': currentUser,
            'poked_by': poked_by,
            'poker_count': poker_count,
            'users': users,
            'session': request.session,
            # 'pokers': pokers,
            'poker_list': poker_list
        }

        print 'poker list: {}'.format(poker_list)
        # print 'pokers: {}'.format(pokers)
        print 'poked_by: {}'.format(poked_by)
        return render(request, "poke/index.html", context)
    return redirect(reverse('poke:index'))

def poke(request, id):
    if 'user_id' in request.session:
        uId = request.session['user_id']
        Poke.objects.Poke(id, uId)
        print "hit poke"
        print "pokee: {}".format(id)
        print "poker: {}".format(uId)
        return redirect(reverse('poke:index'))
    return redirect(reverse('login:index'))
