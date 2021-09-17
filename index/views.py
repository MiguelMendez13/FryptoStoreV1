from django.shortcuts import render
from django.template.loader import  get_template as GetHTML
from django.shortcuts import render
import mysql.connector
import random
from django.http import JsonResponse
import hashlib
#from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from web3 import Web3
import web3



# Create your views here.

#0 IDProducto(10)
#1 CodigoProducto varchar(10), 
#2 Nombre varchar(50), 
#3 Precio Integer(5),
#4 Existencias Integer(5),
#5 Departamento varchar(30),
#6 Descripcion Varchar(150),
#7 Marca Varchar(30)

def index(request):

	conexion = mysql.connector.connect(host="localhost",port=3306,user="root",password="",db="fryptotienda1")

	cursor=conexion.cursor()
	cursor.execute("select database();")
	registro=cursor.fetchone()
	cursor.execute("select * from productos where Departamento='Linea_Blanca'")
	resultados=cursor.fetchall()
	ListaLineaBlanca=[]
	ListaLineaRandom=[]
	ListaLineaEnviar=[]
	for fila in resultados:
		ListaLineaBlanca.append([fila[1],fila[2],fila[3]])

	for x in range(5):
		gen = random.choice(ListaLineaBlanca)
		ListaLineaRandom.append(gen)

	i=1
	for item in ListaLineaRandom:
		ListaLineaEnviar.append([item[0],item[1],item[2],i])
		i=i+1

	request.session["Usuario"]=request.session.get('Usuario', "")
	request.session["Npro"] = request.session.get('Npro', 0)
	request.session["Lpro"] = request.session.get('Lpro', [])

	request.session["Subtotal"]=request.session.get('Subtotal', 0)
	request.session["Total"]=request.session.get('Total', 0)
	request.session["Descuento"]=request.session.get('Descuento', 0)
	request.session["Envio"]=request.session.get('Envio', 0)


	parametros={"LLB": ListaLineaEnviar,"Nupro":request.session["Npro"]}


	conexion.close()
	return render(request, "index.html",parametros)




def MostrarArticulo(request,dpto,articulo):
	depto=str(dpto)
	departamento=""
	if(depto=="LB"):
		departamento="Linea_Blanca"
	
	articulol=str(articulo)
	request.session["Npro"] = request.session.get('Npro', 0)
	request.session["Lpro"] = request.session.get('Lpro', [])
	request.session["Usuario"]=request.session.get('Usuario', "")
	request.session["Subtotal"]=request.session.get('Subtotal', 0)
	request.session["Total"]=request.session.get('Total', 0)
	request.session["Descuento"]=request.session.get('Descuento', 0)
	request.session["Envio"]=request.session.get('Envio', 0)

	conexion = mysql.connector.connect(host="localhost",port=3306,user="root",password="",db="fryptotienda1")

	cursor=conexion.cursor()
	cursor.execute("select database();")
	registro=cursor.fetchone()
	cursor.execute("select * from productos where CodigoProducto='"+articulol+"'")
	resultados=cursor.fetchall()
	stringg=[]
	for fila in resultados:
		stringg.append([fila[0],fila[1],fila[2],fila[3],fila[4],fila[5],fila[6],fila[7]])
	
	noProductos = request.session.get('Npro', 0)

	parametros={"stringg":stringg, "dpto":departamento, "Nupro":noProductos}
	conexion.close()

	return render(request, "verArticulo.html",parametros)




