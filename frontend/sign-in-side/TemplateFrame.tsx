import * as React from 'react';
import {
  createTheme,
  ThemeProvider,
  PaletteMode,
  styled,
} from '@mui/material/styles';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Box from '@mui/material/Box';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import ArrowBackRoundedIcon from '@mui/icons-material/ArrowBackRounded';
import ToggleColorMode from './ToggleColorMode';
import getSiteTheme from '../theme/getTheme';

const StyledAppBar = styled(AppBar)(({ theme }) => ({
  position: 'relative',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  flexShrink: 0,
  borderBottom: '1px solid',
  borderColor: theme.palette.divider,
  backgroundColor: theme.palette.background.paper,
  boxShadow: theme.shadows[1],
  backgroundImage: 'none',
  zIndex: theme.zIndex.drawer + 1,
  flex: '0 0 auto',
}));

interface TemplateFrameProps {
  mode: PaletteMode;
  toggleColorMode: () => void;
  children: React.ReactNode;
}

export default function TemplateFrame({
  mode,
  toggleColorMode,
  children,
}: TemplateFrameProps) {
  const signInSideTheme = createTheme(getSiteTheme(mode));

  return (
    <ThemeProvider theme={signInSideTheme}>
      <Box sx={{ height: '100dvh', display: 'flex', flexDirection: 'column' }}>
        <StyledAppBar>
          <Toolbar
            variant="dense"
            disableGutters
            sx={{
              display: 'flex',
              justifyContent: 'space-between',
              width: '100%',
              p: '8px 12px',
            }}
          >
            <Button
              variant="text"
              size="small"
              aria-label="Back to home"
              startIcon={<ArrowBackRoundedIcon />}
              component="a"
              href="/"
              sx={{ display: { xs: 'none', sm: 'flex' } }}
            >
              Back to home
            </Button>
            <IconButton
              size="small"
              aria-label="Back to home"
              component="a"
              href="/"
              sx={{ display: { xs: 'auto', sm: 'none' } }}
            >
              <ArrowBackRoundedIcon />
            </IconButton>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <ToggleColorMode
                data-screenshot="toggle-mode"
                mode={mode}
                toggleColorMode={toggleColorMode}
              />
            </Box>
          </Toolbar>
        </StyledAppBar>
        <Box sx={{ flex: '1 1', overflow: 'auto' }}>{children}</Box>
      </Box>
    </ThemeProvider>
  );
}
