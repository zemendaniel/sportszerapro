function togglePasswordVisibility(id, element) {
    const passwordField = document.getElementById(id);
    const isPasswordVisible = passwordField.type === 'text';
    passwordField.type = isPasswordVisible ? 'password' : 'text';

    const icon = element.querySelector('i');
    icon.className = isPasswordVisible ? 'fa fa-eye' : 'fa fa-eye-slash';
}

window.onscroll = function() {
    let scrollTop = window.scrollY || document.documentElement.scrollTop;
    const btn = document.getElementById('scrollToTopButton');
    if (!btn) {return;}

    if (scrollTop === 0) {
        // User is at the top
        btn.style.display = "none";
    } else if (scrollTop < lastScrollTop) {
        // User is scrolling up
        btn.style.display = "block";
    } else {
        // User is scrolling down
        btn.style.display = "none";
    }
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // For Mobile or negative scrolling
};
function backToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
function getUrlParams() {
    const params = new URLSearchParams(window.location.search);
    const entries = params.entries();
    const paramsObject = {};
    for(const [key, value] of entries) {
        paramsObject[key] = value;
    }
    return paramsObject;
}
// Function to populate form fields based on URL parameters
function populateForm(params) {
    for(const key in params) {
        const input = document.querySelector(`#${key}`);
        if(input) {
            if(input.type === 'checkbox') {
                input.checked = (params[key].toLowerCase() === 'on');
            } else {
                input.value = params[key];
            }
        }
    }
}
document.addEventListener('DOMContentLoaded', (event) => {
    const params = getUrlParams();
    populateForm(params);
    lastScrollTop = window.scrollY || document.documentElement.scrollTop;
    amount = 0;
});

function validatePassword() {
    const password = document.getElementById('password').value;
    const passwordAgain = document.getElementById('password_again').value;
    const messageElement = document.getElementById('passwordMatchMessage');
    const submit = document.getElementById('submit');

     if (!passwordAgain) {
        messageElement.textContent = "";
        submit.disabled = true;
    }
    else if (password === passwordAgain) {
        messageElement.textContent = "A jelszavak egyeznek.";
        messageElement.className = "text-success";
        submit.disabled = false;
    } else {
        messageElement.textContent = "A jelszavak nem egyeznek.";
        messageElement.className = "text-danger";
        submit.disabled = true;
    }
}

idNum = 0;
function createFlashMessage(msg, category){
    let subMessage = "";
    if (msg.includes("|")) {
        const tmp = msg.split("|")
        msg = tmp[0];
        subMessage = tmp[1];
    }

    let className = "alert-dark";
    if (category === "info"){
        className = "alert-dark"
    }
    else if (category === "success"){
        className = 'alert-success'
    }
    else if (category === "error"){
        className = 'alert-danger'
    }
    else if (category === "warning"){
        className = 'alert-warning'
    }

    idNum++;

    const flashId = "flash-" + (idNum - 1);

    let insert = "";
    if (subMessage !== "") {
        insert = `<p>${subMessage}</p>`;
    }


    let result = `
        <div class="alert ${className} alert-dismissible fade show mt-3 text-center flash-message" role="alert" id="${flashId}">
            <b>${msg}</b>
            ${insert}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            <div class="progress-bar"></div>
        </div>
    `;

    document.getElementById('flashMessages').innerHTML += result;

    setTimeout(function() {
        try {
            let element = document.getElementById(flashId);
            element.style.transition = "opacity 0.25s ease-out";
            element.style.opacity = "0"; // Fading out
        }
        catch {
            return;
        }

        setTimeout(function() {
            element.remove();
        }, 250);

    }, 10000);
}