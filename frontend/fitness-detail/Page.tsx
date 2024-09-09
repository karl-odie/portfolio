import * as React from 'react';
import { CircularProgress } from '@mui/material';
import TemplateFrame from '../template/TemplateFrame';
import { activityAPI } from '../api/api';
import { Activity, Biometrics } from '../api-client';
import FitnessMap from './Map';

export default function FitnessDetail() {
  function activityInitialState(): Activity | null {
    return null;
  }
  const initialBiometrics: Biometrics[] = [];

  const currentURL = new URL(window.location.href);
  const path = currentURL.pathname.split('/');
  var uuid_value = path[path.length - 2];

  const [activity, SetActivity] = React.useState(activityInitialState);
  const [biometrics, SetBiometrics] = React.useState(initialBiometrics);

  React.useEffect(() => {
    activityAPI.activitiesRetrieve({ uuid: uuid_value }).then((response) => {
      console.log('Got activity', response);
      SetActivity(response);
    });
  }, []);

  React.useEffect(() => {
    activityAPI
      .activitiesBiometricsList({ uuid: uuid_value })
      .then((response) => {
        console.log('Got biometrics', response);
        SetBiometrics(response);
      });
  }, []);

  function renderMap() {
    if (biometrics.length > 0) {
      return <FitnessMap biometrics={biometrics} />;
    }
    return <CircularProgress />;
  }

  return <TemplateFrame>{renderMap()}</TemplateFrame>;
}
