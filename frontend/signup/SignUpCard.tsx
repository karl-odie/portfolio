import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import MuiCard from '@mui/material/Card';
import FormLabel from '@mui/material/FormLabel';
import FormControl from '@mui/material/FormControl';
import Link from '@mui/material/Link';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';

import { styled } from '@mui/material/styles';

import { SitemarkIcon } from '../components/icons/CustomIcons';
import DjangoCSRFToken from '../components/csrf/DjangoCSRFToken';
import { formErrors } from './FormErrors';

const Card = styled(MuiCard)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignSelf: 'center',
  width: '100%',
  padding: theme.spacing(4),
  gap: theme.spacing(2),
  boxShadow:
    'hsla(220, 30%, 5%, 0.05) 0px 5px 15px 0px, hsla(220, 25%, 10%, 0.05) 0px 15px 35px -5px',
  [theme.breakpoints.up('sm')]: {
    width: '450px',
  },
  ...theme.applyStyles('dark', {
    boxShadow:
      'hsla(220, 30%, 5%, 0.5) 0px 5px 15px 0px, hsla(220, 25%, 10%, 0.08) 0px 15px 35px -5px',
  }),
}));

export default function SignInCard() {
  const [emailError, setEmailError] = React.useState(formErrors.emailError);
  const [emailErrorMessage, setEmailErrorMessage] = React.useState(
    formErrors.emailMessage,
  );
  const [passwordError, setPasswordError] = React.useState(
    formErrors.passwordError,
  );
  const [passwordErrorMessage, setPasswordErrorMessage] = React.useState(
    formErrors.passwordMessage,
  );
  const [passwordMatchError, setPasswordMatchError] = React.useState(false);
  const [passwordMatchErrorMessage, setPasswordMatchErrorMessage] =
    React.useState('');

  const validateEmail = () => {
    const email = document.getElementById('email') as HTMLInputElement;
    if (!email) {
      return null;
    }

    if (!email.value || !/\S+@\S+\.\S+/.test(email.value)) {
      setEmailError(true);
      setEmailErrorMessage('Please enter a valid email address.');
    } else {
      setEmailError(false);
      setEmailErrorMessage('');
    }
  };

  const validatePassword = () => {
    const password1 = document.getElementById('password1') as HTMLInputElement;
    if (!password1) {
      return null;
    }

    if (!password1.value || password1.value.length < 8) {
      setPasswordError(true);
      setPasswordErrorMessage('Password must be at least 8 characters long.');
    } else {
      setPasswordError(false);
      setPasswordErrorMessage('');
    }
    validatePasswordMatch();
  };

  const validatePasswordMatch = () => {
    const password1 = document.getElementById('password1') as HTMLInputElement;
    const password2 = document.getElementById('password2') as HTMLInputElement;
    if (!password1 || !password2) {
      return null;
    }

    if (password1.value == password2.value) {
      setPasswordMatchError(false);
      setPasswordMatchErrorMessage('');
    } else {
      setPasswordMatchError(true);
      setPasswordMatchErrorMessage('Passwords must match.');
    }
  };

  return (
    <Card variant="outlined">
      <Box sx={{ display: { xs: 'flex', md: 'none' } }}>
        <SitemarkIcon />
      </Box>
      <Typography
        component="h1"
        variant="h4"
        sx={{ width: '100%', fontSize: 'clamp(2rem, 10vw, 2.15rem)' }}
      >
        Sign up
      </Typography>
      <Box>
        Already have an account?{' '}
        <Link
          href="/accounts/login/"
          variant="body2"
          sx={{ alignSelf: 'baseline' }}
        >
          Sign in.
        </Link>
      </Box>
      <Box
        component="form"
        noValidate
        method="post"
        action="/accounts/signup/"
        sx={{ display: 'flex', flexDirection: 'column', width: '100%', gap: 2 }}
      >
        <DjangoCSRFToken />
        <FormControl>
          <FormLabel htmlFor="email">Email</FormLabel>
          <TextField
            error={emailError}
            helperText={emailErrorMessage}
            id="email"
            type="email"
            name="email"
            placeholder="your@email.com"
            autoComplete="email"
            autoFocus
            required
            fullWidth
            variant="outlined"
            color={emailError ? 'error' : 'primary'}
            sx={{ ariaLabel: 'email' }}
            onChange={validateEmail}
          />
        </FormControl>
        <FormControl>
          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
            <FormLabel htmlFor="password1">Password</FormLabel>
          </Box>
          <TextField
            error={passwordError}
            helperText={passwordErrorMessage}
            name="password1"
            placeholder="••••••"
            type="password"
            id="password1"
            autoComplete="current-password"
            autoFocus
            required
            fullWidth
            variant="outlined"
            color={passwordError ? 'error' : 'primary'}
            onChange={validatePassword}
          />
        </FormControl>
        <Box>
          <List>
            <ListItem>
              Your password can’t be too similar to your other personal
              information.
            </ListItem>
            <ListItem>
              Your password must contain at least 8 characters.
            </ListItem>
            <ListItem>
              Your password can’t be a commonly used password.
            </ListItem>
            <ListItem>Your password can’t be entirely numeric.</ListItem>
          </List>
        </Box>
        <FormControl>
          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
            <FormLabel htmlFor="password2">Password</FormLabel>
          </Box>
          <TextField
            error={passwordMatchError}
            helperText={passwordMatchErrorMessage}
            name="password2"
            placeholder="••••••"
            type="password"
            id="password2"
            autoComplete="password2"
            autoFocus
            required
            fullWidth
            variant="outlined"
            color={passwordMatchError ? 'error' : 'primary'}
            onChange={validatePasswordMatch}
          />
        </FormControl>
        <Button type="submit" fullWidth variant="contained">
          Sign up
        </Button>
      </Box>
    </Card>
  );
}
