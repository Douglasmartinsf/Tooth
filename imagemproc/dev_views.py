from django.contrib.auth import login, get_user_model
from django.shortcuts import redirect, render
from django.conf import settings

User = get_user_model()

def dev_login(request):
    """
    View de login para desenvolvimento local.
    Cria/loga automaticamente com usuário de desenvolvimento.
    """
    if not settings.DEBUG:
        return redirect('account_login')
    
    # Criar ou pegar usuário de desenvolvimento
    dev_user, created = User.objects.get_or_create(
        username='dev_user',
        defaults={
            'email': 'dev@tooth.local',
            'first_name': 'Dev',
            'last_name': 'User'
        }
    )
    
    if created:
        dev_user.set_password('dev123')
        dev_user.save()
    
    # Fazer login automático
    login(request, dev_user, backend='django.contrib.auth.backends.ModelBackend')
    
    return redirect('imagemproc:upload_save')
