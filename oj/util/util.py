#coding=utf-8

from django.core.paginator import Paginator

Result_dic = {

        4 : 'Accpepted',
        5 : 'Presentation Error',
        6 : 'Wrong Answer',
        7 : 'Time Limit Exceeded',
        8 : 'Memory Limit Exceeded',
        9 : 'Output Limit Exceeded',
        10: 'Runtime Error',
        11: 'Compile Error',
        3 : 'RJ',
        2 : 'CI',
        1 : 'Pending'
        }
language_ab = {
        0: 'C',
        1: 'C++'
        }
#page_number 多少一页
#page 第几页
def paging(tuple_info, page_number, page):
    
    page_num = []
    list_info = {}
    p = Paginator(tuple_info, page_number);
    
    for i in range(0, p.num_pages):
        page_num.append(i + 1)
        list_info['len'] = page_num
        list_info['page'] = page

    if page <= 0 or page > page_number:
        return (None,None)
    else:
        info = p.page(page).object_list
        print info
        return (info,list_info)
     

    
