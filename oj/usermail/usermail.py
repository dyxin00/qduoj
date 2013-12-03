from django.shortcuts import render_to_response
from oj.models import Mail
from oj.forms import Send_mail
from oj.tools import error, jump_page
from oj.util.util import login_asked
from oj.tools import verify_user

def mail_sc(req, fun, context):
    '''the mails list'''
    username = context['ojlogin'].nick
    if fun == '1':  #received mail
        mails = Mail.objects.filter(mail_to=username)
    elif fun == '2': #new mail
        mails = Mail.objects.filter(mail_to=username).filter(is_new=True)
    elif fun == '3': #sended mail
        mails = Mail.objects.filter(mail_from=username)
    else:
        return error('4o4', 'page ', context, 'error.html')
    
    if len(mails) > 50:
        mails = mails[0:50]
    return render_to_response('mail.html', {
        'mails':mails,
        'context':context,
        'fun':fun}
    )

def sendmail_sc(req, fun, context):
    '''send the mail'''
    error = {}
    if req.method == 'POST':
        form = Send_mail(req.POST)
        if form.is_valid():
            sentfrom = context['ojlogin'].nick
            sendto = form.cleaned_data['send_to']
            (status, run_info) = verify_user('mail_verify', sendto, '')
            if status == 0:
                error = run_info
            else:
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                mail = Mail.objects.create(
                    mail_from=sentfrom,
                    mail_to=sendto, title=title,
                    content=content, is_new=True
                        )
                mail.save()
                return jump_page('/mail', 'send success')
    else:
        form = Send_mail()
    return render_to_response('sendmail.html', {
        'context':context,
        'form':form,
        'error':error}
    )

@login_asked
def readmail_sc(req, context, fun, msgid):
    '''read the mail from others'''
    mail = Mail.objects.filter(mail_id=msgid)
    if len(mail) == 0:
        return error('4o4', 'mail ', context, 'error.html')
    
    username = context['ojlogin'].nick
    mail_from = mail[0].mail_from
    mail_to = mail[0].mail_to
    if mail_from != username and mail_to != username:
        return error('4o4', 'mails', context, 'error.html')
    
    if mail_to == context['ojlogin'].nick:
        mail.update(is_new=False)
    return render_to_response('readmail.html', {
        'context':context,
        'mail':mail[0], 
        'fun':fun}
    )
