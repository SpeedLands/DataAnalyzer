document.addEventListener("DOMContentLoaded", function () {
    // Alternar navbar
    document.getElementById('navbar-toggle').addEventListener('click', function () {
        const menu = document.getElementById('navbar-menu');
        menu.classList.toggle('hidden');
        menu.classList.toggle('scale-100');
    });

    // Manejo del modal
    const modal = document.getElementById('login-modal');
    const modalTriggers = ['open-modal', 'open-modal-1']; // Botones que abren el modal

    modalTriggers.forEach(triggerId => {
        document.getElementById(triggerId).addEventListener('click', () => {
            modal.classList.remove('hidden');
        });
    });

    document.getElementById('close-modal').addEventListener('click', () => {
        modal.classList.add('hidden');
    });

    // Cambiar entre tabs de login/registro
    function switchTab(showElement, hideElement, activeTab, inactiveTab) {
        showElement.classList.remove('hidden');
        hideElement.classList.add('hidden');
        activeTab.classList.add('border-b-2', 'border-indigo-600', 'text-indigo-600', 'hover:text-indigo-800');
        inactiveTab.classList.remove('border-b-2', 'border-indigo-600', 'text-indigo-600', 'hover:text-indigo-800');
    }

    document.getElementById('login-tab').addEventListener('click', () => {
        switchTab(
            document.getElementById('login-form'),
            document.getElementById('register-form'),
            document.getElementById('login-tab'),
            document.getElementById('register-tab')
        );
    });

    document.getElementById('register-tab').addEventListener('click', () => {
        switchTab(
            document.getElementById('register-form'),
            document.getElementById('login-form'),
            document.getElementById('register-tab'),
            document.getElementById('login-tab')
        );
    });

    // Alternar visibilidad de la contraseña
    const passwordInput = document.getElementById("login_password");
    const togglePasswordIcon = document.getElementById("toggle-password-icon");

    document.getElementById("toggle-password").addEventListener("click", function () {
        const isPassword = passwordInput.getAttribute("type") === "password";
        passwordInput.setAttribute("type", isPassword ? "text" : "password");
        togglePasswordIcon.classList.toggle("bi-eye", !isPassword);
        togglePasswordIcon.classList.toggle("bi-eye-slash", isPassword);
    });

    // Uso de jQuery Validator para el formulario
    $("#login-form-element").validate({
        errorClass: "error",
        rules: {
            login_email: {
                required: true,
                email: true,
                minlength: 5,
                maxlength: 50
            },
            login_password: {
                required: true,
                minlength: 6,
                maxlength: 50
            }
        },
        messages: {
            login_email: {
                required: "Por favor, introduce tu correo electrónico",
                email: "Introduce un correo electrónico válido",
                minlength: "El correo electrónico debe tener al menos 5 caracteres",
                maxlength: "El correo electrónico no debe superar los 50 caracteres"
            },
            login_password: {
                required: "Por favor, introduce tu contraseña",
                minlength: "La contraseña debe tener al menos 6 caracteres",
                maxlength: "La contraseña no debe superar los 50 caracteres"
            }
        },
        submitHandler: function (form) {
            const emailValue = $('#login_email').val();
            const passwordValue = $('#login_password').val();

            // Enviar datos de login via fetch
            fetch("/login", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: emailValue,
                    password: passwordValue
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    alert('Éxito: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error en la solicitud: ' + error.message);
            });
        }
    });
    $("#register-form-element").validate({
        errorClass: "error",
        rules: {
            register_email: {
                required: true,
                email: true,
                minlength: 5,
                maxlength: 50
            },
            register_password: {
                required: true,
                minlength: 6,
                maxlength: 50
            },
            register_confirm_password: {
                required: true,
                minlength: 6,
                maxlength: 50,
                equalTo: "#register_password"  // Asegura que la confirmación coincida con la contraseña
            }
        },
        messages: {
            register_email: {
                required: "Por favor, introduce tu correo electrónico",
                email: "Introduce un correo electrónico válido",
                minlength: "El correo electrónico debe tener al menos 5 caracteres",
                maxlength: "El correo electrónico no debe superar los 50 caracteres"
            },
            register_password: {
                required: "Por favor, introduce tu contraseña",
                minlength: "La contraseña debe tener al menos 6 caracteres",
                maxlength: "La contraseña no debe superar los 50 caracteres"
            },
            register_confirm_password: {
                required: "Por favor, confirma tu contraseña",
                minlength: "La contraseña debe tener al menos 6 caracteres",
                maxlength: "La contraseña no debe superar los 50 caracteres",
                equalTo: "Las contraseñas no coinciden"
            }
        },
        submitHandler: function (form) {
            const emailValue = $('#register_email').val();
            const passwordValue = $('#register_password').val();
    
            // Enviar datos de registro via fetch
            fetch("/register", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: emailValue,
                    password: passwordValue
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    alert('Éxito: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error en la solicitud: ' + error.message);
            });
        }
    });    
});
