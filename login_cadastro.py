import PySimpleGUI as sg


Theme = 'DarkBlue14' #escuro; claro: 'DarkBlue4'

sg.theme(Theme)

#JANELA INICIAL
def main_wind():
    init = [
        [sg.Text('Usuário')],  # login

        [sg.Input(key='usuario')],  # input

        [sg.Text('senha')],  # senha

        [sg.Input(key='senha', password_char='*')],  # input

        [sg.Button('SIGN IN'), sg.Button('EXIT')],  # ENTRAR

        [sg.Text('novo por aqui?')],

        [sg.Button('SIGN UP')],

        [sg.Text('', key='mensagem')],  # aparece uma mensagem dependendo do login certo ou errado
    ]
    return sg.Window('Oliveira Trade', layout=init, finalize=True)

#JANELA SECUNDÁRIA
def sign_up_wind():
    sign_up = [
        [sg.Text('nome completo')],

        [sg.Input('', key='name', size=(55,1))],

        [sg.Text('nascimento')],

        [sg.Text('dia'),sg.Input('',key='dia',size=(2,1)),
         sg.Text('mês'),sg.Input('', key='mes',size=(2,1)),
         sg.Text('ano'), sg.Input('',key='ano',size=(4,1))],

        [sg.Text('Rua:'), sg.Input('', key='rua'), sg.Text('N°:'), sg.Input('', key='number', size=(6,1))],

        [sg.Text('Estado:'), sg.Input('PA', key='state',size=(3,1)), sg.Text('CEP:'),
         sg.Input(key='cep',size=(5,1)), sg.Text('-'), sg.Input('', key='cep2', size=(3,1))],

        [sg.Text('nome da mãe')],

        [sg.Input('', key='mae', size=(55, 1))],

        [sg.Text('insira o nome de usuário')],

        [sg.Input('',key='new_user', size=(55,1))],

        [sg.Text('Email')],

        [sg.Input('',key='email', size=(55,1))],

        [sg.Text('insira sua senha')],

        [sg.Input(key='newkey', password_char='*', size=(55,1))],

        [sg.Text('repita a senha')],

        [sg.Input(key='newkey_2', password_char='*', size=(55,1))],

        [sg.Text('', key='mensagem_2')],

        [sg.Button('SAVE'), sg.Button('VOLTAR')],
    ]
    return sg.Window('CADASTRO', layout=sign_up, finalize=True)

#verificação nomes cadastrais
def nome_cadastro(nome, mae, email):
    nome = nome.split()
    nome = ''.join(nome)
    mae = mae.split()
    mae = ''.join(mae)
    if nome.isalpha() == True:
        if mae.isalpha() == True:
            if email.count('@') == 1 and email.count(' ') == 0 and email.count('.')>0:
                return 'OKA'
            else:
                return 'FORMATO DE EMAIL INVÁLIDO!'
        else:
            return 'O NOME DA MÃE PRECISA CONTEM SOMENTE LETRAS'
    else:
        return 'O NOME PRECISA CONTEM SOMENTE LETRAS'

#verificação endereço
def adress_cadastro(cep, cep2, rua, number, state):
    if cep.isnumeric() == True and cep2.isnumeric() == True and number.isnumeric() == True and state.isalpha() == True:
        if len(cep) == 5 and len(cep2) == 3 and len(state) == 2 and len(rua)>0:
            return 'OKB'
        else:
            return 'VERIFIQUE O CEP, ESTADO E RUA'
    return 'O CEP E N° RESIDÊNCIA PRECISAM SER NUMEROS E O ESTADO LETRAS'

#verificação aniversário cadastro
def aniver_cadastro(dia,mes,ano):
    if dia.isnumeric() == True and mes.isnumeric() == True and ano.isnumeric() == True:
        if 0< len(dia)<3 and 0< len(mes)<3 and len(ano)==4:
            if 0 < int(dia) < 32 and 0 < int(mes) < 13 and 1900 < int(ano) < 2023:
                return 'OKC'
            else:
                return 'insira valores validos para dia mes e ano'
        else:
            return 'valores maximos de: dia=31, mes=12, ano=2022'
    else:
        return 'insira apenas números nas datas!'

#VERIFICADOR DE NOVO LOGIN E SENHA
def login_key(user, key, key2):
    if len(user) > 0:
        if key == key2:
            if len(key) > 7:
                return 'OKD'
            else:
                return f'a senha precisa de, ao menos, 8 digitos. adicione mais {8 - len(key)}'
        else:
            return 'as senhas são incompatíveis!'
    else:
        return 'o nome do usuário necessita de ao menos um caracter'

#ADICIONANDO LOGIN E SENHA
def inserir(user, key, b):
    with open('cadastros.txt', 'a') as arquivo:
        arquivo.write(str(user) + '\n')
        arquivo.write(str(key) + '\n')
    b = True
    return b

#buscando usuarios
def busca(usuario, senha, a):
    manipulador = open('cadastros.txt', 'r')
    logins = manipulador.readlines()
    for i in range(0,len(logins)):
        if logins[i] == f'{usuario}\n' or logins[i] == usuario:
            if logins[i+1] == f'{senha}\n' or logins[i+1] == senha:
                a = True
    manipulador.close() #sempre fechar o arquivo
    return a

#CRIAÇÃO DAS JANELAS DO INICIO > apenas a primeira janela estará ativada ao iniciarmos
janela1, janela2 = main_wind(), None

#CRIAÇÃO DOS EVENTOS
while True:
# tratação de janelas, eventos e valores
    window, event, values = sg.read_all_windows()

#se a janela for fechada
    if event == sg.WIN_CLOSED or event =='EXIT':
        break
    if window == janela1 and event == 'SIGN UP':
        janela2 = sign_up_wind()
        janela1.hide()

#voltar à página principal
    if window == janela2 and event == 'VOLTAR':
        janela1.un_hide()
        janela2.hide()

#login
    if window == janela1 and event =='SIGN IN':
        a = False
        if len(values['usuario'])>0 and len(values['senha'])>0:
            if busca(values['usuario'], values['senha'], a) == True:
                window['mensagem'].update(f"bem vind@, {values['usuario'] }")
            else:
                window['mensagem'].update('USUÁRIO OU SENHA NÃO ENCONTRADOS!')
        else:
            window['mensagem'].update('INSIRA O LOGIN E SENHA!')

# salvar cadastro
    if window == janela2 and event == 'SAVE':
        key = values['newkey']
        key2 = values['newkey_2']
        user = values['new_user']
        if nome_cadastro(values['name'], values['mae'], values['email']) == 'OKA':
            if adress_cadastro(values['cep'], values['cep2'], values['rua'], values['number'], values['state']) == 'OKB':
                if aniver_cadastro(values['dia'], values['mes'], values['ano']) == 'OKC':
                    if login_key(user, key, key2) == 'OKD':
                        b = False
                        if inserir(user, key, b)==True:
                            window['mensagem_2'].update(f'Seu login foi cadastrado com sucesso, {user}')  # vai atualizar  o texto da 'mensagem2
                        else:
                            window['mensagem_2'].update(f'NOME DE USUÁRIO JÁ CADASTRADO') #nao consegui completar
                    else:
                        window['mensagem_2'].update(login_key(user, key, key2))
                else:
                    window['mensagem_2'].update(aniver_cadastro(values['dia'], values['mes'], values['ano']))
            else:
                window['mensagem_2'].update(adress_cadastro(values['cep'], values['cep2'], values['rua'], values['number'], values['state']))
        else:
            window['mensagem_2'].update(nome_cadastro(values['name'], values['mae'], values['email']))