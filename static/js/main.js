function copyurl() {
	let shorturl = document.getElementById('shorturl')
	let copy = document.getElementById('copy')
	let copy_check = document.getElementById('copy-check')
	shorturl.select()
	document.execCommand('Copy')
	document.getSelection().removeAllRanges()
	copy.style.display = 'none'
	copy_check.style.display = 'block'
	setTimeout(() => {
		copy.style.display = 'block'
		copy_check.style.display = 'none'
	}, 1500)
}

function copybyindex(index) {
	var copy = document.getElementById('copybtn' + index)
	var copy_check = document.getElementById('check-copybtn' + index)
	var text = document.getElementById('shorturl' + index).getAttribute('href')
	var textArea = document.createElement("textarea");
	textArea.value = text;
	textArea.style.top = "0";
	textArea.style.left = "0";
	textArea.style.position = "fixed";
	document.body.appendChild(textArea);
	textArea.focus();
	textArea.select();
	document.execCommand('copy');
	document.body.removeChild(textArea);
	copy.style.display = 'none'
	copy_check.style.display = 'block'
	setTimeout(() => {
		copy.style.display = 'block'
		copy_check.style.display = 'none'
	}, 2000)
}

function clearurlform() {
	let longurl = document.getElementById('longurl')
	let name = document.getElementById('name')
	longurl.value = ''
	name.value = ''
}

function showshorturlform() {
	clearurlform()
	clearalert()
	let copyform = document.getElementById('form-checkurl')
	let shortform = document.getElementById('form-shorturl')
	copyform.style.display = 'none'
	shortform.style.display = 'block'
}

function showiptracker() {
	clearalert()
	document.getElementById('ip').value = ''
	let copyform = document.getElementById('ipresult')
	let shortform = document.getElementById('ipinput')
	copyform.style.display = 'none'
	shortform.style.display = 'block'
}

function showcopyurlform(shortenurl) {
	let urlfield = document.getElementById('shorturl')
	urlfield.value = shortenurl
	let copyform = document.getElementById('form-checkurl')
	let shortform = document.getElementById('form-shorturl')
	copyform.style.display = 'block'
	shortform.style.display = 'none'
}

function shorturl() {
	var longurl = document.getElementById('longurl').value
	if (longurl == '') {
		return
	}
	var submitbtn = document.getElementById('submitbtn')
	submitbtn.setAttribute('disabled', 'true')
	var name = document.getElementById('name').value
	var host = window.location.protocol + "//" + window.location.host;
	var url = host + "/api/AddPublicUrl";
	var xhr = new XMLHttpRequest();
	xhr.open("POST", url);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4) {
			var status = xhr.status
			var text = JSON.parse(xhr.responseText)
			if (status == 200) {
				if (text['success'] == true) {
					submitbtn.removeAttribute('disabled')
					showalert(text['message'], text['category'])
					showcopyurlform(text['shorturl'])
				} else {
					submitbtn.removeAttribute('disabled')
					showalert(text['message'], text['category'])
				}
			} else {
				submitbtn.removeAttribute('disabled')
				showalert('Something went wrong! Please try again later')
			}
		}
	};
	var data = `longurl=${encodeURIComponent(longurl)}&name=${encodeURIComponent(name)}`;
	xhr.send(data);
}

