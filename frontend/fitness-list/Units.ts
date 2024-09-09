function one_figure_round(value: number, precision: number): number {
  const factor = Math.pow(10, precision);
  return Math.round(value * factor) / factor;
}

function format_distance(metres: number | null): string {
  if (metres === null) {
    return '-';
  }
  var kilo = one_figure_round(metres / 1000, 1);
  return kilo + ' km';
}

function format_elevation(metres: number | null): string {
  if (metres === null) {
    return '-';
  }
  var kilo = one_figure_round(metres, 0);
  return kilo + ' m';
}

function format_duration(total_seconds: number | null): string {
  if (total_seconds === null) {
    return '-';
  }
  total_seconds = Math.floor(total_seconds);
  if (total_seconds > 3600) {
    var hours = Math.floor(total_seconds / 3600);
    var remaining_seconds = total_seconds - hours * 3600;
    var minutes = Math.floor(remaining_seconds / 60);
    var remaining_seconds = remaining_seconds - minutes * 60;
    return hours + ' hr ' + minutes + ' min ' + remaining_seconds + ' sec';
  }
  if (total_seconds > 60) {
    var minutes = Math.floor(total_seconds / 60);
    var remaining_seconds = total_seconds - minutes * 60;
    return minutes + ' min ' + remaining_seconds + ' sec';
  }
  return total_seconds + ' s';
}

function format_pace(seconds: number | null, metres: number | null): string {
  if (seconds === null || metres === null) {
    return '-';
  }
  var kilo = metres / 1000.0;
  var seconds_per_km = seconds / kilo;
  var minutes_per_km = Math.floor(seconds_per_km / 60.0);
  var remaining_seconds = Math.floor(seconds_per_km - minutes_per_km * 60);
  return minutes_per_km + ':' + remaining_seconds + '/km';
}

export { format_distance, format_duration, format_elevation, format_pace };
