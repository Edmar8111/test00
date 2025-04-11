from django.shortcuts import render, redirect, get_object_or_404
import shortuuid
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse,HttpRequest
from .models import user_info, user_complemento, PubInfo, Fav_user, RequisicaoAdotar
from time import sleep
import os 

userObject=0 
valorObjectLogin=0 
valor1=0 
verify0=0
verify01=0
pubId=0
verify_list=[]
pubInfo=[]
filterObject={}
requestInfo=[{'MailReq':[a.email for a in user_info.objects.all()]}]

def pubInfoObject(requestObject=None):
    #executa a listagem das info e images das pub referente
    global pubInfo, filterObject
    
    verifyStep=0
    DbPubInfo=[objectdb for objectdb in PubInfo.objects.all()] 
    pubInfo=[]
    Objectget=[PubInfo.objects.get(id=pubObject.id) for pubObject in PubInfo.objects.all()]
    filterObject={}
    for filterObjectsDb in Objectget:
        if filterObjectsDb.idade != 0 or filterObjectsDb.tipo_n != 'Desconhecido':
            pubInfo.append(filterObjectsDb)
    sleep(0.5)
    while verifyStep<len(pubInfo):
        filterObject[int(pubInfo[verifyStep].id)]=[]
        for a in range(0, len(DbPubInfo)):
            if pubInfo[verifyStep].id==DbPubInfo[a].creator:
                filterObject[pubInfo[verifyStep].id].append(DbPubInfo[a].imgpub)    
        if a==len(DbPubInfo)-1:
            verifyStep+=1
    try:
        if requestObject is not None:
            print(PubInfo.objects.get(id=requestObject))
            return PubInfo.objects.get(id=requestObject)

    except: 
        return 


def deletar_pub(PubId):
        #executa o delete do post
        
        list_del=[]
        imgPubDelete=[]
        objectPub=[{'pubId':[a.id for a in PubInfo.objects.all()], 'idCreator':[a.creator for a in PubInfo.objects.all()], 'ImgPub':[a.imgpub for a in PubInfo.objects.all()]}]
        for addPostDelete in range(0,len(objectPub[0]['pubId'])):
            if PubId==objectPub[0]['pubId'][addPostDelete]:
                list_del.append(objectPub[0]['pubId'][addPostDelete])
                for deletePubIndex in PubInfo.objects.all():
                    if objectPub[0]['pubId'][addPostDelete]==deletePubIndex.creator:
                       list_del.append(deletePubIndex.id)
                imgPubDelete.append(objectPub[0]['ImgPub'][addPostDelete])
            if objectPub[0]['idCreator'][addPostDelete]==PubId:
                imgPubDelete.append(objectPub[0]['ImgPub'][addPostDelete])
        sleep(0.5)
        try:
            for deletePub in list_del[::-1]:
                PubInfo.objects.get(id=int(deletePub)).delete()
            sleep(0.5)
            for ImgDeleteServer in imgPubDelete:
                if os.path.exists(f'media/{str(ImgDeleteServer)}'):
                    print('request image delete')
                    os.remove((f'media/{str(ImgDeleteServer)}'))
        except:pass
        return redirect(home)


def cadastro_user(metodo_acesso_user, nome_user, email_user, pass_word, telefone_user, cidade_user):
    #efetua o cadastro do usuario no db
    try: 
        cadastro_info_save=user_info(
            tipo=metodo_acesso_user,
            nome=nome_user,
            email=email_user,
            senha=pass_word,
            telefone=telefone_user,
            cidade=cidade_user,
            enctype_hash=shortuuid.ShortUUID().random(length=7)
        )
        cadastro_info_save.save()
        return print('Dados Salvos')
    except:
       return HttpResponse('ERROR INIT')


def verify(checkUp):
    global verify0
    verify0=+checkUp
    return verify0


