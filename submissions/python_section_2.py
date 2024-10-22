import pandas as pd
import numpy as np
from datetime import datetime, time

df = pd.read_csv("C:\\Users\\gande\\OneDrive\\Desktop\\Mapup\\MapUp-DA-Assessment-2024\\submissions\\dataset-2.csv")

# Question 1: Distance Matrix Calculation
def calculate_distance_matrix(df):
    locations = list(set(df['id_start'].unique()) | set(df['id_end'].unique()))
    distance_df = pd.DataFrame(index=locations, columns=locations)

    for _, row in df.iterrows():
        distance_df.at[row['id_start'], row['id_end']] = row['distance']

    distance_df = distance_df.fillna(0)
    distance_df = distance_df + distance_df.T
    np.fill_diagonal(distance_df.values, 0)
    return distance_df

distance_matrix = calculate_distance_matrix(df)
print("Distance Matrix:")
print(distance_matrix)


# Question 2: Unroll Distance Matrix
def unroll_distance_matrix(df):
    locations = df.index
    unrolled_data = []

    for start_loc in locations:
        for end_loc in locations:
            if start_loc != end_loc:
                unrolled_data.append({
                    'id_start': start_loc,
                    'id_end': end_loc,
                    'distance': df.at[start_loc, end_loc]
                })

    unrolled_df = pd.DataFrame(unrolled_data)
    return unrolled_df

unrolled_result = unroll_distance_matrix(distance_matrix)
print("\nUnrolled Distance Matrix:")
print(unrolled_result)

# Question 3: Finding IDs within Percentage Threshold
def find_ids_within_ten_percentage_threshold(df):
    all_results = []
    for reference_id in df['id_start'].unique():
        reference_df = df[df['id_start'] == reference_id]
        reference_avg_distance = reference_df['distance'].mean()
        threshold = 0.1 * reference_avg_distance

        result_df = df[
            (df['id_start'] != reference_id) &
            (df['distance'] >= (reference_avg_distance - threshold)) &
            (df['distance'] <= (reference_avg_distance + threshold))
        ]

        result_df = result_df.sort_values(by='id_start')
        all_results.append(result_df)

    return pd.concat(all_results, ignore_index=True)

result_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_result)
print("\nIDs within 10% Distance Threshold:")
print(result_within_threshold)


# Question 4: Calculate Toll Rate
def calculate_toll_rate(df):
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df

result_with_toll = calculate_toll_rate(result_within_threshold)
print("\nToll Rates for Each Vehicle Type:")
print(result_with_toll)


# Question 5: Calculate Time-Based Toll Rates
def calculate_time_based_toll_rates(df):
    required_columns = ['startDay', 'startTime', 'endDay', 'endTime', 'distance']

    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"Missing required column: {col}")

    time_ranges_weekday = [
        (time(0, 0), time(10, 0), 0.8),
        (time(10, 0), time(18, 0), 1.2),
        (time(18, 0), time(23, 59, 59), 0.8)
    ]

    time_ranges_weekend = [
        (time(0, 0), time(23, 59, 59), 0.7)
    ]

    day_mapping = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

    start_day_list, start_time_list, end_day_list, end_time_list, toll_rate_list = [], [], [], [], []

    for _, row in df.iterrows():
        start_datetime = pd.to_datetime(f"{row['startDay']} {row['startTime']}")
        end_datetime = pd.to_datetime(f"{row['endDay']} {row['endTime']}")

        day_index = start_datetime.weekday()
        start_day_name = day_mapping[day_index]
        end_day_name = day_mapping[(day_index + 1) % 7] 

        start_day_list.append(start_day_name)
        end_day_list.append(end_day_name)

        toll_rate = 0.0
        if day_index < 5: 
            for start_time, end_time, discount_factor in time_ranges_weekday:
                if start_datetime.time() >= start_time and start_datetime.time() < end_time:
                    toll_rate = row['distance'] * discount_factor
                    break
        else: 
            for start_time, end_time, discount_factor in time_ranges_weekend:
                if start_datetime.time() >= start_time and start_datetime.time() < end_time:
                    toll_rate = row['distance'] * discount_factor
                    break

        toll_rate_list.append(toll_rate)

        start_time_list.append(start_datetime.time())
        end_time_list.append(end_datetime.time())

    df['start_day'] = start_day_list
    df['start_time'] = start_time_list
    df['end_day'] = end_day_list
    df['end_time'] = end_time_list
    df['toll_rate'] = toll_rate_list 

    return df

result_with_toll['startDay'] = '2024-10-20'  
result_with_toll['startTime'] = '08:30:00'   
result_with_toll['endDay'] = '2024-10-20'     
result_with_toll['endTime'] = '09:30:00'  

result3 = calculate_time_based_toll_rates(result_with_toll)
print("\nTime Based Toll Rates:")
print(result3)