def AgregarArticulo(request):
	parametros={}
	if request.is_ajax():
		noProductos = request.session['Npro']=request.session.get('Npro', 0)+1
		noProductoss = request.session['Lpro'].append(str(request.POST["product"]))
		request.session["Usuario"]=request.session.get('Usuario', "")
		subt = request.session["Subtotal"]=request.session.get('Subtotal', 0)
		total= request.session["Total"]=request.session.get('Total', 0)
		desc=request.session["Descuento"]=request.session.get('Descuento', 0)
		envio=request.session["Envio"]=request.session.get('Envio', 0)
		
		sub=0
		tot=0
		desc=0


		conexion = mysql.connector.connect(host="localhost",port=3306,user="root",password="",db="fryptotienda1")
		cursor=conexion.cursor()
		cursor.execute("select database();")
		registro=cursor.fetchone()
		cursor.execute("select * from productos where CodigoProducto='"+str(request.POST["product"])+"'")
		resultados=cursor.fetchall()
		
		for fila in resultados:
			sub=sub+fila[3]
	#		print (sub)
	#		print(fila[3])
	#	print(sub)
		request.session["Subtotal"]=request.session.get('Subtotal', 0)+sub
		#print("subt: "+str(request.session["Subtotal"]))
		request.session["Total"]=request.session["Subtotal"]-request.session["Descuento"]+request.session["Envio"]
		if int(request.POST["carritos"])==1:
			#print("carrito")
			pass
		else:
			#print("no carrito")
			pass

		parametros={"NumProductos":int(request.session.get('Npro', 0),),"ToTaL":int(request.session["Total"])}
		conexion.close()
	return JsonResponse(parametros)




def BorrarArticulo(request):
	parametros={}
	request.session["Npro"] = request.session.get('Npro', 0)
	request.session["Lpro"] = request.session.get('Lpro', [])
	request.session["Usuario"]=request.session.get('Usuario', "")
	request.session["Subtotal"]=request.session.get('Subtotal', 0)
	request.session["Total"]=request.session.get('Total', 0)
	request.session["Descuento"]=request.session.get('Descuento', 0)
	request.session["Envio"]=request.session.get('Envio', 0)
	if request.is_ajax():

		lsProductoss = request.session['Lpro']
		productodel=str(request.POST["product"])
		cant=int(request.POST["cantidad"])
		noProductos = request.session['Npro']=request.session.get('Npro', 0)-cant
		contador=0
		ls2=[]

		conexion = mysql.connector.connect(host="localhost",port=3306,user="root",password="",db="fryptotienda1")
		cursor=conexion.cursor()
		cursor.execute("select database();")
		registro=cursor.fetchone()
		cursor.execute("select * from productos where CodigoProducto='"+str(request.POST["product"])+"'")
		resultados=cursor.fetchall()
		sub=0
		for fila in resultados:
			sub=sub+fila[3]
		request.session["Subtotal"]=request.session.get('Subtotal', 0)-(sub*cant)
		request.session["Total"]=request.session["Total"]-(sub*cant)



		for it in lsProductoss:
			if(it==productodel) & (contador!=cant):
				contador+=1
			else:
				ls2.append(it)

		request.session['Lpro']=ls2
	parametros={"NumProductos":int(request.session.get('Npro', 0),),"ToTaL":request.session["Total"]}
	conexion.close()
	return JsonResponse(parametros)




def Carrito(request):
	lsProductos = request.session.get('Lpro', [])
	datos={}
	productosAgregados={}
	request.session["Subtotal"]=request.session.get('Subtotal', 0)
	request.session["Total"]=request.session.get('Total', 0)
	request.session["Descuento"]=request.session.get('Descuento', 0)
	request.session["Envio"]=request.session.get('Envio', 0)
	request.session["Usuario"]=request.session.get('Usuario', "")
	conexion = mysql.connector.connect(host="localhost",port=3306,user="root",password="",db="fryptotienda1")
	cursor=conexion.cursor()
	cursor.execute("select database();")
	registro=cursor.fetchone()

	for pro in lsProductos:
		contador=0
		for pro2 in lsProductos:
			if pro == pro2:
				contador+=1
			else:
				pass
		productosAgregados[pro]=contador
	
	lol=list(productosAgregados.keys())
#	print ("lol: "+str(lol))
	for info in lol:
		cursor.execute("select * from productos where CodigoProducto='"+info+"'")
		resultados=cursor.fetchall()
		for fila in resultados:
			datos[info]=[fila[0],fila[1],fila[2],fila[3],fila[4],fila[5],fila[6],fila[7]]
