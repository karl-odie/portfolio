import * as React from 'react';
import { createRoot } from 'react-dom/client';
import SignUp from './signup/SignUp';

document.body.style.margin = '0px';
const container = document.getElementById('root');
const root = createRoot(container!);
root.render(<SignUp />);