def home(request: HttpRequest):
    global verify0, verify01, verify_list, pubInfo
    

    context=None
    try:
        pubInfoObject()
    except:pass
    #efetua verificação se o usuario possui notificação ativa
    verify_list=[]
    def verify_notify(id_user):
        for verificar_notifica in RequisicaoAdotar.objects.all():
            if verificar_notifica.destinatario==id_user and verificar_notifica.log_on==False:
                verify_list.append(verificar_notifica.pub_selec)
            
        return verify_list

    # for delet in RequisicaoAdotar.objects.all():
    #     RequisicaoAdotar.objects.get(pk=delet.id).delete()    

    if verify0==1 and verify01==1:
        context={
        'logo': 'image/petconnect.svg',
        'login_display':'none',
        'logout_display':True,
        'key_user':userObject.enctype_hash,
        'user_name':userObject.nome,
        'pub_index':pubInfo,
        'notification':False,
        }

        
        verify_notify(userObject.id)
        if len(verify_list)>0:
            context['notification']=True
           
        
        return render(request, 'html/home.html', context)
    if verify0==1 and verify01==0:
        verify_notify(userObject.id)
        if len(verify_list)>0:
            context['notification']=True

        context={
        'logo': 'image/petconnect.svg',
        'login_display':'none',
        'logout_display':True,
        'key_user':'None',
        'user_name':userObject.nome,
        'pub_index':pubInfo,
        'notification':False,
        'pub_id':0,
        }
        
        return render(request, 'html/home.html', context)
    
    if request.method=='GET' and verify0==0:
        context={
        'logo': 'image/petconnect.svg',
        'login_display':'flex',
        'logout_display':False,
        'key_user':'None',
        'pub_index':pubInfo,
        'notification':False,
        'pub_id':0,
        }
        
        return render(request, 'html/home.html', context)


def perfil_user(request, key_inst):
    global userObject, verify0, verify01
    #criar a indexação de pub e favoritos user
    def verify_notify(id_user):
        for verificar_notifica in RequisicaoAdotar.objects.all():
            if verificar_notifica.destinatario==id_user and verificar_notifica.log_on==False:
                verify_list.append(verificar_notifica.pub_selec)
        return
    try:
        context={
            'key_user':userObject.enctype_hash,
            'login_display':'none',
            'user_name':userObject.nome,
            'user_id':userObject.id,
            'logout_display':True,
            'notification':False,
        }
        context['ong_true']=True if int(userObject.tipo)==1 else False
        verify_notify(userObject.id)
        if len(verify_list)>0:
            context['notification']=True

        if request.method=='GET':
            context['key_user']=userObject.enctype_hash
            if request.GET.get('click_logout')!=None or verify0==0:
                verify0=0
                return redirect(home)
            if request.GET.get('click_edit')!=None:
                return redirect(complemento_info)
            return render(request, 'html/menuUser.html', context)
    except:
        print('Test')
        return redirect(login)


def complemento_info(request):
    global valor1, userObject, verify0, verify01

    def verify_notify(id_user):
        for verificar_notifica in RequisicaoAdotar.objects.all():
            if verificar_notifica.destinatario==id_user and verificar_notifica.log_on==False:
                verify_list.append(verificar_notifica.pub_selec)
        return
    if request.method=='GET':
        verify0=1
        
        from .models import user_complemento as uc    
        context = {
            'logo':'image/petconnct.svg',
            'login_display':'none',
            'logout_display':True,
            'nome':userObject.nome,
            'email':userObject.email,
            'cidade':userObject.cidade,
            'key_user':userObject.enctype_hash,
            'user_name':userObject.nome
        }

        verify_notify(userObject.id)    
        if len(verify_list)>0:
            context['notification']=True

        for loop_inf in uc.objects.all():
            if loop_inf.cep and loop_inf.id_id==userObject.id:
                valor1=loop_inf.id
                context['cep']=loop_inf.cep
            if loop_inf.cpf and loop_inf.id_id==userObject.id:
                context['cpf']=loop_inf.cpf
            if loop_inf.estado and loop_inf.id_id==userObject.id:
                context['estado']=loop_inf.estado
            if loop_inf.endereco and loop_inf.id_id==userObject.id:
                context['endereco']=loop_inf.endereco
            if loop_inf.rua and loop_inf.id_id==userObject.id:
                context['rua']=loop_inf.rua
            if loop_inf.numero and loop_inf.id_id==userObject.id:
                context['numero']=loop_inf.numero
            if loop_inf.complemento and loop_inf.id_id==userObject.id:
                context['complemento']=loop_inf.complemento
            if loop_inf.date and loop_inf.id_id==userObject.id:
                context['date']=loop_inf.date
        
        
        return render(request, 'html/complemento_info.html', context)

    # if verify0==1:
    #     print('Criar menu user')
    #     context['nome']=userObject.nome
    #     context['email']=userObject.email
    #     context['cidade']=userObject.cidade
    #     context['key_user']=userObject.enctype_hash    
    
    if request.method == 'POST':
        if valor1==0:
            for search_user in user_complemento.objects.all():
                if search_user.id_id == userObject.id:
                    valor1=search_user.id
        #fetuar verificação de dados existentes
        id_saver = user_complemento.objects.get(id=valor1)
        id_saver0 = user_info.objects.get(id=userObject.id)
        id_saver0.nome=request.POST.get('nome')
        id_saver0.email=request.POST.get('email')
        id_saver0.cidade=request.POST.get('cidade')
        id_saver.cpf=request.POST.get('cpf')
        id_saver.date=request.POST.get('date')
        id_saver.cep=request.POST.get('cep')
        id_saver.estado=request.POST.get('estado')
        id_saver.endereco=request.POST.get('endereco')
        id_saver.rua=request.POST.get('rua')
        id_saver.numero=int(request.POST.get('numero'))
        id_saver.complemento=request.POST.get('complemento')
        
        id_saver0.save()
        id_saver.save()
        verify0=1
        return redirect(login)


