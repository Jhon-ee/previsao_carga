import math
from tkinter import *
from tkinter import ttk,messagebox,filedialog
import mysql.connector
import tabula
import pandas as pd

#               PREVISAO DE CARGA DE ACORDO COM A NBR 5410
class Circuito(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('900x540')
        self.title('PREVISAO DE CARGA DE ACORDO COM A NBR 5410')
        self.entry_nome= Entry(self,width=35,font=('Arial',12))
        self.entry_area = Entry(self,width=35,font=('Arial',12))
        self.entry_perimetro = Entry(self,width=35,font=('Arial',12))

        self.op = ['SALAS E DORMITÓRIOS','COZINHAS, COPAS E ÁREAS DE SERVIÇO','DEMAIS CÔMODOS']
        self.entry_tipo = ttk.Combobox(self, values= self.op, width=35,font=('Arial',12))
        self.entry_tipo.grid(row=3,column=1)

        nome= Label(self,text='Nome do Cômodo',font=('Arial black',13))
        nome.grid(row=0,column=0)
        self.entry_nome.grid(row=0,column=1)

        area = Label(self,text='Área do Cômodo',font=('Arial black',13))
        area.grid(row=1,column=0)
        self.entry_area.grid(row=1,column=1)

        perimetro = Label(self,text='Perímetro',font=('Arial black',13))
        perimetro.grid(row=2,column=0)
        self.entry_perimetro.grid(row=2,column=1)

        tipo = Label(self,text='Tipo de Cômodo',font=('Arial black',13))
        tipo.grid(row=3,column=0)

        cad = Button(self,text='Registrar',command= self.cadastro,height=2, width=9,font='times 12').grid(row=0,column=3,padx=2,pady=5)
        pdf = Button(self,text='Cadastrar PDF',command=self.pdf,height=2, width=12,font='times 12').grid(row=0,column=4,padx=2,pady=5)
        up = Button(self,text='Atualizar',command=self.atualizar,height=2,width=9,font='times 12').grid(row=0,column=5,padx=2,pady=5)
        ex = Button(self,text='Excluir',command=self.excluir,height=2,width=9,font='times 12').grid(row=2,column=3,padx=2)
        ex_all = Button(self,text='Excluir Tudo',command=self.excluir_all,height=2,width=12,font='times 12').grid(row=2,column=4,padx=2)
        
        colun = ('Id','Nome','Área(m²)','Perímetro(m)','Tipo','Pot Ilum(VA)','Quant TUG','Pot TUG(VA)')
        frame = Frame(self)
        frame.grid(row=4, column=0, columnspan=8,sticky='ns',pady=40)
        scrollbar = Scrollbar(frame, orient="vertical")
        self.tab = ttk.Treeview(frame,columns= colun,show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tab.yview)
        self.tab.pack(side="left", fill="both",expand=True)
        scrollbar.pack(side="right", fill="y")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                    background="silver",
                    foreground="black",
                    rowheight=30,
                    fieldbackground="silver")

        self.tab.column('Id',width=50,anchor='center')
        self.tab.column('Nome',width=100,anchor='center')
        self.tab.column('Área(m²)',width=100,anchor='center')
        self.tab.column('Perímetro(m)',width=100,anchor='center')
        self.tab.column('Tipo',width=250,anchor='center')
        self.tab.column('Pot Ilum(VA)',width=100,anchor='center')
        self.tab.column('Quant TUG',width=80,anchor='center')
        self.tab.column('Pot TUG(VA)',width=100,anchor='center')

        for col in colun:
            self.tab.heading(col,text=col)
        
        self.consulta()
        self.tab.bind('<Double-Button-1>', self.getvalues)

    def getvalues(self,event):
        self.entry_nome.delete(0,END)
        self.entry_area.delete(0,END)
        self.entry_perimetro.delete(0,END)
        self.entry_tipo.delete(0,END)

        row_name = self.tab.selection()[0]    
        select = self.tab.set(row_name)
        self.entry_nome.insert(0,select['Nome'])
        self.entry_area.insert(0,select['Área(m²)'])
        self.entry_perimetro.insert(0,select['Perímetro(m)'])
        self.entry_tipo.insert(0,select['Tipo'])

    def ilum(self):
        if(float(self.area)<=6):
            self.pot_ilum = 100
        else:
            resto = float(self.area) - 6
            self.pot_ilum = 100
                
            for a in range(int(resto),4,-4):
                self.pot_ilum += 60

    def tug(self):
        if(self.tipo == 'SALAS E DORMITÓRIOS'):
            self.q_tug = math.ceil(float(self.perimetro)/5)
            self.pot_tug = self.q_tug * 100
            
        elif(self.tipo == 'COZINHAS, COPAS E ÁREAS DE SERVIÇO'):
            self.q_tug = math.ceil(float(self.perimetro)/3.5)    
            
            if(self.q_tug<=3):
                self.pot_tug = self.q_tug * 600
            elif(self.q_tug>3 and self.q_tug<=6):
                resto = self.q_tug - 3
                self.pot_tug = (3*600) + (resto*100)
            else:
                resto = self.q_tug - 2
                self.pot_tug = (2*600) + (resto*100)
        else:
            self.q_tug = 1
            self.pot_tug = 100

    def pdf(self):
        file_path = filedialog.askopenfilename(initialdir = "/", title = "Selecione um arquivo", filetypes = (("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")))
        pdf = tabula.read_pdf(file_path,multiple_tables=True, pages='all')
        df = pd.DataFrame(pdf[0])
        for i in range(0,len(df)):
            self.name = str(df.iloc[i,0])
            self.area = str(df.iloc[i,1])
            self.perimetro = str(df.iloc[i,2])
            cond = True
            for child in self.tab.get_children():
                if self.tab.item(child, 'values')[1] == self.name:
                    messagebox.showerror(message= f'{self.name} já existe!')
                    cond = False
                    break
            if cond:
                if (self.name.startswith('Sala') or self.name.startswith('SALA') or self.name.startswith('DORMITÓRIO') or 
                self.name.startswith('DORMITORIO') or self.name.startswith('SUITE')):
                    self.tipo = 'SALAS E DORMITÓRIOS' 
                elif (self.name.startswith('COZINHA') or self.name.startswith('Cozinha') or self.name.startswith('COPA') or 
                self.name.startswith('Copa') or self.name.startswith('ÁREA DE SERVIÇO') or self.name.startswith('ÁREA SERVIÇO')):
                    self.tipo = 'COZINHAS, COPAS E ÁREAS DE SERVIÇO'
                else:
                    self.tipo = 'DEMAIS CÔMODOS'
                
                self.ilum()
                self.tug()
                conexao = mysql.connector.connect(host="localhost", user="root", password="Jhon@123", database="previsao_carga")
                cursor = conexao.cursor()
                comando = "INSERT INTO valores (nome, area, perimetro, tipo, ilum, q_tug, pot_tug) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                valores = (self.name, self.area, self.perimetro, self.tipo, self.pot_ilum, self.q_tug, self.pot_tug)
                cursor.execute(comando,valores)
                conexao.commit()
                cursor.execute("SELECT MAX(id) FROM valores")
                id = cursor.fetchone()[0]
                self.tab.insert('','end',values=(id, self.name,self.area,self.perimetro,self.tipo, self.pot_ilum, self.q_tug, self.pot_tug))
                cursor.close()
                conexao.close()

    def cadastro(self):
        self.name = self.entry_nome.get()
        self.area = self.entry_area.get()
        self.perimetro = self.entry_perimetro.get()
        self.tipo = self.entry_tipo.get()
        
        if(self.name == '' or self.area == '' or self.perimetro == '' or self.tipo == ''):
            messagebox.showinfo('ALERTA','Por favor preencha todos os campos')    
        else:
            cond = True
            for child in self.tab.get_children():
                if self.tab.item(child, 'values')[1] == self.name:
                    messagebox.showerror(message= f'{self.name} já existe!')
                    cond = False
                    break
            if cond:
                self.ilum()
                self.tug()
                conexao = mysql.connector.connect(host="localhost", user="root", password="Jhon@123", database="previsao_carga")
                cursor = conexao.cursor()
                comando = "INSERT INTO valores (nome, area, perimetro, tipo, ilum, q_tug, pot_tug) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                valores = (self.name, self.area, self.perimetro, self.tipo, self.pot_ilum, self.q_tug, self.pot_tug)
                cursor.execute(comando,valores)
                conexao.commit()
                messagebox.showinfo("Status", "Cadastrado com Sucesso!")
            
                self.entry_nome.delete(0,END)
                self.entry_area.delete(0,END)
                self.entry_perimetro.delete(0,END)
                self.entry_tipo.delete(0,END)
            
                cursor.execute("SELECT MAX(id) FROM valores")
                id = cursor.fetchone()[0]
                self.tab.insert('','end',values=(id, self.name,self.area,self.perimetro,self.tipo, self.pot_ilum, self.q_tug, self.pot_tug))
                cursor.close()
                conexao.close()

    def consulta(self):
        conexao = mysql.connector.connect(host="localhost", user="root", password="Jhon@123", database="previsao_carga")
        cursor = conexao.cursor()
        comando = "SELECT * FROM valores"
        cursor.execute(comando)
        result = cursor.fetchall()

        for i, (id,nome, area, perim, tipo, ilum, qtug, potug) in enumerate(result,start=1):
            self.tab.insert('','end', values=(id,nome, area, perim, tipo, ilum, qtug, potug))
        
        cursor.close()
        conexao.close()
        
    def atualizar(self):
        self.name = self.entry_nome.get()
        self.area = self.entry_area.get()
        self.perimetro = self.entry_perimetro.get()
        self.tipo = self.entry_tipo.get()

        if(self.name == '' or self.area == '' or self.perimetro == '' or self.tipo == ''):
            messagebox.showinfo('ALERTA','Por favor selecione uma linha')
        else:
            self.ilum()
            self.tug()
            conexao = mysql.connector.connect(host="localhost", user="root", password="Jhon@123", database="previsao_carga")
            cursor = conexao.cursor()
            select = self.tab.focus()
            id = self.tab.item(select)["values"][0]
            comando = "UPDATE valores SET nome= %s, area= %s, perimetro= %s, tipo= %s, ilum= %s, q_tug= %s, pot_tug= %s WHERE id= %s"
            valores = (self.name, self.area, self.perimetro, self.tipo, self.pot_ilum, self.q_tug, self.pot_tug, id)
            cursor.execute(comando, valores)
            conexao.commit()
            messagebox.showinfo('Status','Atualizado com Sucesso')
            self.entry_nome.delete(0,END)
            self.entry_area.delete(0,END)
            self.entry_perimetro.delete(0,END)
            self.entry_tipo.delete(0,END)
            self.tab.item(select,values=(id, self.name, self.area, self.perimetro, self.tipo, self.pot_ilum, self.q_tug, self.pot_tug))
            cursor.close()
            conexao.close()

    def excluir_all(self):
        conexao = mysql.connector.connect(host="localhost", user="root", password="Jhon@123", database="previsao_carga")
        cursor = conexao.cursor()
        self.tab.delete(*self.tab.get_children())
        comando = "DELETE FROM valores"
        cursor.execute(comando)
        conexao.commit()
        messagebox.showinfo('Status','Deletado com Sucesso')
            
        reset = "ALTER TABLE valores AUTO_INCREMENT = 1"
        cursor.execute(reset)
        conexao.commit()
        cursor.close()
        conexao.close()
    
    def excluir(self):
        try:
            conexao = mysql.connector.connect(host="localhost", user="root", password="Jhon@123", database="previsao_carga")
            cursor = conexao.cursor()
            select = self.tab.focus()
            id = self.tab.item(select)["values"][0]
            self.tab.delete(select)
            comando = "DELETE FROM valores WHERE id = %s"
            valores = (id,)
            cursor.execute(comando,valores)
            conexao.commit()
            messagebox.showinfo('Status','Deletado com Sucesso')
            self.entry_nome.delete(0,END)
            self.entry_area.delete(0,END)
            self.entry_perimetro.delete(0,END)
            self.entry_tipo.delete(0,END)
            
            reset = "ALTER TABLE valores AUTO_INCREMENT = 1"
            cursor.execute(reset)
            conexao.commit()
            cursor.close()
            conexao.close()

        except IndexError:
            messagebox.showinfo('ALERTA','Por favor selecione uma linha')

