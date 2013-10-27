'''contest '''
import datetime
from django.core.exceptions import ObjectDoesNotExist
#from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from oj.models import Contest, User, Contest_problem, Solution
from oj.qduoj_config.qduoj_config import PAGE_CONTEST_NUM
from oj.util.util import paging

def contest_list_sc(context, page):

    '''return contest list '''
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

def contest_sc(context, cid):
    '''contest detailed information'''
    problem_list = []

    try:
        cid = int(cid)
    except ValueError:
        return render_to_response("error.html",
                    {'pageinfo':'page not found!', 'title':'404 not found!'})

    contest = Contest.objects.filter(contest_id = cid)
    problem = Contest_problem.objects.filter(contest_id = cid)
    contest_solution = Solution.objects.filter(contest_id = cid)
    for cpb in problem:
        p_contest_solution = contest_solution.filter(
            problem_id=cpb.problem_id)
        problem_list.append(
                {
                    "problem_id" : cpb.problem_id,
                    "num":cpb.num,
                    "title" : cpb.title,
                    "submit" : p_contest_solution.count(),
                    "Ac" : p_contest_solution.filter(result = 4).count(),
                    "score":cpb.score
                    }
                )

    return render_to_response("contest.html",
                              {"context":context,
                               "contest":contest[0],
                               "problem_list" : problem_list}
                             )


def contest_rank_sc(context, cid):

    '''contest rank'''
    contest_solution = Solution.objects.filter(contest_id=cid)
    try:
        contest = Contest.objects.get(contest_id=cid)
    except Contest.DoesNotExist:
        pass
    oi_mode = contest.oi_mode

    user_id_list = contest_solution.values_list('user', flat=True).distinct()

    contest_problem = Contest_problem.objects.filter (contest_id=cid)
    contest_problem = contest_problem.order_by('num')

    contest_problem_id = contest_problem.values_list(
                                                    'problem_id',
                                                     flat=True
                                                    ).distinct()

    if oi_mode:
        contest_score = contest_rank_oi(contest_problem_id,
                                     user_id_list,
                                     contest_solution,
                                     cid)
    else:
        contest_score = contest_rank_acm(contest_problem_id,
                                     user_id_list,
                                     contest_solution,
                                     cid)
    return render_to_response("contest_rank.html",
                              {"contest_score":contest_score,
                               "contest":contest,
                               "context":context})

def contest_rank_acm(contest_problem_id, user_id_list, contest_solution, cid):

    '''acm mode'''
    contest_score = []
    try:
        contest_time = Contest.objects.get(contest_id = cid).start_time
    except Contest.DoesNotExist:
        pass

    for user_id in user_id_list:
        try:
            user = User.objects.get(user_id=user_id).nick
        except User.DoesNotExist:
            pass
        user_solution = contest_solution.filter(user_id = user_id)

        solved = user_solution.filter(result = 4).count()

        user_problem = []
        total_time = datetime.timedelta()
        for pb_id in contest_problem_id:

            pb_id_solution = user_solution.filter(problem_id = pb_id)
            count = pb_id_solution.count()
            try:
                problem_name = Contest_problem.objects.filter(
                    contest_id = cid).get(problem_id = pb_id)
            except Contest_problem.DoesNotExits:
                pass

            ac_solution = pb_id_solution.filter(result = 4)
            if len(ac_solution):

                ac_time = ac_solution[0].judgetime
                ac_user_time = ac_time - contest_time
                penalty = count - len(ac_solution)
                time_penalty = datetime.timedelta(minutes=20*penalty)
                user_problem.append(
                    {
                        'problem_name' : problem_name.title,
                        'submit': 1,
                        'ac_user_time':ac_user_time,
                        'penalty': penalty,
                        'pid' :pb_id
                    })

                total_time = total_time + ac_user_time + time_penalty

            else:
                user_problem.append(
                    {
                        'problem_name':problem_name.title,
                        'submit': 0,
                        'ac_user_time':ac_user_time,
                        'penalty':penalty,
                        'pid' :pb_id
                    }
                    )
        contest_score.append(
                {
                    'rank': 0,
                    'user' : user,
                    'user_id' : user_id,
                    'solved' : solved,
                    'penalty':total_time,
                    'problem' :user_problem,
                    }
                )

    contest_score = sorted(contest_score, key=lambda user:
                           (-user['solved'], user['penalty']))
    return contest_score

def contest_rank_oi(contest_problem_id, user_id_list, contest_solution, cid):

    '''oi mode'''
    contest_score = []
    for user_id in user_id_list:
        try:
            user = User.objects.get(user_id=user_id).nick
        except User.DoesNotExist:
            pass
        user_solution = contest_solution.filter(user_id = user_id)

        solved = user_solution.filter(result = 4).count()
        user_problem = []
        total_score = 0.0
        for pb_id in contest_problem_id:

            pb_id_solution = user_solution.filter(
                problem_id = pb_id).order_by('-solution_id')
            try:
                pb_score = Contest_problem.objects.get(
                    problem_id = pb_id).score
                problem_name = Contest_problem.objects.filter(
                    contest_id = cid).get(problem_id = pb_id)
            except ObjectDoesNotExist:
                pass

            if len(pb_id_solution):
                score = pb_score * pb_id_solution[0].score / 100
                user_problem.append(
                    {
                        'problem_name' : problem_name.title,
                        'problem_score': score,
                        'submit' : 1,
                        'pid' :pb_id
                    }
                    )
                total_score = total_score + score
            else:
                user_problem.append(
                    {
                        'problem_name' : problem_name.title,
                        'problem_score': 0.0,
                        'submit' : 0,
                        'pid' :pb_id
                    }
                    )

        contest_score.append(
                {
                    'rank': 0,
                    'user' : user,
                    'user_id' : user_id,
                    'solved' : solved,
                    'score':total_score,
                    'problem' :user_problem
                    }
                )

    contest_score = sorted(contest_score, key=lambda user: -user['score'])

    return contest_score