#	print(productosAgregados)
#	print(datos)

	
	noProductos = request.session.get('Npro', 0)
	listatemp=datos
	listfinal=[]
	cont=0
	for proo in productosAgregados:
		listatemp[proo].append(productosAgregados[proo])
		listfinal.append(listatemp[proo])
		cont+=1
	#print(listfinal)
	parametros={"Nupro":noProductos,"Lsfinal":listfinal,"SBT": request.session["Subtotal"]}
	conexion.close()
	return render(request, "carrito.html",parametros)
	



def perfilver(request):
	request.session["Npro"] = request.session.get('Npro', 0)
	request.session["Lpro"] = request.session.get('Lpro', [])
	request.session["Usuario"]=request.session.get('Usuario', "")
	request.session["Subtotal"]=request.session.get('Subtotal', 0)
	request.session["Total"]=request.session.get('Total', 0)
	request.session["Descuento"]=request.session.get('Descuento', 0)
	request.session["Envio"]=request.session.get('Envio', 0)
	pagina=""
	error=""
	if("usuarioEntrar" in dict(request.POST)):
		usuario=request.POST["usuarioEntrar"]
		pswrd=request.POST["pswrd"]
		passcode=str(hashlib.sha512(pswrd.encode("utf-8")).hexdigest())
		conexion = mysql.connector.connect(host="localhost",port=3306,user="root",password="",db="fryptotienda1")
		cursor=conexion.cursor()
		cursor.execute("select database();")
		registro=cursor.fetchone()
		try:
			
			cursor.execute("select * from usuarios where correo='%s'"%(str(usuario)))
			resultados=cursor.fetchone()
			if(resultados==None):
				error="Error en usuario o contraseña."
			else:
				if (resultados[7]==passcode):
					print("Si usuario y contraseña")
					request.session["Usuario"]=request.POST["usuarioEntrar"]
				else:
					error="Error en usuario o contraseña."
		except Exception as e:
			error="Error en usuario o contraseña."
		conexion.close()


	else:
		pass
	if(request.session["Usuario"]!="" and "Usuario" in dict(request.session)):
		pagina="perfil.html"
	else:
		pagina="ingresarPerfil.html"
	parametros={"Nupro":request.session["Npro"],"error":error}
	return render(request, pagina,parametros)



def Registrar(request):
	request.session["Npro"] = request.session.get('Npro', 0)
	request.session["Lpro"] = request.session.get('Lpro', [])
	request.session["Usuario"]=request.session.get('Usuario', "")
	request.session["Subtotal"]=request.session.get('Subtotal', 0)
	request.session["Total"]=request.session.get('Total', 0)
	request.session["Descuento"]=request.session.get('Descuento', 0)
	request.session["Envio"]=request.session.get('Envio', 0)
	parametros={"Nupro":request.session["Npro"]}
	
	return render(request, "registrar.html",parametros)



