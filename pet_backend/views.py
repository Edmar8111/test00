from django.shortcuts import render, redirect, get_object_or_404
import shortuuid
from django.http import HttpResponse
from .models import user_info, user_complemento, PubInfo, Fav_user, RequisicaoAdotar
from time import sleep
import os
valor0 = 0
valor1 = 0
verify0=0
verify01=0
verify_list=[]

#efetua o cadastro do usuario no db
def cadastro_user(metodo_acesso_user, nome_user, email_user, pass_word, telefone_user, cidade_user):
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

#home refinamento direcionando via nav bar interno
def home(request):
    # for delet in RequisicaoAdotar.objects.all():
    #     RequisicaoAdotar.objects.get(pk=delet.id).delete()

    global verify0, verify01, verify_list
    verify_list=[]
    def verify_notify(id_user):
        for verificar_notifica in RequisicaoAdotar.objects.all():
            if verificar_notifica.destinatario==id_user and verificar_notifica.log_on==False:
                verify_list.append(verificar_notifica.pub_selec)
            
        return verify_list
        
    if verify0==1 and verify01==1:
        context={
        'logo': 'image/petconnect.svg',
        'login_display':'none',
        'logout_display':True,
        'key_user':valor0.enctype_hash,
        'user_name':valor0.nome,
        'pub_index':[],
        'notification':False,
        }

        
        verify_notify(valor0.id)
        if len(verify_list)>0:
            context['notification']=True
           
        try:
            for test in PubInfo.objects.all():
                try:
                    if context['pub_id']!=test.creator:
                        context['pub_index'].append(PubInfo.objects.get(pk=test.id))
                        context['pub_id']=test.id
                    else:
                        print(f'Passando ID:{test.id}')
                except:                
                    context['pub_index'].append(PubInfo.objects.get(pk=test.id))  
                    context['pub_id']=test.id
        except:
            pass
          
        return render(request, 'html/home.html', context)
    if verify0==1 and verify01==0:
        context={
        'logo': 'image/petconnect.svg',
        'login_display':'none',
        'logout_display':True,
        'key_user':valor0.enctype_hash,
        'user_name':valor0.nome,
        'pub_index':[],
        'notification':False,
        }

        verify_notify(valor0.id)
        if len(verify_list)>0:
            context['notification']=True
        try:
            for test in PubInfo.objects.all():
                try:
                    if context['pub_id']!=test.creator:
                        context['pub_index'].append(PubInfo.objects.get(pk=test.id))
                        context['pub_id']=test.id
                    else:
                        pass
                except:                
                    context['pub_index'].append(PubInfo.objects.get(pk=test.id))  
                    context['pub_id']=test.id
        except:
            pass
        return render(request, 'html/home.html', context)
    
    if verify0==0:
        verify_list=[]
        context={
        'logo': 'image/petconnect.svg',
        'login_display':'block',
        'logout_display':False,
        'pub_index':[]
        }
        try:
            for test in PubInfo.objects.all():
                try:
                    if context['pub_id']!=test.creator:
                        context['pub_index'].append(PubInfo.objects.get(pk=test.id))
                        context['pub_id']=test.id
                        context['key_user']=user_info.objects.get(pk=test.creator).enctype_hash
                    else:
                        print(f'Passando ID:{test.id}')
                except:                
                    context['pub_index'].append(PubInfo.objects.get(pk=test.id))  
                    context['pub_id']=test.id
        except:
            pass
        return render(request, 'html/home.html', context)
    