function showalert(message, category, id = 'alertmsg') {
	var alertmsg = document.getElementById(id)
	if (category == 'success') {
		alertmsg.innerHTML = `<div class="alert alert-success fade show alert-dismissible d-flex align-items-center" role="alert">
          <svg aria-label="Success:" class="bi flex-shrink-0 me-2" height="24" role="img" width="24">
            <use xlink:href="#check-circle-fill">
            </use>
          </svg>
          <div>
            ${message}
            <button aria-label="Close" class="btn-close" data-bs-dismiss="alert" type="button">
            </button>
          </div>
        </div>`
	} else if (category == 'warning') {
		alertmsg.innerHTML = `<div class="alert alert-warning fade show alert-dismissible d-flex align-items-center" role="alert">
          <svg aria-label="Warning:" class="bi flex-shrink-0 me-2" height="24" role="img" width="24">
            <use xlink:href="#exclamation-triangle-fill">
            </use>
          </svg>
          <div>
            ${message}
            <button aria-label="Close" class="btn-close" data-bs-dismiss="alert" type="button">
            </button>
          </div>
        </div>`
	} else if (category == 'error') {
		alertmsg.innerHTML = `<div class="alert alert-danger fade show alert-dismissible d-flex align-items-center" role="alert">
          <svg aria-label="Danger:" class="bi flex-shrink-0 me-2" height="24" role="img" width="24">
            <use xlink:href="#exclamation-triangle-fill">
            </use>
          </svg>
          <div>
            ${message}
            <button aria-label="Close" class="btn-close" data-bs-dismiss="alert" type="button">
            </button>
          </div>
        </div>`
	}
}

function clearalert(id = 'alertmsg') {
	var alertmsg = document.getElementById(id)
	alertmsg.innerHTML = ''
}

function registeruser() {
	var username = document.getElementById('username').value
	var email = document.getElementById('email').value
	var password = document.getElementById('password').value
	var confirm_password = document.getElementById('confirm-password').value
	if (username == '') {
		return
	} else if (email == '') {
		return
	} else if (password == '') {
		return
	} else if (confirm_password == '') {
		return
	}
	var submitbtn = document.getElementById('submitbtn')
	submitbtn.setAttribute('disabled', 'true')
	var host = window.location.protocol + "//" + window.location.host;
	var url = host + "/api/register";
	var xhr = new XMLHttpRequest();
	xhr.open("POST", url);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4) {
			var status = xhr.status
			var text = JSON.parse(xhr.responseText)
			if (status == 200) {
				if (text['success'] == true) {
					submitbtn.removeAttribute('disabled')
					showalert(text['message'], text['category'])
					setTimeout(() => {
						window.location.href = host + '/login'
					}, 1000)
				} else {
					submitbtn.removeAttribute('disabled')
					showalert(text['message'], text['category'])
				}
			} else {
				submitbtn.removeAttribute('disabled')
				showalert('Something went wrong! Please try again later')
			}
		}
	};
	var data = `username=${encodeURIComponent(username)}&email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}&confirm-password=${encodeURIComponent(confirm_password)}`;
	xhr.send(data);
}

function loginuser() {
	var username = document.getElementById('username').value
	var password = document.getElementById('password').value
	var checked = document.getElementById('remember').checked
	if (username == '') {
		return
	} else if (password == '') {
		return
	}
	var submitbtn = document.getElementById('submitbtn')
	submitbtn.setAttribute('disabled', 'true')
	var host = window.location.protocol + "//" + window.location.host;
	var url = host + "/api/login";
	var xhr = new XMLHttpRequest();
	xhr.open("POST", url);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4) {
			var status = xhr.status
			var text = JSON.parse(xhr.responseText)
			if (status == 200) {
				if (text['success'] == true) {
					submitbtn.removeAttribute('disabled')
					showalert(text['message'], text['category'])
					setTimeout(() => {
						window.location.href = host + '/dashboard'
					}, 1000)
				} else {
					submitbtn.removeAttribute('disabled')
					showalert(text['message'], text['category'])
				}
			} else {
				submitbtn.removeAttribute('disabled')
				showalert('Something went wrong! Please try again later')
			}
		}
	};
	var data = `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&checked=${encodeURIComponent(checked)}`;
	xhr.send(data);
}

