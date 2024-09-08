import { Biometrics } from '@portfolio/api-client';
import { LngLat, LngLatBounds } from 'maplibre-gl';

function mapBounds(biometrics: Biometrics[]): LngLatBounds {
  if (biometrics.length == 0) {
    return new LngLatBounds(new LngLat(54.6, -3.14), new LngLat(54.6, -3.14));
  }
  var max_longitude = -180.0;
  var min_longitude = 180.0;
  var max_latitude = -90.0;
  var min_latitude = 90.0;
  for (var point of biometrics) {
    var longitude = point.longitude;
    var latitude = point.latitude;
    if (longitude > max_longitude) {
      max_longitude = longitude;
    }
    if (longitude < min_longitude) {
      min_longitude = longitude;
    }
    if (latitude > max_latitude) {
      max_latitude = latitude;
    }
    if (latitude < min_latitude) {
      min_latitude = latitude;
    }
  }
  var lat_padding = 0.1 * (max_latitude - min_latitude);
  var lon_padding = 0.1 * (max_longitude - min_longitude);

  return new LngLatBounds(
    new LngLat(min_longitude - lon_padding, min_latitude - lat_padding),
    new LngLat(max_longitude + lon_padding, max_latitude + lat_padding),
  );
}

interface Bounds {
  max: number;
  min: number;
}

interface BioBounds {
  heartRate: Bounds;
  cadence: Bounds;
  altitude: Bounds;
}

function dataBounds(biometrics: Biometrics[]): BioBounds {
  var max_heartRate = 0;
  var min_heartRate = 0;
  var max_cadence = 0;
  var min_cadence = 0;
  var max_altitude = 0;
  var min_altitude = 0;
  for (var point of biometrics) {
    if (point.heartRate && point.heartRate > max_heartRate) {
      max_heartRate = point.heartRate;
    }
    if (point.heartRate && point.heartRate < min_heartRate) {
      min_heartRate = point.heartRate;
    }
    if (point.cadence && point.cadence > max_cadence) {
      max_cadence = point.cadence;
    }
    if (point.cadence && point.cadence < min_cadence) {
      min_cadence = point.cadence;
    }
    if (point.altitude && point.altitude > max_altitude) {
      max_altitude = point.altitude;
    }
    if (point.altitude && point.altitude < min_altitude) {
      min_altitude = point.altitude;
    }
  }
  return {
    heartRate: { max: max_heartRate, min: min_heartRate },
    cadence: { max: max_cadence, min: min_cadence },
    altitude: { max: max_altitude, min: min_altitude },
  };
}

function boundNonDim(nonDim: number, bounds: Bounds): number {
  return bounds.min + nonDim * (bounds.max - bounds.min);
}

function colorFromKey(
  current_point: Biometrics,
  color_key: string,
  bounds: BioBounds,
): string {
  var value: number | null = null;
  var valueBounds: Bounds | null = null;
  if (color_key == 'heartRate') {
    value = current_point.heartRate;
    valueBounds = bounds.heartRate;
  } else if (color_key == 'cadence') {
    value = current_point.cadence;
    valueBounds = bounds.cadence;
  } else if (color_key == 'altitude') {
    value = current_point.altitude;
    valueBounds = bounds.altitude;
  }
  if (value === null || valueBounds === null) {
    return '#000000';
  }
  if (value < boundNonDim(0.1, valueBounds)) {
    return '#00e5c4';
  }
  if (value < boundNonDim(0.2, valueBounds)) {
    return '#00e075';
  }
  if (value < boundNonDim(0.3, valueBounds)) {
    return '#00dc29';
  }
  if (value < boundNonDim(0.4, valueBounds)) {
    return '#1ed800';
  }
  if (value < boundNonDim(0.5, valueBounds)) {
    return '#65d400';
  }
  if (value < boundNonDim(0.6, valueBounds)) {
    return '#a8cf00';
  }
  if (value < boundNonDim(0.7, valueBounds)) {
    return '#cbae00';
  }
  if (value < boundNonDim(0.8, valueBounds)) {
    return '#c76800';
  }
  if (value < boundNonDim(0.9, valueBounds)) {
    return '#c32500';
  }
  return '#bf001b';
}

export { mapBounds, colorFromKey, BioBounds, dataBounds };
