#CodigoProducto varchar(10), Nombre varchar(50), Precio Integer(5), Existencias Integer(5), Departamento varchar(30), Descripcion Varchar(150), Marca Varchar(30)
import random
import shutil


caracteres = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9"]
caracteres2 = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9"," "]
licuadoraImagen=["Refrigerador1.jpg","Refrigerador2.jpg","Refrigerador3.jpg","Refrigerador4.jpg","Refrigerador5.jpg","Refrigerador6.jpg","Refrigerador7.jpg","Refrigerador8.jpg"]






Descripcion="Este refrigerador de la marca %s cuenta con %s cajones, fabricada en %s además de contar con %s temperaturas diferentes incluyendo un botón extra para descongelar en tan solo %s minutos, Contiene una potencia de %s watts, con un peso de %s kg y fabricación exterior de %s."
marcas=["Mabe","Oster","RCA","LG","Hisense"]
materiales=["Platico","Aluminio","Metal"]


archivo=open("Lista de Registros Refrigeradores.txt","w")


def genfun(marcaE):
	motores=str(random.randint(2,9))
	anio=str(random.randint(2014,2021))
	veloc=str(random.randint(3,9))
	seg=str(random.randint(9,50))
	wats=str(random.randint(200,350))
	peso="{0:.2f}".format(random.randint(10,30)+random.random())
	mat=str(random.choice(materiales))

	texto=Descripcion%(marcaE,motores,anio,veloc,seg,wats,peso,mat)
	return(texto)





for x2 in range(30,60):
	codigo=""
	Nombre="Refrigerador "
	Precio=0
	Existencia=0
	Nombre=""
	departamento="Linea_Blanca"
	SQLSentencia = "insert into productos values(%s,'%s','%s',%s,%s,'%s','%s','%s');\n"


	marca=random.choice(marcas)

	for x in range(10):
		caracter=random.choice(caracteres)
		codigo=codigo+caracter
	#print (codigo)

	Nombre=Nombre+marca+" mod: "
	for x in range(5):
		caracter=random.choice(caracteres)
		Nombre=Nombre+caracter
	#print (Nombre)


	Precio=random.randint(999,2100)
	#print (Precio)


	Existencias =random.randint(100,200)
	#print(Existencias)


	Desc2=genfun(marca)
	#print(Desc2)

	imagensel=random.choice(licuadoraImagen)

	copiarimagen=shutil.copy("RefrigeradoresPlantilla/"+imagensel, codigo+".jpg")




	SQLSentencia=SQLSentencia%(str(x2),codigo,Nombre,Precio,Existencias,departamento,Desc2,marca)
	print(SQLSentencia)
	archivo.write(SQLSentencia)


archivo.close()