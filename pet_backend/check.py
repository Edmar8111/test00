from .models import RequisicaoAdotar
notify=False
list_verify=[]
def verify00(id_user):
    global notify
    pub_id=0
    for verificar_not in RequisicaoAdotar.objects.all():
        if verificar_not.destinatario == id_user:
            pub_id=verificar_not.pub_selec
            if verificar_not.destinatario == id_user and verificar_not.pub_selec==pub_id:
                list_verify.append(verificar_not.destinatario)
    if len(list_verify)>0:
        notify=True
    return print(notify)        