def RegistrarUsuario(request):
	pag=""
	parametros={}
	error=""
	completo=0
	permitidonom="ABCDEFGHIJKLMNÑOPQRSTUVXYZ ".lower()
	permitidoape="ABCDEFGHIJKLMNÑOPQRSTUVXYZ".lower()
	codigo=list("ABCDEFGHIJKLMNÑOPQRSTUVXYZ0123456789".lower())
	permitidomail="ABCDEFGHIJKLMNÑOPQRSTUVXYZ0123456789.@".lower()
	permitidopass="ABCDEFGHIJKLMNÑOPQRSTUVXYZ0123456789.@!$%&/()?*-+ ".lower()+"ABCDEFGHIJKLMNÑOPQRSTUVXYZ"
	if request.is_ajax():
		request.session["Npro"] = request.session.get('Npro', 0)
		request.session["Lpro"] = request.session.get('Lpro', [])
		request.session["Usuario"]=request.session.get('Usuario', "")
		request.session["Subtotal"]=request.session.get('Subtotal', 0)
		request.session["Total"]=request.session.get('Total', 0)
		request.session["Descuento"]=request.session.get('Descuento', 0)
		request.session["Envio"]=request.session.get('Envio', 0)

		nombre=str(request.POST["nombre"]).lower()
		apaterno=str(request.POST["apaterno"]).lower()
		amaterno=str(request.POST["amaterno"]).lower()
		numero=str(request.POST["numero"]).lower()
		mail=str(request.POST["mail"]).lower()
		password=str(request.POST["password"])
		correocomprobar=0
		if(nombre=="" or apaterno=="" or amaterno=="" or numero=="" or mail=="" or password==""):
			error=error+"LLena todos los campos"
		else:
			
			for nom in nombre: 
				if(nom in permitidonom):
					pass
				else:
					error=error+"Error en tu nombre, recuerda solo usar letras y espacio;\n"
					break
			for nom in apaterno: 
				if(nom in permitidoape):
					pass
				else:
					error=error+"Error en tu apellido paterno, recuerda solo usar letras;\n"
					break
			for nom in amaterno: 
				if(nom in permitidoape):
					pass
				else:
					error=error+"Error en tu apellido materno, recuerda solo usar letras;\n"
					break
			for nom in mail: 
				if(nom in permitidomail):
					pass
				else:
					correocomprobar+=1
					break
			
			if("@"in mail):
				pass
			else:
				correocomprobar+=1
			if("."in mail):
				pass
			else:
				correocomprobar+=1
			if(correocomprobar !=0):
				error=error+"Error en el formato de tu correo;\n"

			for nom in password: 
				if(nom in permitidopass):
					pass
				else:
					error=error+"Error en el formato de tu contraseña solo se permite\nestos caracteres especiales: .@!$%&/()?*-+ y espacio;\n"
					break
			
			if(len(nombre)>30):
				error=error+"El nombre no debe de tener mas de 30 caracteres;\n"
			if(len(apaterno)>15):
				error=error+"El apellido no debe de tener mas de 15 caracteres;\n"
			if(len(apaterno)>15):
				error=error+"El apellido no debe de tener mas de 15 caracteres;\n"
			if(len(numero)>14):
				error=error+"El numero no debe de tener mas de 14 caracteres;\n"
			if(len(password)>10):
				error=error+"El password no debe de tener mas de 10 caracteres;\n"
			if(len(mail)>40):
				error=error+"El correo no debe de tener mas de 40 caracteres;\n"

		
		if(error==""):
			conexion = mysql.connector.connect(host="localhost",port=3306,user="root",password="",db="fryptotienda1")

			cursor=conexion.cursor()
			cursor.execute("select database();")
			registro=cursor.fetchone()


			genco=""
			for x in range(15):
				genco=genco+random.choice(codigo)
			passcode=str(hashlib.sha512(password.encode("utf-8")).hexdigest())
			codeveri=str(hashlib.sha512(genco.encode("utf-8")).hexdigest())
			
			sqlin=str("insert into usuariosnuevos values('%s','%s','%s',%i,'%s','%s','%s','%s')"%(codeveri,genco,mail,int(numero),nombre,apaterno,amaterno,passcode))
			cursor.execute(sqlin)
			conexion.commit()
			conexion.close()

			error="Registrado porfavor verifica tu correo electronico para ingresar a tu perfil y continuar comprando"
			parametros["completo"]=0
			templatecorreo=open("index/template.html")
			templatecorre = templatecorreo.read()
			templatecorreo.close()
			paginaenv="http://127.0.0.1:8000/verificarcorreo/"+codeveri


			subject, from_email, to = 'prueba',"frikypruebascorreo@gmail.com",'dnmiguel.friky@gmail.com'
			text_content = 'This is an important message.'
			html_content=render_to_string('template.html', {'urlverif':paginaenv})

			msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			#msg.attach_file("index/logo1.2_4k.png")
			msg.send()

		else:
			completo=1
			
		parametros["error"]=error
		parametros["completo"]=completo
			
	else:
		pass
	return JsonResponse(parametros)