function deleteurl(url_id, index) {
	var submitbtn = document.getElementById('deletebtn' + index)
	submitbtn.setAttribute('disabled', 'true')
	var host = window.location.protocol + "//" + window.location.host;
	var url = host + "/api/deleteurl";
	var xhr = new XMLHttpRequest();
	xhr.open("POST", url);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4) {
			var status = xhr.status
			var text = JSON.parse(xhr.responseText)
			if (status == 200) {
				if (text['success'] == true) {
					submitbtn.removeAttribute('disabled')
					showalert(text['message'], text['category'], 'deletealert' + index)
					setTimeout(() => {
						document.getElementById('closebtn' + index).click()
						document.getElementById('urlcard' + index).remove()
					}, 1000)
				} else {
					submitbtn.removeAttribute('disabled')
					showalert(text['message'], text['category'], 'deletealert' + index)
				}
			} else {
				submitbtn.removeAttribute('disabled')
				showalert('Something went wrong! Please try again later', text['category'], 'deletealert' + index)
			}
		}
	};
	var data = `id=${url_id}`;
	xhr.send(data);
}

function editurl(url_id, index) {
	var longurl = document.getElementById('longurl' + index).value
	var name = document.getElementById('name' + index).value
	if (longurl == '') {
		return
	}
	if (name == '') {
		return
	}
	var submitbtn = document.getElementById('savebtn' + index)
	submitbtn.setAttribute('disabled', 'true')
	var host = window.location.protocol + "//" + window.location.host;
	var url = host + "/api/editurl";
	var xhr = new XMLHttpRequest();
	xhr.open("POST", url);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4) {
			var status = xhr.status
			var text = JSON.parse(xhr.responseText)
			if (status == 200) {
				if (text['success'] == true) {
					new_url = host + '/' + name
					submitbtn.removeAttribute('disabled')
					showalert(text['message'], text['category'], 'editalert' + index)
					setTimeout(() => {
						document.getElementById('urlclosebtn' + index).click();
						document.getElementById('shorturl' + index).setAttribute('href', new_url)
						document.getElementById('shorturl' + index).innerText = new_url
						document.getElementById('alongurl' + index).setAttribute('href', longurl)
						document.getElementById('alongurl' + index).innerText = longurl.substring(0, 25) + '...'
					}, 1000)
				} else {
					submitbtn.removeAttribute('disabled')
					showalert(text['message'], text['category'], 'editalert' + index)
				}
			} else {
				submitbtn.removeAttribute('disabled')
				showalert('Something went wrong! Please try again later', text['category'], 'editalert' + index)
			}
		}
	};
	var data = `id=${url_id}&longurl=${encodeURIComponent(longurl)}&name=${encodeURIComponent(name)}`;
	xhr.send(data);
}

function trackip() {
	var ipaddress = document.getElementById('ip').value
	items = ['country', 'countryCode', 'region', 'regionName', 'city', 'zip', 'lat', 'lon', 'timezone', 'isp']
	if (ipaddress == '') {
		return
	}
	var host = window.location.protocol + "//" + window.location.host;
	try {
		var submitbtn = document.getElementById('submitbtn')
		submitbtn.setAttribute('disabled', 'true')
		var url = host+'/api/checkip?ip=' + ipaddress
		var xhr = new XMLHttpRequest();
		xhr.open("POST", url);
		xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
		xhr.onreadystatechange = function() {
			if (xhr.readyState === 4) {
				var status = xhr.status
				var text = JSON.parse(xhr.responseText)
				if (status == 200) {
					if (text['status'] == 'success') {
						for (var i = 0; i < items.length; i++) {
							document.getElementById(items[i]).innerText = text[items[i]]
						}
						submitbtn.removeAttribute('disabled')
						let copyform = document.getElementById('ipresult')
						let shortform = document.getElementById('ipinput')
						copyform.style.display = 'block'
						shortform.style.display = 'none'
					} else {
						submitbtn.removeAttribute('disabled')
						showalert(text['message'], 'error')
					}
				} else {
					submitbtn.removeAttribute('disabled')
					showalert('Something went wrong! Please try again later', 'error')
				}
			}
		};
		var data = ``;
		xhr.send(data);
	} catch {
		submitbtn.removeAttribute('disabled')
		showalert('Something went wrong! Please try again later', 'error')
	}
}

function getipinfo(ipaddress){
	`http://localhost/iptracker?ip=103.173.175.9&submit=true`
	var host = window.location.protocol + "//" + window.location.host;
	url=`${host}/iptracker?ip=${ipaddress}&submit=true`
	window.location.href=url
}

