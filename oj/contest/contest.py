import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.models import *
from oj.forms import *
from oj.qduoj_config.qduoj_config import *
from oj.util.util import *

def contest_list_sc(req, context, page):

    try:
        page = int(page)
    except ValueError:
        return render_to_response("error.html",
                    {'pageinfo':'page not found!', 'title':'404 not found!'})

    (contest, list_info) = paging(
        Contest.objects.order_by("-contest_id"), PAGE_CONTEST_NUM, page
        )
    if contest == None:
        return render_to_response("error.html",
                    {'pageinfo':'page not found!', 'title':'404 not found!'})


    return render_to_response("contest_list.html",
                    { "context" : context,
                     "contest":contest,
                     "list_info": list_info
                    })

def contest_sc(req, context, cid):
    problem_list = []

    try:
        cid = int(cid)
    except ValueError:
        return render_to_response("error.html",
                    {'pageinfo':'page not found!', 'title':'404 not found!'})

    contest = Contest.objects.filter(contest_id = cid)
    problem = Contest_problem.objects.filter(contest_id = cid)
    contest_solution = Solution.objects.filter(contest_id = cid)
    for cp in problem:
        p_contest_solution = contest_solution.filter(problem_id = cp.problem_id)
        problem_list.append(
                {
                    "problem_id" : cp.problem_id,
                    "num":cp.num,
                    "title" : cp.title,
                    "submit" : p_contest_solution.count(),
                    "Ac" : p_contest_solution.filter(result = 4).count()
                    }
                )

    return render_to_response("contest.html",
                              {"context":context,
                               "contest":contest[0],
                               "problem_list" : problem_list}
                             )


def contest_rank_sc(req, context, cid):

    contest_solution = Solution.objects.filter(contest_id=cid)

    user_id_list = contest_solution.values_list('user', flat=True).distinct()

    contest_problem = Contest_problem.objects.filter (contest_id=cid)
    contest_problem = contest_problem.order_by('num')

    contest_problem_id = contest_problem.values_list(
                                                    'problem_id',
                                                     flat=True
                                                    ).distinct()

    print contest_problem_id

    contest_score = contest_rank_acm(contest_problem_id,
                                     user_id_list,
                                     contest_solution,
                                     cid)
    return render_to_response("contest_rank.html", {"contest_scor":contest_score})

def contest_rank_acm(contest_problem_id, user_id_list, contest_solution,cid):

    contest_score = []
    contest_time = Contest.objects.get(contest_id = cid).start_time

    for user_id in user_id_list:

        user = User.objects.get(user_id=user_id).nick
        user_solution = contest_solution.filter(user_id = user_id)

        solved = user_solution.filter(result = 4).count()
        #user_problem[]
        for pb_id in contest_problem_id:

            pb_id_solution = user_solution.filter(problem_id = pb_id)
            count = pb_id_solution.count()
            count_ac = pb_id_solution.count()

            ac_solution = pb_id_solution.filter(result = 4)
            if len(ac_solution):

                ac_time = ac_solution[0].judgetime
                ac_user_time = ac_time - contest_time
                time_penalty = datetime.timedelta(minutes=21*count-count_ac)

                print time_penalty 
                print ac_user_time
                print time_penalty + ac_user_time
                print ac_time, contest_time, pb_id, ac_solution[0].solution_id 

            if count != 0:
                print count,pb_id

        print user
        print user_solution
        print
        contest_score.append(
                {
                    'rank': 0,
                    'user_id' : user,
                    'solved' : solved,
                    'penalty':0,
                    'problem' :0,
                    }
                )




