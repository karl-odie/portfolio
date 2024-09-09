import * as React from 'react';
import { Map, Source, Layer, LayerProps } from 'react-map-gl/maplibre';
import 'maplibre-gl/dist/maplibre-gl.css';
import { Biometrics } from '@portfolio/api-client';
import {
  mapBounds,
  colorFromKey,
  BioBounds,
  dataBounds,
} from './track_properties';
import ControlPanel from './Control';
import { Box } from '@mui/material';
import { useTheme } from '@mui/material/styles';

function startPoint(biometrics: Biometrics[]) {
  if (biometrics.length == 0) {
    return {
      type: 'Point',
      coordinates: [-3.14, 54.6],
    };
  }
  var start = biometrics[0];
  return {
    type: 'Point',
    coordinates: [start.longitude, start.latitude],
  };
}

function endPoint(biometrics: Biometrics[]) {
  if (biometrics.length == 0) {
    return {
      type: 'Point',
      coordinates: [-3.14, 54.6],
    };
  }
  var end = biometrics[biometrics.length - 1];
  return {
    type: 'Point',
    coordinates: [end.longitude, end.latitude],
  };
}

function geoLine(
  index: number,
  previous_point: Biometrics,
  current_point: Biometrics,
  color_key: string,
  bounds: BioBounds,
) {
  var color = colorFromKey(current_point, color_key, bounds);

  return {
    type: 'Feature',
    properties: {
      id: index,
      elevation: current_point.altitude,
      speed: 0.0,
      distance: 0.0,
      cadence: current_point.cadence,
      heart_rate: current_point.heartRate,
      color: color,
    },
    geometry: {
      type: 'LineString',
      coordinates: [
        [previous_point.longitude, previous_point.latitude],
        [current_point.longitude, current_point.latitude],
      ],
    },
  };
}

const startPointLayer: LayerProps = {
  id: 'startPoint',
  type: 'circle',
  paint: {
    'circle-radius': 7,
    'circle-color': '#00ff00',
    'circle-stroke-color': '#000000',
    'circle-stroke-width': 1,
  },
  filter: ['==', 'label', 'start'],
};

const endPointLayer: LayerProps = {
  id: 'endPoint',
  type: 'circle',
  paint: {
    'circle-radius': 7,
    'circle-color': '#ff0000',
    'circle-stroke-color': '#000000',
    'circle-stroke-width': 1,
  },
  filter: ['==', 'label', 'end'],
};

const lineLayer: LayerProps = {
  id: 'lines',
  type: 'line',
  layout: {
    'line-join': 'round',
    'line-cap': 'round',
  },
  paint: {
    'line-width': 3,
    'line-color': ['get', 'color'],
  },
};

function geoJson(biometrics: Biometrics[], color_key: string) {
  var features = [];
  var bounds = dataBounds(biometrics);
  for (var i = 1; i < biometrics.length; i++) {
    var previous_point = biometrics[i - 1];
    var current_point = biometrics[i];
    features.push(geoLine(i, previous_point, current_point, color_key, bounds));
  }
  features.push({
    type: 'Feature',
    geometry: startPoint(biometrics),
    properties: {
      label: 'start',
    },
  });
  features.push({
    type: 'Feature',
    geometry: endPoint(biometrics),
    properties: {
      label: 'end',
    },
  });
  return {
    type: 'FeatureCollection',
    features: features,
  };
}

export default function FitnessMap({
  biometrics,
}: {
  biometrics: Biometrics[];
}) {
  const [colorKey, setColorKey] = React.useState('altitude');
  const theme = useTheme();

  function mapStyle(): string {
    console.log('Theme', theme);
    if (theme.palette.mode == 'dark') {
      return '/static/map_style_dark.json';
    }
    return '/static/map_style_light.json';
  }

  console.log('Rendering map from', biometrics);
  return (
    <Box sx={{ position: 'relative' }}>
      <Map
        initialViewState={{
          bounds: mapBounds(biometrics),
        }}
        style={{ width: 800, height: 800 }}
        mapStyle={mapStyle()}
        maplibreLogo={false}
        styleDiffing
      >
        <Source type="geojson" data={geoJson(biometrics, colorKey)}>
          <Layer {...lineLayer} />
          <Layer {...startPointLayer} />
          <Layer {...endPointLayer} />
        </Source>
      </Map>
      <ControlPanel value={colorKey} onChange={setColorKey} />
    </Box>
  );
}
