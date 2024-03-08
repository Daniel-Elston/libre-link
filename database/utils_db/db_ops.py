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
            'is_low': item.get('isLow', False)
        }
        preparations.append(prepared_item)
    return preparations


def prepare_trends(data, measurement_id):
    preparations = []
    for item in data:
        prepared_item = {
            'measurement_id': measurement_id,
            'timestamp': item.get('Timestamp'),
            'trend_arrow': None if np.isnan(item.get('TrendArrow', np.nan)) else item.get('TrendArrow'),
            # if np.isnan(item.get('TrendMessage', np.nan)) else item.get('TrendMessage'),
            'trend_message': None,
        }
        preparations.append(prepared_item)
    return preparations
