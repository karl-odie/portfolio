var getFormErrors = function () {
  var emailError = false;
  var emailErrorMessage = '';
  var passwordError = false;
  var passwordErrorMessage = '';
  var element = document.getElementById('form-errors') as HTMLScriptElement;
  var text = element.textContent;
  if (text) {
    var errors = JSON.parse(text);
    var email_errors = errors['email'];
    var password_errors = errors['password1'];
    console.log('Extracted errors', email_errors, password_errors);
    if (email_errors) {
      emailError = true;
      emailErrorMessage = email_errors[0];
    }
    if (password_errors) {
      passwordError = true;
      passwordErrorMessage = password_errors[0];
    }
  }
  return {
    emailError: emailError,
    emailMessage: emailErrorMessage,
    passwordError: passwordError,
    passwordMessage: passwordErrorMessage,
  };
};

var formErrors = getFormErrors();

export { formErrors };