def login_user_verify(request):
    global verify0,userObject, verify01, valorObjectLogin
    #verificação pela etapa de login
    if valorObjectLogin==0:
        return redirect(home)
    #redireciona para verificação de user
    if user_complemento.objects.all() and userObject!=0:
        for user_comp_verify in user_complemento.objects.all():
            if user_comp_verify.id_id == userObject.id:
                verify(1)   
                data_complement = user_comp_verify
                break
        if verify0==1 and verify01 == 0 and data_complement.cep and data_complement.cpf and data_complement.estado and data_complement.endereco :
            messages.success(request, f'Usuario {userObject.nome} Logado!')
            return redirect(home)
        if verify01==1 and verify0==0:
            verify0=1
            verify01=0
            return redirect(complemento_info)
        else:
            #criar msg no front que retorne a requisição de complementação do usuario
            return redirect(complemento_info)


def login(request):
    global valorObjectLogin, userObject,verify01,verify0
    
    context={
        'logo':'image/petconnect.svg',
        'msg_display':'none',
        'logout_display':False, 
    } 
    # for delete in user_info.objects.all():
    #       user_info.objects.get(pk=delete.id).delete()

    if request.method == 'POST':
        valorObjectLogin=1
        print('request') if request.POST.get('email') in requestInfo[0]['MailReq'] else False
        for verificar in user_info.objects.all():
            if request.POST.get('email') == verificar.email and request.POST.get('password') == verificar.senha:
                userObject = user_info.objects.get(pk=verificar.id)
                return redirect(login_user_verify)
            
        context['msg_display']='block'
        return render(request, 'html/login.html', context)
                
    if request.method == 'GET':
        if verify0==1:
            try:
                userObject=user_info.objects.get(id=userObject.id)
                verify01=1
                verify0=0
                return redirect(complemento_info)
            except:
                return redirect(login)
        return render(request, 'html/login.html', context)


def cadastro(request): 
    global verify0
    
    context={'logo': 'image/petconnct.svg',
             'error_msg':False}
    for user_inf in user_info.objects.all():
        verify(1) if user_inf.email == request.POST.get('email') else verify(0)
        if verify0>0:
           context['error_msg']='ERRO! Email já cadastrado'                      
           break
    #verificação de conta existente
    if request.method=='GET':
        return render(request, 'html/cadastro.html', context)
    
    if request.method == 'POST' and verify0==0:
        #efetua o chamado da function que recebe os valores inputados no front
        cadastro_user(request.POST.get('type'), request.POST.get('name'),request.POST.get('email'),request.POST.get('password'),request.POST.get('phone'),request.POST.get('city'))
        
        sleep(0.5)
        complemento_save_file=user_complemento(id_id=user_info.objects.latest('id').id,numero=request.POST.get('phone'),endereco=request.POST.get('city'))
        complemento_save_file.save()
        return redirect(login)
    else:
        #criar o retorno via front msg para user
        verify0=0
        return render(request, 'html/cadastro.html', context)


