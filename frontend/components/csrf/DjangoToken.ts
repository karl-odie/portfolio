var getToken = function () {
  var tokenValue = 'notokenfound';
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
