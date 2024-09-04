import * as React from 'react';

import { activityAPI } from '../api/api';
import { ActivitySVGPoints } from '../api-client';

function join_pair(point: ActivitySVGPoints): string {
  return point.x + ',' + point.y;
}

function points_to_polyline(points: ActivitySVGPoints[]): string {
  let pairs: string[] = points.map(join_pair);
  return pairs.join(' ');
}

export default function ActivitySVG({ activity }: { activity: string }) {
  let blankArray: ActivitySVGPoints[] = [];

  const [points, SetPoints] = React.useState(blankArray);

  React.useEffect(() => {
    activityAPI.activitiesSvgList({ uuid: activity }).then((result) => {
      console.log('Got points', result);
      SetPoints(result);
    });
  }, []);

  return (
    <svg xmlns="http://www.w3.org/2000/svg" height="100" width="100">
      <polyline
        fill="none"
        stroke-width="3px"
        stroke="white"
        points={points_to_polyline(points)}
      />
    </svg>
  );
}
