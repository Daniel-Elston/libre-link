from __future__ import annotations

import numpy as np


def prepare_measurements(data):
    preparations = []
    for item in data:
        prepared_item = {
            'factory_timestamp': item.get('FactoryTimestamp'),
            'timestamp': item.get('Timestamp'),
            'type': item.get('type'),
            'value_mg_per_dl': item.get('ValueInMgPerDl'),
            'measurement_colour': item.get('MeasurementColor'),
            'glucose_units': item.get('GlucoseUnits'),
            'value': item.get('Value'),
            'is_high': item.get('isHigh', False),
            'is_low': item.get('isLow', False),
            'trend_arrow': None if np.isnan(item.get('TrendArrow', np.nan)) else item.get('TrendArrow'),
            'trend_message': None
        }
        preparations.append(prepared_item)
    return preparations
