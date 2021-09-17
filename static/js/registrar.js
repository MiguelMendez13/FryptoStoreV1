
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

function agregar() {
	var formulario= document.getElementById("formulario");
	var form = new FormData(formulario);
	document.getElementById("boton").disabled = true;
	
	urlop="/RegistrarUsuario/"
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

				
				alert(data.error);

				document.getElementById("boton").disabled = false;
				if(data.completo==0){
					location.href="http://127.0.0.1:8000/perfil/";
				}
			}
		)
	
}