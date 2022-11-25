var form = document.querySelector("#form")

var u_name = document.querySelector("#u_name")
var mate_name = document.querySelector("#mate_name")

var surname = document.querySelector("#surname")
var mate_surname = document.querySelector("#mate_surname")

var email = document.querySelector("#email")
var is_swimmer = document.querySelector("#is_swimmer")


form.onsubmit = () => {

    if (!is_swimmer.checked) {
        alert("You must be a swimmer")
        return false
    }
////
//    tester = /^[_A-zA-Z]*((-|\s)*[_A-zA-Z])*$/
//    email_tester = /^\S+@\S+\.\S+$/
//
//    n = name.value
//    mate_n = mate_name.value
//
//    s = surname.value
//    mate_s = mate_surname.value
//
//    e = email.value
//
//    console.log(n)
//    console.log(s)
//    console.log(e)
//    console.log(mate_n)
//    console.log(mate_s)
//
//    if (n.length < 2 || n.length > 20) {
//        alert("name length must be in range <2; 20>");
//        return false
//    }
//
//    if (!tester.test(n))  {
//        alert("In name only allowed alphabetic char");
//        return false
//    }
//
//    if (s.length < 2 || s.length > 20) {
//        alert("surname length must be in range <2; 20>");
//        return false
//    }
//
//    if (!tester.test(s))  {
//        alert("In surname only allowed alphabetic char");
//        return false
//    }
//
//    if (mate_n && !tester.test(mate_n)) {
//        alert("In mate name only allowed alphabetic char");
//        return false
//    }
//
//    if (mate_n && mate_n.length < 2 || mate_n.length > 20) {
//        alert("mate name length must be in range <2; 20>");
//        return false
//    }
//
//    if (mate_s && !tester.test(mate_s)) {
//        alert("In mate surname only allowed alphabetic char");
//        return false
//    }
//
//    if (mate_s && mate_s.length < 2 || mate_s.length > 20) {
//        alert("mate surname length must be in range <2; 20>");
//        return false
//    }
//
//    if (!email_tester.test(e)) {
//        alert("Invalid email")
//        return false
//    }
//
//    if (!check_user(n, s)) {
//        alert("user already exist")
//        return false
//    }
//
//    if (mate_s && mate_n && !check_user(mate_n, mate_s)) {
//        alert("user already exist")
//        return false
//    }


    sendMessage()
    return false
}


function sendMessage() {

    json = {
        surname: surname.value,
        email: email.value,
        mate_name: mate_name.value,
        mate_surname: mate_surname.value,
        is_swimmer: is_swimmer.checked,
        name: u_name.value
    }

    console.log({json})
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {

        if ( this.readyState == 4 && this.status == 200 ) {
            alert(this.responseText)
        }

    }
    req.open('POST', "/api/user/create")
    req.setRequestHeader('Content-type', 'application/json; charset=UTF-8', false)
    req.send(JSON.stringify(json))
}

function check_user(name, surname) {
    var result;
    var req = new XMLHttpRequest()
    req.onreadystatechange = function () {

        if ( this.readyState == 4 && this.status == 200 ) {
            result = JSON.parse(this.responseText)
        }
    }
    req.open('GET', "/api/user/check/" + name + "/" + surname + "", false)
    req.send()

    return result
}