def pubCreate(request, inst_hash):
    global userObject, verify0, verify01
    img_save={}
    context={'logout_display':True,'login_display':'none' ,'key_user':userObject.enctype_hash,'user_name':userObject.nome}
    
    
    if request.method=='GET' and verify0==1:

            return render(request, 'html/cadastrol_pet.html', context)
    if request.method=='POST' and verify0==1:
        print(request.POST.get('status'))
        list_t={}
        for pub_test in PubInfo.objects.all():
            list_t['url:']=pub_test.imgpub
            if int(pub_test.creator)==int(userObject.id):
                list_t['id:']=pub_test.id
     
        saveInfo=PubInfo(
            titulo=request.POST.get('titulo'),
            imgpub=request.FILES['file0'],
            idade=request.POST.get('idade'),
            sexo='FEMEA' if request.POST.get('sexo')=='1' else 'MACHO',
            castramento='Sim' if request.POST.get('castrado')=='1' else 'Não',
            raca=request.POST.get('raca'),
            desc=request.POST.get('descricao') if request.POST.get('descricao')!='' else 'NONE',
            tipo_n= request.POST.get('tipo_n'),
            on_true=int(request.POST.get('status')),
            creator=userObject.id,
            )
        saveInfo.save()
        try: img_save['file1']=request.FILES['file1'] 
        except: img_save['file1']=False
        try: img_save['file2']=request.FILES['file2']
        except: img_save['file2']=False            
        try: img_save['file3']=request.FILES['file3'] 
        except: img_save['file3']=False
        try:img_save['file4']=request.FILES['file4']
        except:img_save['file4']=False
        list_t['id:']=PubInfo.objects.last().id
        if img_save['file1']!=False:
            save_test=PubInfo(
                titulo=f'{PubInfo.objects.get(pk=int(list_t['id:'])).titulo}-file1',
                imgpub=img_save['file1'],
                creator=PubInfo.objects.get(pk=int(list_t['id:'])).id
            )
            save_test.save()
        if img_save['file2']!=False:
            save_test=PubInfo(
                titulo=f'{PubInfo.objects.get(pk=int(list_t['id:'])).titulo}-file2',
                imgpub=img_save['file2'],
                creator=PubInfo.objects.get(pk=int(list_t['id:'])).id
            )
            save_test.save()
        if img_save['file3']!=False:
            save_test=PubInfo(
                titulo=f'{PubInfo.objects.get(pk=int(list_t['id:'])).titulo}-file3',
                imgpub=img_save['file3'],
                creator=PubInfo.objects.get(pk=int(list_t['id:'])).id
            )
            save_test.save()
        if img_save['file4']!=False:
            save_test=PubInfo(
                titulo=f'{PubInfo.objects.get(pk=int(list_t['id:'])).titulo}-file4',
                imgpub=img_save['file4'],
                creator=PubInfo.objects.get(pk=int(list_t['id:'])).id
            )
            save_test.save()
        
        
        # for indice in range(len(img_save)):
        #     SaveImgInfo=PubInfo(
        #         titulo=PubInfo.objects.last().titulo,
        #         creator=PubInfo.objects.last().creator,
        #         imgpub=img_save[f'a{indice}'],
        #         )
        
        return redirect(f'http://127.0.0.1:8000/petconnect/menu={userObject.enctype_hash}')
    else:
        return redirect(home)


def pubIndex(request, inst_hash):
    global verify0, userObject, pubInfo
    try:
        print(userObject.nome)
        context={'PubObject':[PubInfo.objects.get(id=a.id) for a in pubInfo],
                 'user_name':userObject.nome,'login_display':'none',
                 'logo':'image/petconnect.svg','key_user':userObject.enctype_hash,
                 'logout_display':True,
                 }
        return render(request,'html/pubs_page.html', context)
    except:
        return HttpResponse('Error INIT')


