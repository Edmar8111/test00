from .models import RequisicaoAdotar
notify=False

def verify00(id_user):
    global notify
    pub_id=0
    for verificar_not in RequisicaoAdotar.objects.all():
        if verificar_not.destinatario == id_user:
            pub_id=verificar_not.pub_selec
            if verificar_not.destinatario == id_user and verificar_not.pub_selec==pub_id:
                notify=True
                return notify
        else:
            notify=False
            return notify