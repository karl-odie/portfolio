import * as React from 'react';
import { Box, Card, CardContent, Typography } from '@mui/material';
import { Activity } from '@portfolio/api-client';
import ActivitySVG from './ActivitySVG';

export default function ActivityPanel({ activity }: { activity: Activity }) {
  return (
    <Card sx={{ display: 'flex', margin: '5px' }}>
      <Box>
        <ActivitySVG activity={activity.uuid} />
      </Box>
      <Box sx={{ display: 'flex', flexDirection: 'column' }}>
        <CardContent sx={{ flex: '1 0 auto' }}>
          <Typography component="div" variant="h5">
            {activity.name}
          </Typography>
          <Typography
            variant="subtitle1"
            component="div"
            sx={{ color: 'text.secondary' }}
          >
            {activity.time.toLocaleString()}
          </Typography>
        </CardContent>
      </Box>
    </Card>
  );
}
