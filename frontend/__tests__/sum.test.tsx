//import * as React from 'react'
//import {beforeAll, afterEach, afterAll, test, expect} from '@jest/globals';
//import {http, HttpResponse} from 'msw'
//import {setupServer} from 'msw/node'
//import {render, fireEvent, screen} from '@testing-library/react'
import { test, expect } from '@jest/globals';
import { sum } from '../sum';
import '@testing-library/jest-dom';

test('test sum', () => {
  expect(sum(1, 2)).toBe(3);
});
