import * as React from 'react';
import { Box, Card, CardContent, Typography, Link } from '@mui/material';
import { Activity } from '@portfolio/api-client';
import ActivitySVG from './ActivitySVG';
import {
  format_distance,
  format_duration,
  format_elevation,
  format_pace,
} from './Units';
import Metric from './Metric';

export default function ActivityPanel({ activity }: { activity: Activity }) {
  return (
    <Card sx={{ display: 'flex', margin: '5px' }}>
      <Box>
        <ActivitySVG activity={activity.uuid} />
      </Box>
      <Box sx={{ display: 'flex', flexDirection: 'column' }}>
        <Box>
          <CardContent sx={{ flex: '1 0 auto' }}>
            <Link href={'/fitness/activity/' + activity.uuid + '/'}>
              <Typography
                variant="subtitle1"
                component="span"
                sx={{ color: 'text.secondary' }}
              >
                {activity.time.toLocaleString()}{' '}
              </Typography>
              <Typography component="span" variant="h5">
                {activity.name}
              </Typography>
            </Link>
          </CardContent>
        </Box>
        <Box sx={{ display: 'flex', flexDirection: 'row' }}>
          <Box sx={{ display: 'flex', flexDirection: 'column', margin: '5px' }}>
            <Metric
              name="Distance"
              value={format_distance(activity.distance)}
            />
            <Metric
              name="Duration"
              value={format_duration(activity.duration)}
            />
            <Metric
              name="Pace"
              value={format_pace(activity.duration, activity.distance)}
            />
          </Box>
          <Box sx={{ display: 'flex', flexDirection: 'column', margin: '5px' }}>
            <Metric
              name="Elevation"
              value={format_elevation(activity.elevation)}
            />
            <Metric name="TRIMP" value={(activity.trimp || ' -').toString()} />
          </Box>
        </Box>
      </Box>
    </Card>
  );
}
