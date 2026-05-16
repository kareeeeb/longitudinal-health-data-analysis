import xml.etree.ElementTree as ET
import pandas as pd

# 1. Load the XML
print("Loading export.xml... this might take a moment.")
tree = ET.parse('export.xml')
root = tree.getroot()

data = []

# 2. Define our mapping for Sleep Stages
# Apple stores these as integers (6=REM, 7=Core/Light, 8=Deep, etc.)
sleep_lookup = {
    'HKCategoryValueSleepAnalysisAsleepUnspecified': 'Asleep',
    'HKCategoryValueSleepAnalysisAsleepDeep': 'Deep',
    'HKCategoryValueSleepAnalysisAsleepCore': 'Core',
    'HKCategoryValueSleepAnalysisAsleepREM': 'REM',
    'HKCategoryValueSleepAnalysisAwake': 'Awake'
}

# 3. The Loop
for record in root.findall('Record'):
    r_type = record.attrib.get('type')
    
    # Handle Heart Rate, HRV, and Weight
    if r_type in [
        'HKQuantityTypeIdentifierHeartRateVariabilitySDNN',
        'HKQuantityTypeIdentifierRestingHeartRate',
        'HKQuantityTypeIdentifierBodyMass'
    ]:
        data.append({
            'Metric': r_type.replace('HKQuantityTypeIdentifier', ''),
            'Value': record.attrib.get('value'),
            'Start': record.attrib.get('startDate'),
            'End': record.attrib.get('endDate')
        })
    
    # Handle Sleep Stages and Duration
    elif r_type == 'HKCategoryTypeIdentifierSleepAnalysis':
        raw_val = record.attrib.get('value')
        # Map the numeric code to a readable stage name
        stage = sleep_lookup.get(raw_val, raw_val)
        
        data.append({
            'Metric': 'SleepAnalysis',
            'Value': stage,
            'Start': record.attrib.get('startDate'),
            'End': record.attrib.get('endDate')
        })

# 4. Save to CSV
df = pd.DataFrame(data)
df.to_csv('health_data_full.csv', index=False)
print("Done! Open 'health_data_full.csv' to see your data.")
