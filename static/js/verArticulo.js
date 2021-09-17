
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
	form.append("carritos",0);

	var Tp = document.getElementById("TotalProductos");
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
				Tp.innerHTML=array_sus
			}
		)
}
