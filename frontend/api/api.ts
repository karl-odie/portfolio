import { ActivitiesApi, Configuration } from '../api-client';
import { csrftoken } from '../components/csrf/DjangoToken';

const currentURL = new URL(window.location.href);
const basePath = currentURL.protocol + '//' + currentURL.host + '/';

const apiConfiguration = new Configuration({
  basePath: basePath,
  headers: {
    'X-CSRFToken': csrftoken,
  },
});

const activityAPI = new ActivitiesApi(apiConfiguration);

export { activityAPI };
