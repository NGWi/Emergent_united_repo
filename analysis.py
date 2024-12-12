def analyze_biometric_data(data):
    """
    Analyzes biometric data for health issues.

    Parameters:
    - data (dict): A dictionary containing biometric data with keys 'heart_rate', 'blood_oxygen', 'glucose_level', and 'hrv'.

    Returns:
    - dict: Analysis results indicating any health issues.
    """
    results = {}
    
    # Heart Rate Analysis
    heart_rate = data.get('heart_rate', None)
    if heart_rate is not None:
        if heart_rate < 60 or heart_rate > 100:
            results['heart_rate_issue'] = "Abnormal heart rate detected."
        else:
            results['heart_rate_issue'] = "Heart rate is normal."
    else:
        results['heart_rate_issue'] = "Heart rate data not provided."

    # Blood Oxygen Analysis
    blood_oxygen = data.get('blood_oxygen', None)
    if blood_oxygen is not None:
        if blood_oxygen < 95:
            results['blood_oxygen_issue'] = "Low blood oxygen levels detected."
        else:
            results['blood_oxygen_issue'] = "Blood oxygen levels are normal."
    else:
        results['blood_oxygen_issue'] = "Blood oxygen data not provided."

    # Glucose Level Analysis
    glucose_level = data.get('glucose_level', None)
    if glucose_level is not None:
        if glucose_level < 70 or glucose_level >= 200:
            results['glucose_level_issue'] = "Abnormal glucose levels detected."
        else:
            results['glucose_level_issue'] = "Glucose levels are normal."
    else:
        results['glucose_level_issue'] = "Glucose level data not provided."

    # HRV Analysis
    hrv = data.get('hrv', None)
    if hrv is not None:
        if data['hrv'] < 19:
            """
            https://www.webmd.com/heart/what-is-heart-rate-variability#
            :~:text=heart%20rate%20variability-,In%20healthy%20adults,-%2C%20average%20heart%20rate
            """
            results['hrv_issue'] = "Low HRV detected, which may indicate stress or health issues."
        else:
            results['hrv_issue'] = "HRV is within normal range."
    else:
        results['hrv_issue'] = "HRV data not provided."

    return results