def perfil_user(request, key_inst):
    global valor0, verify0, verify01
    #criar a indexação de pub e favoritos user
    def verify_notify(id_user):
        for verificar_notifica in RequisicaoAdotar.objects.all():
            if verificar_notifica.destinatario==id_user and verificar_notifica.log_on==False:
                verify_list.append(verificar_notifica.pub_selec)
        return
    context={
        'key_user':valor0.enctype_hash,
        'login_display':'none',
        'user_name':valor0.nome,
        'user_id':valor0.id,
        'logout_display':True,
        'notification':False,
    }
    context['ong_true']=True if int(valor0.tipo)==1 else False
    verify_notify(valor0.id)
    if len(verify_list)>0:
        context['notification']=True

    if request.method=='GET':
        context['key_user']=valor0.enctype_hash
        if request.GET.get('click_logout')!=None or verify0==0:
            verify0=0
            return redirect(home)
        if request.GET.get('click_edit')!=None:
            return redirect(complemento_info)
        return render(request, 'html/menuUser.html', context)

def complemento_info(request):
    global valor1, valor0, verify0, verify01

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
            'nome':valor0.nome,
            'email':valor0.email,
            'cidade':valor0.cidade,
            'key_user':valor0.enctype_hash,
            'user_name':valor0.nome
        }

        verify_notify(valor0.id)    
        if len(verify_list)>0:
            context['notification']=True

        for loop_inf in uc.objects.all():
            if loop_inf.cep and loop_inf.id_id==valor0.id:
                valor1=loop_inf.id
                context['cep']=loop_inf.cep
            if loop_inf.cpf and loop_inf.id_id==valor0.id:
                context['cpf']=loop_inf.cpf
            if loop_inf.estado and loop_inf.id_id==valor0.id:
                context['estado']=loop_inf.estado
            if loop_inf.endereco and loop_inf.id_id==valor0.id:
                context['endereco']=loop_inf.endereco
            if loop_inf.rua and loop_inf.id_id==valor0.id:
                context['rua']=loop_inf.rua
            if loop_inf.numero and loop_inf.id_id==valor0.id:
                context['numero']=loop_inf.numero
            if loop_inf.complemento and loop_inf.id_id==valor0.id:
                context['complemento']=loop_inf.complemento
            if loop_inf.date and loop_inf.id_id==valor0.id:
                context['date']=loop_inf.date
        
        
        return render(request, 'html/complemento_info.html', context)

    # if verify0==1:
    #     print('Criar menu user')
    #     context['nome']=valor0.nome
    #     context['email']=valor0.email
    #     context['cidade']=valor0.cidade
    #     context['key_user']=valor0.enctype_hash    
    
    if request.method == 'POST':
        if valor1==0:
            for search_user in user_complemento.objects.all():
                if search_user.id_id == valor0.id:
                    valor1=search_user.id
        #fetuar verificação de dados existentes
        id_saver = user_complemento.objects.get(id=valor1)
        id_saver0 = user_info.objects.get(id=valor0.id)
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
    global verify0,valor0, verify01
    if user_complemento.objects.all():
        for user_comp_verify in user_complemento.objects.all():
            if user_comp_verify.id_id == valor0.id:
                verify(1)   
                data_complement = user_comp_verify
                break
        if verify0==1 and verify01 == 0 and data_complement.cep and data_complement.cpf and data_complement.estado and data_complement.endereco :
            return redirect(home)
        if verify01==1 and verify0==0:
            verify0=1
            verify01=0
            return redirect(complemento_info)
        else:
            #criar msg no front que retorne a requisição de complementação do usuario
            return redirect(complemento_info)
            
def login(request):
    global valor0,verify01,verify0
    context={
        'logo':'image/petconnect.svg',
        'msg_display':'none',
        'logout_display':False,
    } 
    # for delete in user_info.objects.all():
    #       user_info.objects.get(pk=delete.id).delete()

    if request.method == 'POST':
        for verificar in user_info.objects.all():
            if request.POST.get('email') == verificar.email and request.POST.get('password') == verificar.senha:
                valor0 = user_info.objects.get(pk=verificar.id)
                return redirect(login_user_verify)
            
        context['msg_display']='block'
        return render(request, 'html/login.html', context)
                
    if request.method == 'GET':
        if verify0==1:
            try:
                valor0=user_info.objects.get(id=valor0.id)
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
    global valor0, verify0, verify01
    img_save={}

    inst_hash=valor0.enctype_hash
    if request.method=='GET' and verify0==1:
            return render(request, 'html/cadastrol_pet.html', {'key_inst':inst_hash})
    if request.method=='POST' and verify0==1:
        list_t={}
        for pub_test in PubInfo.objects.all():
            list_t['url:']=pub_test.imgpub
            if int(pub_test.creator)==int(valor0.id):
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
            creator=valor0.id,
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
        
        return redirect(f'http://127.0.0.1:8000/petconnect/menu={valor0.enctype_hash}')
    else:
        return redirect(home)

