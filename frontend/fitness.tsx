import * as React from 'react';
import { createRoot } from 'react-dom/client';
import FitnessList from './fitness-list/List';

document.body.style.margin = '0px';
const container = document.getElementById('root');
const root = createRoot(container!);
root.render(<FitnessList />);