def post_detail(request, id, name):
    global userObject, pubInfo, verify0,pubId
    if pubId!=0:
        if id!=pubId:
            id=pubId
    pubId=id
    print(pubId)
    context={'pub_file':[], 'img0':{}, 'fav_on':False, 'pub_id':0, 'pubInfoObject':pubInfoObject(id), 'user_name':None, 'key_user':None, 'user_id':None}
        
    def requestHash():
        try:
            context['user_name']=userObject.nome
            context['login_display']='none'
            context['logout_display']=True
            context['key_user']=userObject.enctype_hash
            context['user_id']=userObject.id
            context['verify']=verify0
        except:
            pass
    
    def verify_image():
        try:
            context['img0']=PubInfo.objects.get(pk=id).imgpub
            for imgPub in PubInfo.objects.all():
                if PubInfo.objects.get(pk=id).id == imgPub.creator:
                    context['pub_file'].append(imgPub.imgpub)    
        except:
            return
    
    def fav_v():
            for verify_fav in Fav_user.objects.all():
                if verify_fav.user_id==userObject.id and verify_fav.id_pub==context['pubInfoObject'].id:
                    context['fav_on']=True

    if verify0==0 and request.method=='GET':
        sleep(0.5)
        verify_image()
        return render(request, 'html/page_pet.html', context)
    
    if request.method=='GET' and verify0==1:
        requestHash()
        verify_image() 
        fav_v()
        return render(request, 'html/page_pet.html', context)
    
    if request.method=='POST' and int(request.POST.get('click_fav'))==1:
        print(id)
        requestHash()
        verify_image()
        
        save_fav=Fav_user(
            id_pub=id,
            user_id=context['user_id'],
        )
        save_fav.save()
        if len(context['pub_file'])==0:            
            try:
                get_pub(id_pub=context['pub_id'])
            except:
                print('error pub')
                pass
        fav_v()
        return render(request, 'html/page_pet.html', context)
    if request.method=='POST' and int(request.POST.get('click_fav'))==2:
        print('requestRemove')
        requestHash()
        verify_image()
        for exec_del in Fav_user.objects.all():
            if exec_del.id_pub == context['pubInfoObject'].id and exec_del.user_id == context['user_id']:
                Fav_user.objects.get(pk=exec_del.id).delete()
                break
        print('Retirado dos favoritos')
        fav_v()
        return render(request, 'html/page_pet.html', context)
    
    if request.method=='POST' and int(request.POST.get('click_fav'))==0:
        requestHash()
        #modo de exclusão cascata
        if int(request.POST.get('bt_delete'))==1:
            for exec_delete in PubInfo.objects.all(): 
                if int(exec_delete.creator)==id:
                        delet_pub=PubInfo.objects.get(pk=int(exec_delete.id))
                        if os.path.exists(f'media/{exec_delete.imgpub}'):
                            os.remove(f'media/{exec_delete.imgpub}')
                        delet_pub.delete()
                if exec_delete.creator==userObject.id and exec_delete.id == id:
                    delet_pub = PubInfo.objects.get(pk=int(exec_delete.id))
                    if os.path.exists(f'media/{exec_delete.imgpub}'):
                            os.remove(f'media/{exec_delete.imgpub}')
                    delet_pub.delete()
            return redirect(home)
        #executar return de forma direta
    
        return render(request, 'html/pubPage.html', context)


