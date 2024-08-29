var getCookie = function (name: string) {
  var cookieValue = null;
  console.log('Looking for cooke', name, 'in', document.cookie);
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    console.log('Split into', cookies);
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      console.log('Considering', cookie);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        console.log('Found value', cookieValue);
        break;
      }
    }
  }
  var element = <HTMLInputElement>(
    document.querySelector('[name=csrfmiddlewaretoken]')
  );
  if (element) {
    cookieValue = element.value;
  }
  return cookieValue;
};

var csrftoken = getCookie('csrftoken');

export { csrftoken };