def pubIndex(request, inst_hash):
    global verify0, valor0
    pub_inf={}
    cont_pub=0
    for pub in PubInfo.objects.all():
        #efetuar verificação se há pub adicionais do user
        if int(pub.creator)==valor0.id:
            pub_inf['file0']=[
                pub.id,pub.titulo,pub.imgpub,
                pub.data_pub,pub.castramento]
            break
    for pub0 in PubInfo.objects.all():
        
        if int(pub0.creator)==valor0.id:
            cont_pub+=1
        if cont_pub>5:
            break
        if cont_pub==2:
            try:
                if len(pub_inf['file1'])==0:
                    pub_inf['file1']=[
                        pub0.id,pub0.titulo,pub0.imgpub,
                        pub0.data_pub,pub0.castramento]
                else:
                    pass
            except:
                    pub_inf['file1']=[
                        pub0.id,pub0.titulo,pub0.imgpub,
                        pub0.data_pub,pub0.castramento]
        if cont_pub==3:
            try:
                if len(pub_inf['file2'])==0:
                    pub_inf['file2']=[
                        pub0.id,pub0.titulo,pub0.imgpub,
                        pub0.data_pub,pub0.castramento]
                else:
                    pass
            except:
                pub_inf['file2']=[
                        pub0.id,pub0.titulo,pub0.imgpub,
                        pub0.data_pub,pub0.castramento]
        if cont_pub==4:
            try:
                if len(pub_inf['file3'])==0:
                    pub_inf['file3']=[
                        pub0.id,pub0.titulo,pub0.imgpub,
                        pub0.data_pub,pub0.castramento]
                else:
                    pass
            except:
                pub_inf['file3']=[
                        pub0.id,pub0.titulo,pub0.imgpub,
                        pub0.data_pub,pub0.castramento]
        if cont_pub==5:
            pub_inf['file4']=[
                pub0.id,pub0.titulo,pub0.imgpub,
                pub0.data_pub,pub0.castramento]
            break
          
    # for pub in PubInfo.objects.all():
    #      pub.delete()
    titulo=titulo0=titulo1=titulo2=titulo3=False
    url=url0=url1=url2=url3=False
    try:
        if pub_inf['file0'][1]:
            titulo=True
        if pub_inf['file0'][2]:
            url=True
        if pub_inf['file1'][1]:
            titulo0=str(pub_inf['file1'][1])
        if pub_inf['file1'][2]:
            url0=pub_inf['file1'][2]
        if pub_inf['file2'][1]:
            titulo1=str(pub_inf['file2'][1])
        if pub_inf['file2'][2]:
            url1=pub_inf['file2'][2]
        if pub_inf['file3'][1]:
            titulo2=str(pub_inf['file3'][1])
        if pub_inf['file3'][2]:
            url2=pub_inf['file3'][2]
        if pub_inf['file4'][1]:
            titulo3=str(pub_inf['file4'][1])
        if pub_inf['file4'][2]:
            url3=pub_inf['file4'][2]
    except:
        pass
    if verify0==1:
            inst_hash=valor0.enctype_hash
            context={
                'key_inst':inst_hash,
                'titulo':pub_inf['file0'][1] if titulo!=False else False,
                'img0':pub_inf['file0'][2] if url!=False else False,
                'creator':valor0.nome,
                'key_hash':valor0.enctype_hash,
                'id_user':valor0.id,
                'titulo0':titulo0 if titulo0!=False else False,
                'img00':url0 if url0!=False else False,
                'titulo1':titulo1 if titulo1 != False else False,
                'img1':pub_inf['file2'][2] if url1 != False else False,
                'titulo2':titulo2 if titulo2 != False else False,
                'img2':pub_inf['file3'][2] if url2 != False else False,
                'titulo3':titulo3 if titulo3 != False else False,
                'img3':pub_inf['file4'][2] if url3 != False else False,
            }
            return render(request,'html/pubs_page.html', context)

    else:
        return HttpResponse('Error INIT')

