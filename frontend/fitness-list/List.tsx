import * as React from 'react';

import { List } from '@mui/material';
import TemplateFrame from '../template/TemplateFrame';
import { activityAPI } from '../api/api';
import { Activity } from '../api-client';
import ActivityPanel from './ActivityPanel';

export default function FitnessList() {
  let blankArray: Activity[] = [];

  const [activities, SetActivities] = React.useState(blankArray);

  React.useEffect(() => {
    activityAPI.activitiesList().then((response) => {
      console.log('Got activities', response);
      SetActivities(response);
    });
  }, []);

  return (
    <TemplateFrame>
      <List>
        {activities.map((result) => (
          <ActivityPanel activity={result} />
        ))}
      </List>
    </TemplateFrame>
  );
}
