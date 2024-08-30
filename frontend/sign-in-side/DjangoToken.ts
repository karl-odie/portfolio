var getToken = function () {
  var tokenValue = null;
  var element = <HTMLInputElement>(
    document.querySelector('[name=csrfmiddlewaretoken]')
  );
  if (element) {
    tokenValue = element.value;
  }
  return tokenValue;
};

var csrftoken = getToken();

export { csrftoken };
