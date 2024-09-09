import * as React from 'react';
import { createRoot } from 'react-dom/client';
import ButtonAppBar from './navbar';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

document.body.style.margin = '0px';
const container = document.getElementById('root');
const root = createRoot(container!);
root.render(
  <>
    <ButtonAppBar />
    <h1>Hello, react!</h1>
  </>,
);