def edit_post(request:HttpRequest, hash, id):
    global verify0, userObject
    editMSG=False
    ObjectInfoEdit=PubInfo.objects.get(id=id)
    #requisita a URL COMPLETA: request.get_full_path()
    
    pubObjectInfo={'titulo':str(PubInfo.objects.get(pk=id).titulo), 'castrado':str(PubInfo.objects.get(pk=id).castramento),
                   'raca':str(PubInfo.objects.get(pk=id).raca), 'sexo':str(PubInfo.objects.get(pk=id).sexo),'typePet':str(PubInfo.objects.get(pk=id).tipo_n),
                   'idade':int(PubInfo.objects.get(pk=id).idade),'descricao':str(PubInfo.objects.get(pk=id).desc), 'ImageFirst':PubInfo.objects.get(pk=id).imgpub,
                   'status':int(ObjectInfoEdit.on_true),
                   'imagesPub':list(),'ImagesID':list(),'id':id,
                   
                   #userObjects
                   'key_user':userObject.enctype_hash,'logout_display':True,'login_display':'none','user_name':userObject.nome
                   }
    for imageAdd in PubInfo.objects.all():
        if imageAdd.creator==id:
            pubObjectInfo['ImagesID'].append(imageAdd.id)
            pubObjectInfo['imagesPub'].append(imageAdd.imgpub)

    if request.method=='POST':
        AlocateInfo=None
        if request.POST.get('statusNew')!=None:
            editMSG=True
            AlocateInfo=request.POST.get('statusNew')
            ObjectInfoEdit.on_true=int(AlocateInfo)
            ObjectInfoEdit.save()
        if request.POST.get('tituloNew')!=None:
            editMSG=True
            AlocateInfo=request.POST.get('tituloNew')
            ObjectInfoEdit.titulo=str(AlocateInfo)
            ObjectInfoEdit.save()
        
        if request.POST.get('idadeNew')!=None:
            editMSG=True
            AlocateInfo=request.POST.get('idadeNew')
            ObjectInfoEdit.idade=int(AlocateInfo)
            ObjectInfoEdit.save()

        if request.POST.get('descricaoNew')!=None:
            editMSG=True
            AlocateInfo=request.POST.get('descricaoNew')
            ObjectInfoEdit.desc=str(AlocateInfo)
            ObjectInfoEdit.save()

        if request.POST.get('sexoNew')!=None:
            editMSG=True
            AlocateInfo=request.POST.get('sexoNew')
            ObjectInfoEdit.sexo=str(AlocateInfo)
            ObjectInfoEdit.save()

        if request.POST.get('typeNew')!=None:
            editMSG=True
            AlocateInfo=request.POST.get('typeNew')
            ObjectInfoEdit.tipo_n=str(AlocateInfo)
            ObjectInfoEdit.save()

        if request.POST.get('castramentoNew')!=None:
            editMSG=True
            AlocateInfo=request.POST.get('castramentoNew')
            ObjectInfoEdit.castramento=AlocateInfo
            ObjectInfoEdit.save()

        #execute verify file and change
        try:
            if request.FILES[f'{id}']:
                imageChange=PubInfo.objects.get(pk=id)
                imageChange.imgpub=request.FILES[f'{id}']
                editMSG=True
                imageChange.save()
        except:pass
        try:
            if request.FILES[f'{pubObjectInfo["ImagesID"][0]}']:
                imageChange=PubInfo.objects.get(pk=pubObjectInfo["ImagesID"][0])
                imageChange.imgpub=request.FILES[f'{pubObjectInfo["ImagesID"][0]}']
                editMSG=True
                imageChange.save()
        except:pass
        try:
            if request.FILES[f'{pubObjectInfo["ImagesID"][1]}']:
                imageChange=PubInfo.objects.get(pk=pubObjectInfo["ImagesID"][1])
                imageChange.imgpub=request.FILES[f'{pubObjectInfo["ImagesID"][1]}']
                editMSG=True
                imageChange.save()
        except:pass
        try:
            if request.FILES[f'{pubObjectInfo["ImagesID"][2]}']:
                imageChange=PubInfo.objects.get(pk=pubObjectInfo["ImagesID"][2])
                imageChange.imgpub=request.FILES[f'{pubObjectInfo["ImagesID"][2]}']
                editMSG=True
                imageChange.save()
        except:pass
        try:
            if request.FILES[f'{pubObjectInfo["ImagesID"][3]}']:
                imageChange=PubInfo.objects.get(pk=pubObjectInfo["ImagesID"][3])
                imageChange.imgpub=request.FILES[f'{pubObjectInfo["ImagesID"][3]}']
                editMSG=True
                imageChange.save()
        except:pass
        
        def requestImgSave(archive, id=id):
            countImgaddr=[]
            for a in PubInfo.objects.all():
                if f"{str(PubInfo.objects.get(pk=id).titulo)}-" in a.titulo:
                    countImgaddr.append(a.titulo)
            infoPub=PubInfo(
                creator=id,
                imgpub=archive,
                titulo=f'{str(PubInfo.objects.get(pk=id).titulo)}-{len(countImgaddr)}'
            )
            infoPub.save()
        
        def requestDELImg(idDel):
            PubInfo.objects.get(id=idDel).delete()
            print('requisição efetuada')

        try:
            try:

                convertFile=request.FILES['1']
                if request.FILES['1'] and str(request.FILES['1'])!='file0.txt': 
                    requestImgSave(request.FILES['1'])
                elif str(request.FILES['1'])=='file0.txt':
                    fileDecode=int.from_bytes(convertFile.read(), byteorder='big') 
                    requestDELImg(fileDecode)
                else:
                    convertFile=False
                editMSG=True if convertFile!=False else False
                
            except:pass
            sleep(0.5)
            try:
                convertFile=request.FILES['2']
                if request.FILES['2'] and str(request.FILES['2'])!='file0.txt': 
                    requestImgSave(request.FILES['2'])
                elif str(request.FILES['2'])=='file0.txt':
                    fileDecode=int.from_bytes(convertFile.read(), byteorder='big') 
                    requestDELImg(fileDecode)
                else:
                    convertFile=False
                editMSG=True if convertFile!=False else False
            except:pass
            sleep(0.5)
            try:
                convertFile=request.FILES['3']
                if request.FILES['3'] and str(request.FILES['3'])!='file0.txt': 
                    requestImgSave(request.FILES['3'])
                elif str(request.FILES['3'])=='file0.txt':
                    fileDecode=int.from_bytes(convertFile.read(), byteorder='big') 
                    requestDELImg(fileDecode)
                else:
                    convertFile=False
                editMSG=True if convertFile!=False else False
            except:pass
            sleep(0.5)
            try:
                convertFile=request.FILES['4']
                if request.FILES['4'] and str(request.FILES['4'])!='file0.txt': 
                    requestImgSave(request.FILES['4'])
                elif str(request.FILES['4'])=='file0.txt':
                    fileDecode=int.from_bytes(convertFile.read(), byteorder='big') 
                    requestDELImg(fileDecode)
                else:
                    convertFile=False
                editMSG=True if convertFile!=False else False
            except:pass
        except:pass
        sleep(0.5)
        if editMSG==True:
            messages.success(request, 'Publicação Editada')
        else:
            messages.success(request, 'Nenhuma Alteração Efetuada')
        return redirect(reverse(edit_post, args=[userObject.enctype_hash, id]))    
    def editarPub():
        pass
    return render(request, 'html/edit_post0.html', pubObjectInfo)


