let log = (toLog) => console.log(toLog)
let byId = (id) => document.getElementById(id)


function check_confirm(element) {
	log(byId("password").value)
	log(byId("password_confirm").value);
	if (byId("password").value == "" && byId("password_confirm").value != "") {
		log("Password empty");
		!byId("password").classList.contains("red") ? byId("password").classList.toggle("red") : '';
	} else {
		byId("password").classList.contains("red") ? byId("password").classList.toggle("red") : '';
	}

	if (byId("password").value != byId("password_confirm").value) {
		log("mismatch");
		!byId("password_confirm").classList.contains("red") ? byId("password_confirm").classList.toggle("red") : '';
	} else {
		log("match")
		byId("password_confirm").classList.contains("red") ? byId("password_confirm").classList.toggle("red") : '';
	}
	log(byId("password"))
}






// window.addEventListener('on_load', function () {alert('hello!');	}, false);


// window.addEventListener('popstate', (event) => {
// 	console.log(`location: ${document.location}, state: ${JSON.stringify(event.state)}`);
// });
// history.pushState({ page: 1 }, "title 1", "?page=1");
// history.pushState({ page: 2 }, "title 2", "");
// history.replaceState({}, null, location.href)
// history.replaceState({ page: 'Index' }, "title 3", "/dasboard");
// history.back(); // Logs "location: http://example.com/example.html?page=1, state: {"page":1}"
// history.back(); // Logs "location: http://example.com/example.html, state: null"
// history.go(2);  // Logs "location: http://example.com/example.html?page=3, state: {"page":3}"


// function clearSessionHistory() {
// 	history.replaceState({}, null, location.href);
// }



// logoutBtn.addEventListener('click', function () {
// 	clearSessionHistory();
// 	// Your other logout code here
// });