circuito = Circuito()
circuito.mainloop()
   
# def menu2():
#     print('TOPICOS DA NORMA UTILIZADOS\n\n')
#     print('9.5.2.1.2 Na determina��o das cargas de ilumina��o pode ser adotado o seguinte crit�rio:\n')
#     print('a) em c�modos ou depend�ncias com �rea igual ou inferior a 6 m2, deve ser prevista uma carga m�nima de 100 VA\n')
#     print('b) em c�modo ou depend�ncias com �rea superior a 6 m2, deve ser prevista uma carga m�nima de 100 VA\n')
#     print('para os primeiros 6 m2, acrescida de 60 VA para cada aumento de 4 m2 inteiros.\n\n')
#     print('9.5.2.2.1 N�mero de pontos de tomada\n\n')
#     print('a) em banheiros, deve ser previsto pelo menos um ponto de tomada, pr�ximo ao lavat�rio.\n')
#     print('b) em cozinhas, copas, copas-cozinhas, �reas de servi�o, cozinha-�rea de servi�o, lavanderias e locais an�logos, deve ser previsto\n')
#     print('no m�nimo um ponto de tomada para cada 3,5 m, ou fra��o, de per�metro;\n')
#     print('c) em varandas, deve ser previsto pelo menos um ponto de tomada;\n')
#     print('d) em salas e dormit�rios devem ser previstos pelo menos um ponto de tomada para cada 5 m, ou fra��o,\n')
#     print('de per�metro.\n\n')
#     print('9.5.2.2.2 Pot�ncias atribu�veis aos pontos de tomada\n\n')
#     print('a)em banheiros, cozinhas, copas, copas-cozinhas, �reas de servi�o, lavanderias e locais an�logos, no\n')
#     print('m�nimo 600 VA por ponto de tomada, at� tr�s pontos, e 100 VA por ponto para os excedentes.')
#     print('Quando o total de tomadas no conjunto desses ambientes for superior a seis pontos,\n')
#     print('admite-se que o crit�rio de atribui��o de pot�ncias seja de no m�nimo 600 VA por ponto de tomada, at� dois pontos, e 100 VA por ponto para os excedentes\n')
#     print('b) nos demais c�modos ou depend�ncias, no m�nimo 100 VA por ponto de tomada.\n') 
