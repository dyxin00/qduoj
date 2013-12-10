from admin.admin_backends import permission_asked
from oj.tools import error

@permission_asked('problem_add')
def admin_shift_mode_sc(req, context, objects, fun):
    if len(objects) == 0:
        return error('404', 'no this problem', context, 'admin_error.html')
    if fun == 'visible':
        if objects[0].visible == True:
            objects.update(visible=False)
        else:
            objects.update(visible=True)
    elif fun == 'oi_mode':
        if objects[0].oi_mode == True:
            objects.update(oi_mode=False)
        else:
            objects.update(oi_mode=True)
    elif fun == 'private':
	    if objects[0].private == True:
	        objects.update(private=False)
	    else:
	        objects.update(private=True)
    elif fun == 'open_rank':
	    if objects[0].open_rank == True:
	        objects.update(open_rank=False)
	    else:
	        objects.update(open_rank=True)