def delete_post(request, id, hash):
    #delete de account integrado
    global verify0, verify01, userObject
    
    excluir_account=0

    if request.method=="POST":
        try: excluir_account=int(request.POST.get('integrar')) if int(request.POST.get('integrar'))==1 else False
        except: excluir_account=0
        print(f'request:{request.POST.get('integrar')}')
        if excluir_account==1:
            #Efetua a exclusão da conta e da info referente a conta
            for deleteUserInfo in user_info.objects.all():
                if deleteUserInfo.id == id:
                    creatorInfoDelete=None
                    DeleteUserInfo=list()
                    ImageDel=list()
                    for UserInfDelete in PubInfo.objects.all():
                        if UserInfDelete.creator==id:
                            DeleteUserInfo.append(UserInfDelete.id)
                            creatorInfoDelete=UserInfDelete.id
                            ImageDel.append(UserInfDelete.imgpub)
                        if creatorInfoDelete==UserInfDelete.creator:
                            DeleteUserInfo.append(UserInfDelete.id)
                            ImageDel.append(UserInfDelete.imgpub)
                    for DeleteImage in ImageDel:
                        if os.path.exists(f'media/{str(DeleteImage)}'):
                            print('request image delete')
                            os.remove((f'media/{str(DeleteImage)}'))
                    for DeletePubsUser in DeleteUserInfo:
                        PubInfo.objects.get(id=DeletePubsUser).delete()
            sleep(0.5)
            user_info.objects.get(id=id).delete()
            verify0=verify01=0
            print('Usuario e infos deletados')
            return redirect(home)
        else:
            deletar_pub(id)
            return redirect(home)
        
    return redirect(home)

 
def notify_request(request, hash):
    #efetua a notificação via user interligando a request 
    global userObject
    context={'info':{'msg':[],'user':[],'pub_name':[],'pub_id':[]},
            'log_info':{'msg':[],'user':[],'pub_name':[],'pub_id':[],'resposta':[]}
             }
    context['login_display']='none'
    context['logout_display']=True
    context['notification']=False
    context['user_name']=userObject.nome
    context['key_user']=userObject.enctype_hash
    context['tipo_user']= True if int(userObject.tipo)==1 else False
    for requisicao in RequisicaoAdotar.objects.all():
        if requisicao.destinatario==userObject.id and requisicao.log_on==False:
            context['id_remetente']=requisicao.remetente
            context['info']['msg'].append(requisicao.msg)
            context['info']['user'].append(user_info.objects.get(pk=requisicao.remetente).nome)
            context['info']['pub_name'].append(PubInfo.objects.get(pk=requisicao.pub_selec).titulo)
            context['info']['pub_id'].append(requisicao.id)
        elif requisicao.remetente==userObject.id and requisicao.log_on==True:
            context['log_info']['msg'].append(requisicao.msg)
            context['log_info']['user'].append(user_info.objects.get(pk=requisicao.destinatario).nome)
            context['log_info']['pub_name'].append(PubInfo.objects.get(pk=requisicao.pub_selec).titulo)
            context['log_info']['resposta'].append(requisicao.resposta)
            context['log_info']['pub_id'].append(requisicao.id)
        elif requisicao.destinatario==userObject.id and requisicao.log_on==True:
            context['log_info']['msg'].append(requisicao.msg)
            context['log_info']['user'].append(user_info.objects.get(pk=requisicao.destinatario).nome)
            context['log_info']['pub_name'].append(PubInfo.objects.get(pk=requisicao.pub_selec).titulo)
            context['log_info']['resposta'].append(requisicao.resposta)
            context['log_info']['pub_id'].append(requisicao.id)
    if request.method=='POST':
        request_answear=RequisicaoAdotar.objects.get(pk=int(request.POST.get('request0')))
        request_answear.destinatario=context['id_remetente']
        request_answear.remetente=userObject.id
        request_answear.resposta=str(request.POST.get('request_answear'))
        request_answear.log_on=True
        try:
            request_answear.save()
            print('Dados Salvos')
        except:
            print('error no save')
            pass
        return HttpResponse(f'Requisitando resposta a pub Novo destinatario:{context['id_remetente']} requisitado por:{userObject.nome, userObject.id} Resposta:{request.POST.get('request_answear')}') 
    return render(request, 'html/notify.html',context)


