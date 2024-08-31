import * as React from 'react';

import { csrftoken } from './DjangoToken';
import { Input } from '@mui/material';

const DjangoCSRFToken = () => {
  return <Input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />;
};

export default DjangoCSRFToken;
