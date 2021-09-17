#ID int primary key, CodigoProducto varchar(10), Nombre varchar(50), Precio Integer(5), Existencias Integer(5), Departamento varchar(30), Descripcion Varchar(150), Marca Varchar(30)
import random
import shutil


caracteres = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9"]
caracteres2 = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9"," "]
licuadoraImagen=["1.jpg","2.jpg","3.jpg"]
estados=["Aguascalientes","Coahuila","Chiapas","Chihuahua","Puebla","Hidalgo"]





Descripcion="Carne de nuestros mejores provedores del estado de %s, con una calidad de %s estrellas de %s kg"
marcas=["Bisteck de Puerco","Res","Chuleta","Ribeye","Bisteck de Res"]



archivo=open("lista de Registros Carne.txt","w")


def genfun(marcaE):
	est=random.choice(estados)
	estrellas=str(random.randint(7,10))
	kilos=random.randint(0,3)
	gramos=random.random()
	kg=kilos+gramos
	kilgramo="%.2f"%kg
	texto=Descripcion%(est,estrellas,kilgramo)
	return(texto)





for x2 in range(60,75):
	codigo=""
	Nombre="Carne "
	Precio=0
	Existencia=0
	Nombre=""
	departamento="Super"
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


	Precio=random.randint(60,190)
	#print (Precio)


	Existencias =random.randint(100,200)
	#print(Existencias)


	Desc2=genfun(marca)
	#print(Desc2)

	imagensel=random.choice(licuadoraImagen)

	copiarimagen=shutil.copy("Plantillas/carne/"+imagensel, codigo+".jpg")




	SQLSentencia=SQLSentencia%(str(x2),codigo,Nombre,Precio,Existencias,departamento,Desc2,marca)
	print(SQLSentencia)
	archivo.write(SQLSentencia)


archivo.close()