#tela de display de adoção
def post_detail(request, id, name):
    global valor0
    context={'pub_file':[], 'fav_on':False, 'pub_id':0}
    context['name_pub']=name
    try: 
        context['key_user']=valor0.enctype_hash
    except:
        pass
    def verify_image():
        try:
            for pub0 in PubInfo.objects.all():
                if pub0.creator==context['id'] and pub0.titulo!=name:
                    context['pub_file'].append(pub0.imgpub)
        except:
            return
    def get_pub(id_pub=id, exec_0='INIT', exec_1='INIT'):
            global valor0
            context['login_display']='none'
            context['logout_display']=True
            context['user_name']=valor0.nome
            context['user_id']=valor0.id
            context['verify']=verify0 if verify0==1 else False
            for pub_inf in PubInfo.objects.all():   
                if pub_inf.creator==id_pub and name==pub_inf.titulo and valor0.id==pub_inf.creator: 
                    context['id']=pub_inf.id
                    context['titulo']=pub_inf.titulo
                    context['data']=pub_inf.data_pub
                    context['castrado']='Sim' if pub_inf.castramento==True else 'Não'
                    context['img0']=pub_inf.imgpub
                    context['creator']=pub_inf.creator
                    verify_image()
                    break
                elif pub_inf.id==id_pub and name==pub_inf.titulo and id_pub!=valor0.id:
                    context['id']=pub_inf.id
                    context['titulo']=pub_inf.titulo
                    context['data']=pub_inf.data_pub
                    context['castrado']='Sim' if pub_inf.castramento==True else 'Não'
                    context['img0']=pub_inf.imgpub
                    context['creator']=pub_inf.creator
                    verify_image()
                    break
            try:
                for a in PubInfo.objects.all():
                    if a.titulo == context['name_pub']:
                        context['pub_id']=a.id
                        break 
            except:
                pass
            exec_1=context['pub_id']
            return print(f'{exec_0}, tec{exec_1}')
                
    def fav_v():
            for verify_fav in Fav_user.objects.all():
                if verify_fav.user_id==context['user_id'] and verify_fav.id_pub==context['pub_id']:
                    context['fav_on']=True

    if verify0==0 and request.method=='GET':
        try:
            try:    
                for pub0 in PubInfo.objects.all():  
                    if pub0.id==id:
                        context['inst_hash']=user_info.objects.get(pk=pub0.creator).enctype_hash 
                        context['img0']=pub0.imgpub
                        context['id_pub']=pub0.id
                    if pub0.creator==id and pub0.titulo!=name:
                        context['pub_file'].append(pub0.imgpub)
                pass
            except:
                pass
            for test in PubInfo.objects.all():
                try:
                    hash=user_info.objects.get(pk=test.creator).enctype_hash
                    context['user_id']=user_info.objects.get(pk=test.creator).id
                except:
                    pass
            context['verify']=verify0 if verify0==1 else False
            print(context['img0'])
            return render(request, 'html/page_pet.html', context)
        except:
            return render(request, 'html/page_pet.html', context)
    
    if request.method=='GET' and verify0==1:        
        context['key_user']=valor0.enctype_hash
        get_pub()
        fav_v()
        context['titulo']=name
        return render(request, 'html/page_pet.html', context)
    if request.method=='POST' and int(request.POST.get('click_fav'))==1:
        get_pub(exec_0='INIT0')
        
        save_fav=Fav_user(
            id_pub=context['pub_id'],
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
        get_pub()
        for exec_del in Fav_user.objects.all():
            if exec_del.id_pub == context['pub_id'] and exec_del.user_id == context['user_id']:
                Fav_user.objects.get(pk=exec_del.id).delete()
                break
        print('Retirado dos favoritos')
        if len(context['pub_file'])==0:            
            try:
                get_pub(id_pub=context['pub_id'])
            except:
                print('error pub')
                pass
        fav_v()
        return render(request, 'html/page_pet.html', context)
    
    if request.method=='POST' and int(request.POST.get('click_fav'))==0:
        #modo de exclusão cascata
        if int(request.POST.get('bt_delete'))==1:
            for exec_delete in PubInfo.objects.all(): 
                if int(exec_delete.creator)==id:
                        delet_pub=PubInfo.objects.get(pk=int(exec_delete.id))
                        if os.path.exists(f'media/{exec_delete.imgpub}'):
                            os.remove(f'media/{exec_delete.imgpub}')
                        delet_pub.delete()
                if exec_delete.creator==valor0.id and exec_delete.id == id:
                    delet_pub = PubInfo.objects.get(pk=int(exec_delete.id))
                    if os.path.exists(f'media/{exec_delete.imgpub}'):
                            os.remove(f'media/{exec_delete.imgpub}')
                    delet_pub.delete()
            return redirect(home)
        #executar return de forma direta
    
        return render(request, 'html/pubPage.html', context)

def edit_post(request, hash, id):
    global verify0, valor0
    context={'pub_file':[]}
    try: context['id']=valor0.id 
    except: pass
    hash=get_object_or_404(user_info, enctype_hash=hash)

    if verify0==1 and request.method=='GET':
        for verifica_pub in PubInfo.objects.all():
            if verifica_pub.creator==valor0.id and verifica_pub.id==id:
                context['pub_inf0']=PubInfo.objects.get(pk=verifica_pub.id)
                context['id']=PubInfo.objects.get(pk=verifica_pub.id).id
                break
        context['inst_hash']=valor0.enctype_hash
        for a in PubInfo.objects.all():
            if int(a.creator)==id:
                context['pub_file'].append(a.imgpub)
            if int(a.creator)==valor0.id and a.id==id:
                context['pub_file'].append(a.imgpub)
        return render(request, 'html/edit_post.html', context)
    if request.method=='POST':
            hash=valor0.enctype_hash
            pub_save=PubInfo.objects.get(pk=id)
            pub_save.titulo=request.POST.get('titulo_new')
            pub_save.save()
            try:
                v_img=False
                if request.FILES['file0']:
                    for v in PubInfo.objects.all():
                        if v.imgpub==request.POST.get('file01'):
                            v_img=PubInfo.objects.get(pk=int(v.id))
                            break
                v_img.imgpub=request.FILES['file0']
                v_img.save()
            except:
                pass
            try:
                if request.FILES['file1']:
                    for v in PubInfo.objects.all():
                      if v.imgpub==request.POST.get('file02'):
                        v_img=PubInfo.objects.get(pk=int(v.id))
                        break
                    v_img.imgpub=request.FILES['file1']
                    v_img.save()
            except:
                pass
            try:    
                if request.FILES['file2']:
                    for v in PubInfo.objects.all():
                      if v.imgpub==request.POST.get('file03'):
                        v_img=PubInfo.objects.get(pk=int(v.id))
                        break
                    v_img.imgpub=request.FILES['file2']
                    v_img.save()
            except:
                pass
            try:
                if request.FILES['file3']:
                    for v in PubInfo.objects.all():
                      if v.imgpub==request.POST.get('file04'):
                        v_img=PubInfo.objects.get(pk=int(v.id))
                        break
                    v_img.imgpub=request.FILES['file3']
                    v_img.save()
            except:
                pass
            try:
                if request.FILES['file4']:
                    for v in PubInfo.objects.all():
                      if v.imgpub==request.POST.get('file05'):
                        v_img=PubInfo.objects.get(pk=int(v.id))
                        break
                    v_img.imgpub=request.FILES['file4']
                    v_img.save()    
            except:
                pass
            for pub0 in PubInfo.objects.all():
                if int(pub0.creator)==id :
                    context['pub_file'].append(pub0.imgpub)
                if pub0.creator==valor0.id and id==pub0.id:
                    context['pub_file'].append(pub0.imgpub)
            for test in PubInfo.objects.all():
                if test.creator==valor0.id and id==test.id:
                    context['titulo']=test.titulo
                    context['inst_hash']=valor0.enctype_hash
                    context['id']=test.id
                    #efetuar requisição da pub atualizada
                    try:    
                        return render(request, 'html/pubPage.html', context)
                    except:
                        return HttpResponse('Error init')
    else:
        return redirect(login)

#delete de account integrado
def delete_post(request, id, hash):

    global verify0, verify01, valor0
    list_del=[]
    excluir_account=False
    if request.method=="POST":
        try:
            excluir_account=True if int(request.POST.get('integrar'))==1 else False
        
        except:
            pass
        if excluir_account==False:
            try:
                #executa o delete de td referente a pub do user
                for exec_delete in PubInfo.objects.all(): 
                    if int(exec_delete.creator)==id:
                            delet_pub=PubInfo.objects.get(pk=int(exec_delete.id)).id
                            if os.path.exists(f'media/{exec_delete.imgpub}'):
                                os.remove(f'media/{exec_delete.imgpub}')
                            list_del.append(delet_pub)
                    if exec_delete.creator==valor0.id and exec_delete.id == id:
                        delet_pub = PubInfo.objects.get(pk=int(exec_delete.id)).id
                        if os.path.exists(f'media/{exec_delete.imgpub}'):
                                os.remove(f'media/{exec_delete.imgpub}')
                        list_del.append(delet_pub)
                print(list_del)
                for a in range(len(list_del)-1,-1,-1 ):
                    PubInfo.objects.get(pk=list_del[a]).delete()   
        #        redireciona para page
                return redirect(home)
            except:
                
                return HttpResponse('ERROR INIT')
                pass 
        
        #efetua o delete em modo cascade de tds as info referente ao user
        if excluir_account==True:
            for exec_delete in PubInfo.objects.all(): 
                if int(exec_delete.creator)==id:
                        delet_pub=PubInfo.objects.get(pk=int(exec_delete.id))
                        if os.path.exists(f'media/{exec_delete.imgpub}'):
                            os.remove(f'media/{exec_delete.imgpub}')
                        delet_pub.delete()
                if exec_delete.creator==valor0.id and exec_delete.id == id:
                    delet_pub = PubInfo.objects.get(pk=int(exec_delete.id))
                    if os.path.exists(f'media/{exec_delete.imgpub}'):
                            os.remove(f'media/{exec_delete.imgpub}')
                    delet_pub.delete()
            for exec_logsDEL in RequisicaoAdotar.objects.all():
                if exec_logsDEL.destinatario==valor0.id or exec_logsDEL.remetente==valor0.id:
                    RequisicaoAdotar.objects.get(pk=exec_logsDEL.id).delete()
            del_user = user_info.objects.get(pk=id)
            del_user.delete()
            verify0=0
            verify01=0
            return redirect(home)

        # for dele_image in PubInfo.objects.all():
        #     if dele_image.id==id:
        #         list_del.append(dele_image.id)
        #     if dele_image.creator==id:
        #         list_del.append(dele_image.id)
        # sleep(0.5)
        # for a in range(len(list_del)-1,-1,-1 ):
        #     PubInfo.objects.get(pk=list_del[a]).delete()      
        
    return redirect(home)

#efetua a notificação via user interligando a request  
def notify_request(request, hash):
    global valor0
    context={'info':{'msg':[],'user':[],'pub_name':[],'pub_id':[]},
            'log_info':{'msg':[],'user':[],'pub_name':[],'pub_id':[],'resposta':[]}
             }
    context['login_display']='none'
    context['logout_display']=True
    context['notification']=False
    context['user_name']=valor0.nome
    context['key_user']=valor0.enctype_hash
    context['tipo_user']= True if int(valor0.tipo)==1 else False
    for requisicao in RequisicaoAdotar.objects.all():
        if requisicao.destinatario==valor0.id and requisicao.log_on==False:
            context['id_remetente']=requisicao.remetente
            context['info']['msg'].append(requisicao.msg)
            context['info']['user'].append(user_info.objects.get(pk=requisicao.remetente).nome)
            context['info']['pub_name'].append(PubInfo.objects.get(pk=requisicao.pub_selec).titulo)
            context['info']['pub_id'].append(requisicao.id)
        elif requisicao.remetente==valor0.id and requisicao.log_on==True:
            context['log_info']['msg'].append(requisicao.msg)
            context['log_info']['user'].append(user_info.objects.get(pk=requisicao.destinatario).nome)
            context['log_info']['pub_name'].append(PubInfo.objects.get(pk=requisicao.pub_selec).titulo)
            context['log_info']['resposta'].append(requisicao.resposta)
            context['log_info']['pub_id'].append(requisicao.id)
        elif requisicao.destinatario==valor0.id and requisicao.log_on==True:
            context['log_info']['msg'].append(requisicao.msg)
            context['log_info']['user'].append(user_info.objects.get(pk=requisicao.destinatario).nome)
            context['log_info']['pub_name'].append(PubInfo.objects.get(pk=requisicao.pub_selec).titulo)
            context['log_info']['resposta'].append(requisicao.resposta)
            context['log_info']['pub_id'].append(requisicao.id)
    if request.method=='POST':
        request_answear=RequisicaoAdotar.objects.get(pk=int(request.POST.get('request0')))
        request_answear.destinatario=context['id_remetente']
        request_answear.remetente=valor0.id
        request_answear.resposta=str(request.POST.get('request_answear'))
        request_answear.log_on=True
        try:
            request_answear.save()
            print('Dados Salvos')
        except:
            print('error no save')
            pass
        return HttpResponse(f'Requisitando resposta a pub Novo destinatario:{context['id_remetente']} requisitado por:{valor0.nome, valor0.id} Resposta:{request.POST.get('request_answear')}') 
    return render(request, 'html/notify.html',context)

def request_fav(request):
    global valor0
    
    context={'id_pub':[], 'fav_img0':[], 'info_pub':[]}
    context['fav_on']=False
    context['key_user']=valor0.enctype_hash
    for verify_fav in Fav_user.objects.all():
        if verify_fav.user_id == valor0.id:
            context['info_pub'].append(PubInfo.objects.get(pk=verify_fav.id_pub).titulo)
            context['id_pub'].append(PubInfo.objects.get(pk=verify_fav.id_pub))
            context['fav_img0'].append(PubInfo.objects.get(pk=verify_fav.id_pub).imgpub)
            context['fav_on']=True
    return render(request, 'html/favpage.html', context)

def nav_barHome(request):
    global verify0,valor0
    context={'pubs':{'titulo':[],'img_pub':[],'tipo_a':[],'pub_id':[]}, 'pub_index0':[]}
    if verify0==1:
        context['login_display']='none'
        context['logout_display']=True
        context['user_name']=valor0.nome

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

#executa a comunicação de requisição de adoção
def request_adot(request, hash, id_pub, name):
    global verify0, valor0
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
                        if msg_sent.remetente == valor0.id and id_pub==msg_sent.pub_selec:
                            #redireciona a page de requisição
                            return HttpResponse('Requisição Já encaminhada')
                except:
                    pass
        
            print(f'request id:{id_pub} destinatario{destinatario0}')
            mensage_sent=RequisicaoAdotar(
                remetente=valor0.id,
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