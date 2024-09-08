import * as React from 'react';
import { Box, Card, CardContent, Typography } from '@mui/material';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';

export default function ControlPanel({
  value,
  onChange,
}: {
  value: string;
  onChange: React.Dispatch<React.SetStateAction<string>>;
}) {
  return (
    <Card sx={{ position: 'absolute', top: '10px', left: '10px' }}>
      <FormControl>
        <CardContent sx={{ flex: '1 0 auto' }}>
          <FormLabel id="demo-row-radio-buttons-group-label">
            <Typography variant="subtitle2">Track Color</Typography>
          </FormLabel>
        </CardContent>
        <Box>
          <RadioGroup
            row
            aria-labelledby="demo-row-radio-buttons-group-label"
            name="row-radio-buttons-group"
            value={value}
            onChange={(evt) => onChange(evt.target.value)}
          >
            <FormControlLabel
              value="heartRate"
              control={<Radio size="small" />}
              label="Heart Rate"
            />
            <FormControlLabel
              value="cadence"
              control={<Radio size="small" />}
              label="Cadence"
            />
            <FormControlLabel
              value="altitude"
              control={<Radio size="small" />}
              label="Altitude"
            />
          </RadioGroup>
        </Box>
      </FormControl>
    </Card>
  );
}
