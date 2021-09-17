function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}


function Addd (producto){
	var form = new FormData();
	form.append("product",producto);
	form.append("carritos",1);
	var Tp = document.getElementById("TotalProductos");
	var Inputt=document.getElementById("Input"+producto);
	var Totalll=document.getElementById("Totall");
	urlop="/Agregar/"
	fetch(urlop,{
			method: "POST",
			body: form,
			headers: {
				"X-CSRFToken": getCookie('csrftoken'),
				"X-Requested-With": "XMLHttpRequest"
			}
	}).then(
			function(response){
				return response.json();
			}
		).then(
			function (data){

				array_sus = data.NumProductos;
				Tp.innerHTML=array_sus;
				Inputt.value=parseInt(Inputt.value,10)+1;
				tot=parseInt(data.ToTaL);
				Totalll.innerHTML="Total: "+tot;
			}
		)
}


function Dell (producto,cantidad){
	var form = new FormData();
	form.append("product",producto);
	var Inputt=document.getElementById("Input"+producto);
	var Totalll=document.getElementById("Totall");
	var cantt=0;
	if (cantidad==1){
		cantt=1;
	}
	else if(cantidad==2){
		cantt=parseInt(Inputt.value,10);
	}
	if(cantt==parseInt(Inputt.value,10)){
		var confirmar = confirm("¿Estas seguro de eliminar este articulo?");
		if(confirmar==true){
			form.append("cantidad",cantt);
			var Tp = document.getElementById("TotalProductos");

			urlop="/delart/"
			fetch(urlop,{
					method: "POST",
					body: form,
					headers: {
						"X-CSRFToken": getCookie('csrftoken'),
						"X-Requested-With": "XMLHttpRequest"
					}
			}).then(
					function(response){
						return response.json();
					}
				).then(
					function (data){
						array_sus = data.NumProductos;
						Tp.innerHTML=array_sus;
						Inputt.value=parseInt(Inputt.value,10)-cantt;
						if(Inputt.value==0){
							Inputt.parentNode.parentNode.remove()
						}
						tot=parseInt(data.ToTaL);
						Totalll.innerHTML="Total: "+tot;
					}
				)
		}
	}
	else{
		form.append("cantidad",cantt);
			var Tp = document.getElementById("TotalProductos");

			urlop="/delart/"
			fetch(urlop,{
					method: "POST",
					body: form,
					headers: {
						"X-CSRFToken": getCookie('csrftoken'),
						"X-Requested-With": "XMLHttpRequest"
					}
			}).then(
					function(response){
						return response.json();
					}
				).then(
					function (data){
						array_sus = data.NumProductos;
						Tp.innerHTML=array_sus;
						Inputt.value=parseInt(Inputt.value,10)-cantt;
						if(Inputt.value==0){
							Inputt.parentNode.parentNode.remove()
						}
						tot=parseInt(data.ToTaL);
						Totalll.innerHTML="Total: "+tot;

					}
				)
	}
}