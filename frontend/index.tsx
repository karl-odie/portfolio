import * as React from 'react';
import { createRoot } from 'react-dom/client';
import ButtonAppBar from './navbar';

const container = document.getElementById('root');
const root = createRoot(container!);
root.render(
  <div>
    <ButtonAppBar />
    <h1>Hello, react!</h1>
  </div>,
);