def Wallet(request):
	
	request.session["Usuario"]=request.session.get('Usuario', "")
	request.session["Npro"] = request.session.get('Npro', 0)
	request.session["Lpro"] = request.session.get('Lpro', [])

	request.session["Subtotal"]=request.session.get('Subtotal', 0)
	request.session["Total"]=request.session.get('Total', 0)
	request.session["Descuento"]=request.session.get('Descuento', 0)
	request.session["Envio"]=request.session.get('Envio', 0)
	parametros={}

	if(request.session["Usuario"]!="" and "Usuario" in dict(request.session)):
		parametros["User"]="Loggueado "+str(request.session["Usuario"])
	else:
		parametros["User"]="No Loggueado"

	return render(request, "wallet.html",parametros)





def verificarCorreo(request,usuario):
	conexion = mysql.connector.connect(host="localhost",port=3306,user="root",password="",db="fryptotienda1")
	cursor=conexion.cursor()
	cursor.execute("select database();")
	registro=cursor.fetchone()
	cursor.execute("select * from usuariosnuevos where IdUsuario='%s'"%(str(usuario)))
	resultados=cursor.fetchone()
	print(resultados)
	sqlin=str("insert into usuarios values(%i,'%s','%s',%i,'%s','%s','%s','%s')"%(0,resultados[1],resultados[2],resultados[3],resultados[4],resultados[5],resultados[6],resultados[7]))
	cursor.execute(sqlin)
	conexion.commit()
	sqlin=str("delete from usuariosnuevos where IdUsuario='%s'"%(str(usuario)))
	cursor.execute(sqlin)
	conexion.commit()



	cursor.execute("select * from productos where Departamento='Linea_Blanca'")
	resultados=cursor.fetchall()
	ListaLineaBlanca=[]
	ListaLineaRandom=[]
	ListaLineaEnviar=[]
	for fila in resultados:
		ListaLineaBlanca.append([fila[1],fila[2],fila[3]])

	for x in range(5):
		gen = random.choice(ListaLineaBlanca)
		ListaLineaRandom.append(gen)

	i=1
	for item in ListaLineaRandom:
		ListaLineaEnviar.append([item[0],item[1],item[2],i])
		i=i+1

	request.session["Usuario"]=request.session.get('Usuario', "")
	request.session["Npro"] = request.session.get('Npro', 0)
	request.session["Lpro"] = request.session.get('Lpro', [])

	request.session["Subtotal"]=request.session.get('Subtotal', 0)
	request.session["Total"]=request.session.get('Total', 0)
	request.session["Descuento"]=request.session.get('Descuento', 0)
	request.session["Envio"]=request.session.get('Envio', 0)


	parametros={"LLB": ListaLineaEnviar,"Nupro":request.session["Npro"]}


	conexion.close()
	return render(request, "index.html",parametros)




def delall(request):

	conexion = mysql.connector.connect(host="localhost",port=3306,user="root",password="",db="fryptotienda1")

	cursor=conexion.cursor()
	cursor.execute("select database();")
	registro=cursor.fetchone()
	cursor.execute("select * from productos where Departamento='Linea_Blanca'")
	resultados=cursor.fetchall()
	ListaLineaBlanca=[]
	ListaLineaRandom=[]
	ListaLineaEnviar=[]
	for fila in resultados:
		ListaLineaBlanca.append([fila[1],fila[2],fila[3]])

	for x in range(5):
		gen = random.choice(ListaLineaBlanca)
		ListaLineaRandom.append(gen)

	i=1
	for item in ListaLineaRandom:
		ListaLineaEnviar.append([item[0],item[1],item[2],i])
		i=i+1
	noProductos = request.session['Npro']=0
	request.session['Lpro']=[]
	request.session["Subtotal"]=0
	request.session["Total"]=0
	request.session["Descuento"]=0
	request.session["Envio"]=0
	request.session["Usuario"]=""
	parametros={"LLB": ListaLineaEnviar,"Nupro":noProductos}

#	print(request.session['Npro'])
#	print(request.session['Lpro'])

	conexion.close()
	return render(request, "index.html",parametros)