def request_fav(request):
    global userObject, Fav_user
    context={'id_pub':[], 'fav_img0':[], 'info_pub':[{'titulo':[],}]}
    context['fav_on']=False
    context['key_user']=userObject.enctype_hash
    pubsId=[a.id for a in PubInfo.objects.all()]

    if request.method=='GET':
        for a in Fav_user.objects.all():
            if a.user_id == userObject.id and a.id_pub in pubsId:
                context['fav_on']=True
                context['id_pub'].append(PubInfo.objects.get(id=a.id_pub))
                
                print(a.id_pub)
                context['fav_img0'].append(PubInfo.objects.get(id=a.id_pub).imgpub)

        return render(request, 'html/favpage.html', context)


def nav_barHome(request):
    global verify0,userObject, pubInfo
    pubInfoObject()

    context={'pubs':{'titulo':[],'img_pub':[],'tipo_a':[],'pub_id':[]}, 'pub_index0':[]}
    context['pubInf0']=pubInfo
    if verify0==1:
        context['login_display']='none'
        context['logout_display']=True
        context['user_name']=userObject.nome

    for request_pubId in PubInfo.objects.all():
        if '-' not in str(request_pubId.titulo):
            context['pubs']['titulo'].append(str(PubInfo.objects.get(pk=request_pubId.id).titulo))
            context['pubs']['tipo_a'].append(str(PubInfo.objects.get(pk=request_pubId.id).tipo_n))
            context['pubs']['img_pub'].append(str(PubInfo.objects.get(pk=request_pubId.id).imgpub))
            context['pubs']['pub_id'].append(PubInfo.objects.get(pk=request_pubId.id).id)
    try:
        for test in PubInfo.objects.all():
            try:
                if context['pub_id']!=test.creator:
                    context['pub_index0'].append(PubInfo.objects.get(pk=test.id))
                    context['pub_id']=test.id
                    context['key_user']=user_info.objects.get(pk=test.creator).enctype_hash
                else:
                    print(f'Passando ID:{test.id}')
            except:                
                context['pub_index0'].append(PubInfo.objects.get(pk=test.id))  
                context['pub_id']=test.id
    except:
        pass
    return render(request, 'html/pet_find.html', context)


def request_adot(request, hash, id_pub, name):
    #executa a comunicação de requisição de adoção
    global verify0, userObject
    destinatario0=0
    pub_name=''
    context={'pub_file':[], 'fav_on':False}
    context['key_user']=hash
    context['name_pub']=name
    if request.method=='POST':
        get_destino=PubInfo.objects.get(pk=id_pub).creator
        for verify_creator in PubInfo.objects.all():
            if verify_creator.creator==id_pub:
                id_pub=verify_creator.id
                pub_name=verify_creator.titulo
                destinatario0=verify_creator.creator
                break
        try:
            if len(RequisicaoAdotar.objects.all())>0:
                try:
                    for msg_sent in RequisicaoAdotar.objects.all():
                        if msg_sent.remetente == userObject.id and id_pub==msg_sent.pub_selec:
                            #redireciona a page de requisição
                            return HttpResponse('Requisição Já encaminhada')
                except:
                    pass
        
            print(f'request id:{id_pub} destinatario{destinatario0}')
            mensage_sent=RequisicaoAdotar(
                remetente=userObject.id,
                destinatario=user_info.objects.get(pk=int(get_destino)).id,
                pub_selec=id_pub,
                msg=str(request.POST.get('message_input')),
                )
            
            print('INIT SAVE0')
            mensage_sent.save()
            return redirect(home) 
        except:
            print('error')
            return HttpResponse('ERROR init')