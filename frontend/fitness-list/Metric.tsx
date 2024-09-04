import * as React from 'react';
import { Box, Card, CardContent, Typography } from '@mui/material';

export default function Metric({
  name,
  value,
}: {
  name: string;
  value: string;
}) {
  return (
    <CardContent sx={{ flex: '1 0 auto' }}>
      <Typography variant="subtitle2" component="span">
        {name}:{' '}
      </Typography>
      <Typography component="span" sx={{ color: 'text.secondary' }}>
        {value}
      </Typography>
    </CardContent>
  );
}
