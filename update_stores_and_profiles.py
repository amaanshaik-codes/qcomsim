"""
Update Store System and Regenerate Profiles
- Use the 57 dark stores from blinkit_darkstores_nodes.csv
- Add a master warehouse outside the city
- Update rider and picker profiles to use these stores
- Create warehouse-to-darkstore connections
"""

import pandas as pd
import numpy as np
import hashlib
import random
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)
random.seed(42)

print("="*70)
print("STORE SYSTEM UPDATE & PROFILE REGENERATION")
print("="*70)

# =============================================================================
# LOAD EXISTING DARK STORE DATA
# =============================================================================

nodes_df = pd.read_csv('blinkit_darkstores_nodes.csv')
edges_df = pd.read_csv('blinkit_darkstores_edges.csv')

print(f"\nLoaded {len(nodes_df)} dark store locations")
print(f"Loaded {len(edges_df)} store-to-store connections")

# =============================================================================
# CREATE MASTER WAREHOUSE (Outside city - Shamshabad near Airport)
# =============================================================================

MASTER_WAREHOUSE = {
    'Node_ID': 0,
    'Location': 'Shamshabad Master Warehouse',
    'Latitude': 17.2403,  # Near Hyderabad Airport
    'Longitude': 78.4294,
    'Zone': 'Master_Warehouse',
    'warehouse_type': 'CENTRAL_HUB',
    'capacity_sqft': 150000,
    'cold_storage_sqft': 25000,
    'loading_docks': 20,
    'daily_dispatch_capacity': 500000  # units
}

print(f"\nMaster Warehouse: {MASTER_WAREHOUSE['Location']}")
print(f"  Coordinates: {MASTER_WAREHOUSE['Latitude']}, {MASTER_WAREHOUSE['Longitude']}")

# =============================================================================
# CREATE UNIFIED STORE MASTER TABLE
# =============================================================================

# Generate store IDs for all dark stores
stores = []

# Add Master Warehouse first
stores.append({
    'store_id': 'HYD-MW-001',
    'node_id': 0,
    'store_name': 'Shamshabad Master Warehouse',
    'store_type': 'MASTER_WAREHOUSE',
    'location': 'Shamshabad',
    'zone': 'Master_Warehouse',
    'latitude': 17.2403,
    'longitude': 78.4294,
    'capacity_sqft': 150000,
    'cold_storage_sqft': 25000,
    'loading_docks': 20,
    'daily_order_capacity': 0,  # Doesn't fulfill orders directly
    'is_active': True,
    'opening_time': '00:00',
    'closing_time': '23:59',
    'operating_hours': 24,
})

# Add all dark stores from nodes
for _, row in nodes_df.iterrows():
    node_id = row['Node_ID']
    location = row['Location']
    zone = row['Zone']
    
    # Determine store capacity based on zone (IT hubs get larger stores)
    if zone in ['West', 'Northwest']:
        capacity = random.randint(3000, 5000)
        order_capacity = random.randint(800, 1200)
    elif zone in ['Central', 'Southwest']:
        capacity = random.randint(2500, 4000)
        order_capacity = random.randint(600, 1000)
    else:
        capacity = random.randint(2000, 3500)
        order_capacity = random.randint(400, 800)
    
    stores.append({
        'store_id': f'HYD-DS-{node_id:03d}',
        'node_id': node_id,
        'store_name': f'{location} Dark Store',
        'store_type': 'DARK_STORE',
        'location': location,
        'zone': zone,
        'latitude': row['Latitude'],
        'longitude': row['Longitude'],
        'capacity_sqft': capacity,
        'cold_storage_sqft': int(capacity * 0.15),
        'loading_docks': random.randint(2, 4),
        'daily_order_capacity': order_capacity,
        'is_active': True,
        'opening_time': '06:00',
        'closing_time': '00:00',
        'operating_hours': 18,
    })

stores_df = pd.DataFrame(stores)
stores_df.to_csv('blinkit_stores_master.csv', index=False)
print(f"\nCreated store master with {len(stores_df)} stores")
print(f"  - 1 Master Warehouse")
print(f"  - {len(stores_df)-1} Dark Stores")

# =============================================================================
# CREATE WAREHOUSE TO DARKSTORE CONNECTIONS
# =============================================================================

# Calculate distances from master warehouse to each dark store
def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in km between two coordinates"""
    R = 6371  # Earth's radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

warehouse_connections = []
mw_lat, mw_lon = MASTER_WAREHOUSE['Latitude'], MASTER_WAREHOUSE['Longitude']

for _, row in nodes_df.iterrows():
    distance = haversine_distance(mw_lat, mw_lon, row['Latitude'], row['Longitude'])
    
    # Estimate travel time (assuming avg 30 km/h for trucks in city traffic)
    travel_time_mins = (distance / 30) * 60
    
    warehouse_connections.append({
        'from_node_id': 0,
        'to_node_id': row['Node_ID'],
        'from_location': 'Shamshabad Master Warehouse',
        'to_location': row['Location'],
        'distance_km': round(distance, 2),
        'travel_time_mins': round(travel_time_mins, 0),
        'route_type': 'WAREHOUSE_TO_DARKSTORE',
        'from_zone': 'Master_Warehouse',
        'to_zone': row['Zone'],
    })

warehouse_edges_df = pd.DataFrame(warehouse_connections)
warehouse_edges_df.to_csv('blinkit_warehouse_connections.csv', index=False)
print(f"\nCreated {len(warehouse_edges_df)} warehouse-to-darkstore connections")
print(f"  Avg distance: {warehouse_edges_df['distance_km'].mean():.1f} km")
print(f"  Max distance: {warehouse_edges_df['distance_km'].max():.1f} km")
print(f"  Min distance: {warehouse_edges_df['distance_km'].min():.1f} km")

# =============================================================================
# NAME DATABASE FOR PROFILES
# =============================================================================

TELUGU_MALE_NAMES = ['Raju', 'Venkat', 'Srinivas', 'Ramesh', 'Suresh', 'Naresh', 'Mahesh', 'Ganesh',
    'Krishna', 'Ravi', 'Kiran', 'Anil', 'Sunil', 'Srinu', 'Balu', 'Mani',
    'Hari', 'Sai', 'Praveen', 'Naveen', 'Chandu', 'Ramu', 'Shiva', 'Naga',
    'Venu', 'Murali', 'Satish', 'Santosh', 'Rajesh', 'Dinesh', 'Manoj', 'Vijay',
    'Ajay', 'Sanjay', 'Kumar', 'Prasad', 'Mohan', 'Gopal', 'Ashok', 'Vinod',
    'Nagaraju', 'Tirupathi', 'Mallesh', 'Ramulu', 'Yellaiah', 'Nagesh', 'Srikanth',
    'Madhu', 'Phani', 'Vamsi', 'Teja', 'Pavan', 'Rakesh', 'Lokesh', 'Yogesh']

TELUGU_FEMALE_NAMES = ['Lakshmi', 'Padma', 'Swathi', 'Priya', 'Divya', 'Mounika', 'Anusha', 'Sravani',
    'Bhavana', 'Sowmya', 'Kavitha', 'Sunitha', 'Sirisha', 'Lavanya', 'Jyothi']

TELUGU_SURNAMES = ['Reddy', 'Naidu', 'Rao', 'Kumar', 'Goud', 'Yadav', 'Mudiraj', 'Munnuru',
    'Padmashali', 'Kamma', 'Velama', 'Kapu', 'Setty', 'Chetty', 'Nayak']

MUSLIM_MALE_NAMES = ['Mohammed', 'Ahmed', 'Abdul', 'Syed', 'Khalid', 'Imran', 'Farhan', 'Irfan',
    'Asif', 'Salman', 'Faisal', 'Rizwan', 'Shahid', 'Adnan', 'Waseem', 'Naseer',
    'Jameel', 'Kareem', 'Rashid', 'Anwar', 'Azhar', 'Bilal', 'Ismail', 'Junaid']

MUSLIM_FEMALE_NAMES = ['Fatima', 'Ayesha', 'Zainab', 'Sana', 'Nazia', 'Shabana', 'Rubina', 'Nasreen']

MUSLIM_SURNAMES = ['Khan', 'Syed', 'Pasha', 'Baig', 'Mirza', 'Qureshi', 'Shaikh', 'Ansari', 'Hussain', 'Ali']

NORTH_INDIAN_MALE_NAMES = ['Amit', 'Rahul', 'Rohit', 'Nitin', 'Gaurav', 'Varun', 'Akash', 'Sahil',
    'Karan', 'Pankaj', 'Sachin', 'Vikas', 'Deepak', 'Ravi', 'Sonu', 'Monu']

NORTH_INDIAN_FEMALE_NAMES = ['Priyanka', 'Neha', 'Nisha', 'Pooja', 'Riya', 'Simran', 'Ananya', 'Khushi']

NORTH_INDIAN_SURNAMES = ['Sharma', 'Verma', 'Gupta', 'Singh', 'Kumar', 'Yadav', 'Thakur', 'Chauhan']

# VEHICLE DATABASE
BIKE_MODELS = [('Hero Splendor Plus', 'BIKE', 100), ('Hero HF Deluxe', 'BIKE', 100), ('Bajaj Platina', 'BIKE', 100),
    ('Bajaj CT100', 'BIKE', 100), ('TVS Sport', 'BIKE', 110), ('Honda Shine', 'BIKE', 125), ('Bajaj Pulsar 125', 'BIKE', 125)]

SCOOTER_MODELS = [('Honda Activa 6G', 'SCOOTER', 110), ('TVS Jupiter', 'SCOOTER', 110), ('Hero Destini 125', 'SCOOTER', 125),
    ('Suzuki Access 125', 'SCOOTER', 125), ('Ola S1', 'ELECTRIC_SCOOTER', 0), ('Ather 450X', 'ELECTRIC_SCOOTER', 0)]

CYCLE_MODELS = [('Hero Sprint', 'CYCLE', 0), ('Hercules Roadsters', 'CYCLE', 0)]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_rider_id():
    return f"RDR-{hashlib.md5(str(random.random()).encode()).hexdigest()[:8].upper()}"

def generate_picker_id():
    return f"PKR-{hashlib.md5(str(random.random()).encode()).hexdigest()[:8].upper()}"

def generate_phone():
    prefixes = ['98', '97', '96', '95', '94', '93', '91', '90', '89', '88', '87', '86', '85', '84', '83', '82', '81', '80', '79', '78', '77', '76', '75', '74', '73', '72', '71', '70']
    return f"+91{random.choice(prefixes)}{random.randint(10000000, 99999999)}"

def generate_email(first_name, last_name, birth_year):
    domains = ['gmail.com', 'gmail.com', 'gmail.com', 'yahoo.com', 'rediffmail.com']
    patterns = [f"{first_name.lower()}{random.randint(1, 999)}", f"{first_name.lower()}.{last_name.lower()}", f"{first_name.lower()}{str(birth_year)[-2:]}"]
    return f"{random.choice(patterns)}@{random.choice(domains)}"

def get_name(gender, community):
    if community == 'telugu':
        return (random.choice(TELUGU_MALE_NAMES), random.choice(TELUGU_SURNAMES)) if gender == 'M' else (random.choice(TELUGU_FEMALE_NAMES), random.choice(TELUGU_SURNAMES))
    elif community == 'muslim':
        return (random.choice(MUSLIM_MALE_NAMES), random.choice(MUSLIM_SURNAMES)) if gender == 'M' else (random.choice(MUSLIM_FEMALE_NAMES), random.choice(MUSLIM_SURNAMES))
    else:
        return (random.choice(NORTH_INDIAN_MALE_NAMES), random.choice(NORTH_INDIAN_SURNAMES)) if gender == 'M' else (random.choice(NORTH_INDIAN_FEMALE_NAMES), random.choice(NORTH_INDIAN_SURNAMES))

def generate_vehicle_number(vehicle_type):
    districts = ['09', '10', '11', '12', '13', '14', '07', '08']
    letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    if vehicle_type == 'CYCLE':
        return 'N/A'
    return f"TS{random.choice(districts)}{random.choice(letters)}{random.choice(letters)}{random.randint(1000, 9999)}"

def get_vehicle(vehicle_distribution):
    vehicle_type = random.choices(list(vehicle_distribution.keys()), weights=list(vehicle_distribution.values()))[0]
    if vehicle_type == 'BIKE':
        model, vtype, cc = random.choice(BIKE_MODELS)
    elif vehicle_type in ['SCOOTER', 'ELECTRIC_SCOOTER']:
        if vehicle_type == 'ELECTRIC_SCOOTER':
            model, vtype, cc = random.choice([m for m in SCOOTER_MODELS if m[1] == 'ELECTRIC_SCOOTER'])
        else:
            model, vtype, cc = random.choice([m for m in SCOOTER_MODELS if m[1] == 'SCOOTER'])
    else:
        model, vtype, cc = random.choice(CYCLE_MODELS)
    return model, vtype, cc

def generate_shift_times(shift_type):
    if shift_type == 'FULL_TIME':
        shifts = [('06:00', '14:00'), ('07:00', '15:00'), ('10:00', '18:00'), ('12:00', '20:00'), ('14:00', '22:00'), ('16:00', '00:00')]
    elif shift_type == 'PART_TIME':
        shifts = [('06:00', '10:00'), ('10:00', '14:00'), ('14:00', '18:00'), ('18:00', '22:00'), ('19:00', '23:00'), ('20:00', '00:00')]
    else:
        shifts = [('09:00', '13:00'), ('10:00', '14:00'), ('14:00', '18:00')]
    return random.choice(shifts)

# =============================================================================
# DARK STORES LIST (from nodes, excluding master warehouse)
# =============================================================================

DARK_STORES = []
for _, row in nodes_df.iterrows():
    DARK_STORES.append({
        'store_id': f"HYD-DS-{row['Node_ID']:03d}",
        'node_id': row['Node_ID'],
        'name': f"{row['Location']} Dark Store",
        'location': row['Location'],
        'zone': row['Zone'],
        'lat': row['Latitude'],
        'lng': row['Longitude'],
    })

print(f"\nUsing {len(DARK_STORES)} dark stores for profiles")

# =============================================================================
# RIDER SEGMENTS - 97-99% MALE
# =============================================================================

RIDER_SEGMENTS = {
    'FULL_TIME_EXPERIENCED': {
        'experience_months_range': (18, 60), 'age_range': (22, 40), 'gender_ratio': 0.98,
        'vehicle_distribution': {'BIKE': 0.70, 'SCOOTER': 0.25, 'ELECTRIC_SCOOTER': 0.05},
        'on_time_rate_range': (0.88, 0.98), 'acceptance_rate_range': (0.85, 0.98),
        'cancellation_rate_range': (0.01, 0.05), 'avg_delivery_time_range': (8, 14),
        'daily_orders_range': (25, 45), 'earnings_per_order_range': (25, 40),
        'rating_range': (4.4, 4.9), 'weight': 0.25, 'shift_type': 'FULL_TIME',
    },
    'FULL_TIME_REGULAR': {
        'experience_months_range': (6, 24), 'age_range': (20, 35), 'gender_ratio': 0.98,
        'vehicle_distribution': {'BIKE': 0.65, 'SCOOTER': 0.30, 'ELECTRIC_SCOOTER': 0.05},
        'on_time_rate_range': (0.82, 0.94), 'acceptance_rate_range': (0.80, 0.94),
        'cancellation_rate_range': (0.03, 0.10), 'avg_delivery_time_range': (10, 16),
        'daily_orders_range': (20, 35), 'earnings_per_order_range': (22, 35),
        'rating_range': (4.2, 4.7), 'weight': 0.30, 'shift_type': 'FULL_TIME',
    },
    'PART_TIME_STUDENT': {
        'experience_months_range': (1, 12), 'age_range': (18, 25), 'gender_ratio': 0.97,
        'vehicle_distribution': {'BIKE': 0.40, 'SCOOTER': 0.45, 'CYCLE': 0.10, 'ELECTRIC_SCOOTER': 0.05},
        'on_time_rate_range': (0.75, 0.90), 'acceptance_rate_range': (0.70, 0.88),
        'cancellation_rate_range': (0.05, 0.15), 'avg_delivery_time_range': (12, 20),
        'daily_orders_range': (8, 18), 'earnings_per_order_range': (20, 30),
        'rating_range': (4.0, 4.5), 'weight': 0.20, 'shift_type': 'PART_TIME',
    },
    'PART_TIME_EVENING': {
        'experience_months_range': (2, 18), 'age_range': (22, 45), 'gender_ratio': 0.98,
        'vehicle_distribution': {'BIKE': 0.55, 'SCOOTER': 0.40, 'ELECTRIC_SCOOTER': 0.05},
        'on_time_rate_range': (0.78, 0.92), 'acceptance_rate_range': (0.75, 0.90),
        'cancellation_rate_range': (0.04, 0.12), 'avg_delivery_time_range': (11, 18),
        'daily_orders_range': (10, 22), 'earnings_per_order_range': (22, 32),
        'rating_range': (4.1, 4.6), 'weight': 0.15, 'shift_type': 'PART_TIME',
    },
    'NEW_JOINER': {
        'experience_months_range': (0, 3), 'age_range': (18, 30), 'gender_ratio': 0.97,
        'vehicle_distribution': {'BIKE': 0.50, 'SCOOTER': 0.40, 'CYCLE': 0.08, 'ELECTRIC_SCOOTER': 0.02},
        'on_time_rate_range': (0.65, 0.82), 'acceptance_rate_range': (0.65, 0.85),
        'cancellation_rate_range': (0.08, 0.20), 'avg_delivery_time_range': (15, 25),
        'daily_orders_range': (5, 15), 'earnings_per_order_range': (18, 28),
        'rating_range': (3.8, 4.3), 'weight': 0.10, 'shift_type': 'FULL_TIME',
    },
}

# =============================================================================
# PICKER SEGMENTS - 97-99% MALE
# =============================================================================

PICKER_SEGMENTS = {
    'FULL_TIME_SENIOR': {
        'experience_months_range': (12, 48), 'age_range': (22, 40), 'gender_ratio': 0.98,
        'avg_pick_time_range': (8, 15), 'daily_orders_range': (80, 150),
        'accuracy_rate_range': (0.985, 0.999), 'items_per_hour_range': (150, 280),
        'hourly_rate': (50, 70), 'shift_type': 'FULL_TIME', 'weight': 0.20,
    },
    'FULL_TIME_REGULAR': {
        'experience_months_range': (3, 18), 'age_range': (20, 35), 'gender_ratio': 0.98,
        'avg_pick_time_range': (12, 22), 'daily_orders_range': (60, 120),
        'accuracy_rate_range': (0.970, 0.995), 'items_per_hour_range': (100, 200),
        'hourly_rate': (45, 60), 'shift_type': 'FULL_TIME', 'weight': 0.25,
    },
    'PART_TIME_STUDENT': {
        'experience_months_range': (1, 12), 'age_range': (18, 25), 'gender_ratio': 0.97,
        'avg_pick_time_range': (15, 30), 'daily_orders_range': (30, 70),
        'accuracy_rate_range': (0.950, 0.988), 'items_per_hour_range': (70, 150),
        'hourly_rate': (40, 55), 'shift_type': 'PART_TIME', 'weight': 0.30,
    },
    'PART_TIME_EVENING': {
        'experience_months_range': (2, 24), 'age_range': (25, 45), 'gender_ratio': 0.98,
        'avg_pick_time_range': (14, 25), 'daily_orders_range': (40, 80),
        'accuracy_rate_range': (0.975, 0.996), 'items_per_hour_range': (80, 160),
        'hourly_rate': (42, 58), 'shift_type': 'PART_TIME', 'weight': 0.15,
    },
    'NEW_JOINER': {
        'experience_months_range': (0, 2), 'age_range': (18, 30), 'gender_ratio': 0.97,
        'avg_pick_time_range': (25, 45), 'daily_orders_range': (20, 50),
        'accuracy_rate_range': (0.920, 0.970), 'items_per_hour_range': (40, 100),
        'hourly_rate': (38, 50), 'shift_type': 'TRAINING', 'weight': 0.10,
    },
}

# =============================================================================
# GENERATE RIDERS (~150 per store)
# =============================================================================

NUM_RIDERS = len(DARK_STORES) * 150  # ~8550 riders
print(f"\n{'='*70}")
print(f"GENERATING {NUM_RIDERS:,} RIDER PROFILES")
print(f"{'='*70}")

total_weight = sum(s['weight'] for s in RIDER_SEGMENTS.values())
rider_segment_counts = {name: int(NUM_RIDERS * seg['weight'] / total_weight) for name, seg in RIDER_SEGMENTS.items()}
diff = NUM_RIDERS - sum(rider_segment_counts.values())
rider_segment_counts['FULL_TIME_REGULAR'] += diff

riders = []
for segment_name, segment in RIDER_SEGMENTS.items():
    count = rider_segment_counts[segment_name]
    print(f"  Generating {segment_name}: {count} riders...")
    
    for _ in range(count):
        gender = 'M' if random.random() < segment['gender_ratio'] else 'F'
        age = random.randint(*segment['age_range'])
        birth_year = 2024 - age
        community = random.choices(['telugu', 'muslim', 'north'], weights=[0.55, 0.30, 0.15])[0]
        first_name, last_name = get_name(gender, community)
        experience_months = random.randint(*segment['experience_months_range'])
        join_date = datetime(2024, 12, 1) - timedelta(days=experience_months * 30)
        vehicle_model, vehicle_type, engine_cc = get_vehicle(segment['vehicle_distribution'])
        vehicle_number = generate_vehicle_number(vehicle_type)
        home_store = random.choice(DARK_STORES)
        shift_start, shift_end = generate_shift_times(segment['shift_type'])
        on_time_rate = round(random.uniform(*segment['on_time_rate_range']), 3)
        acceptance_rate = round(random.uniform(*segment['acceptance_rate_range']), 3)
        cancellation_rate = round(random.uniform(*segment['cancellation_rate_range']), 3)
        avg_delivery_time = round(random.uniform(*segment['avg_delivery_time_range']), 1)
        daily_orders = random.randint(*segment['daily_orders_range'])
        rating = round(random.uniform(*segment['rating_range']), 2)
        earnings_per_order = random.uniform(*segment['earnings_per_order_range'])
        days_worked = int(experience_months * 22 * random.uniform(0.7, 0.95))
        total_orders = int(days_worked * daily_orders * random.uniform(0.8, 1.1))
        total_earnings = int(total_orders * earnings_per_order)
        
        if experience_months < 1: status = 'TRAINING'
        elif cancellation_rate > 0.15 or on_time_rate < 0.70: status = 'PROBATION'
        elif on_time_rate > 0.92 and rating > 4.5: status = 'STAR_PERFORMER'
        else: status = 'ACTIVE'
        
        last_active = datetime(2024, 12, 4) - timedelta(hours=random.randint(0, 48)) if status in ['ACTIVE', 'STAR_PERFORMER'] else datetime(2024, 12, 4) - timedelta(days=random.randint(0, 7))
        
        riders.append({
            'rider_id': generate_rider_id(),
            'first_name': first_name,
            'last_name': last_name,
            'full_name': f"{first_name} {last_name}",
            'gender': gender,
            'age': age,
            'phone_number': generate_phone(),
            'email': generate_email(first_name, last_name, birth_year),
            'community': community.upper(),
            'vehicle_type': vehicle_type,
            'vehicle_model': vehicle_model,
            'vehicle_number': vehicle_number,
            'engine_cc': engine_cc,
            'home_store_id': home_store['store_id'],
            'home_store_node_id': home_store['node_id'],
            'home_store_name': home_store['name'],
            'service_zone': home_store['zone'],
            'store_location': home_store['location'],
            'home_lat': round(home_store['lat'] + random.uniform(-0.01, 0.01), 6),
            'home_lng': round(home_store['lng'] + random.uniform(-0.01, 0.01), 6),
            'rider_segment': segment_name,
            'shift_type': segment['shift_type'],
            'shift_start': shift_start,
            'shift_end': shift_end,
            'experience_months': experience_months,
            'join_date': join_date.strftime('%Y-%m-%d'),
            'status': status,
            'last_active': last_active.strftime('%Y-%m-%d %H:%M'),
            'on_time_delivery_rate': on_time_rate,
            'order_acceptance_rate': acceptance_rate,
            'cancellation_rate': cancellation_rate,
            'avg_delivery_time_mins': avg_delivery_time,
            'customer_rating': rating,
            'total_orders_delivered': total_orders,
            'daily_avg_orders': daily_orders,
            'total_earnings': total_earnings,
            'avg_earnings_per_order': round(earnings_per_order, 2),
            'peak_hour_preference': random.choice(['MORNING', 'AFTERNOON', 'EVENING', 'NIGHT']),
            'weekend_availability': random.choice([True, True, True, False]),
            'has_insulated_bag': random.choice([True, True, True, True, False]),
            'has_rain_gear': random.choice([True, True, False]),
            'knows_english': random.choice([True, True, False, False, False]),
            'knows_hindi': True,
            'knows_telugu': community == 'telugu' or random.random() < 0.6,
        })

riders_df = pd.DataFrame(riders)
riders_df = riders_df.sample(frac=1, random_state=42).reset_index(drop=True)
riders_df.to_csv('rider_profiles_new.csv', index=False)
print(f"\nSaved {len(riders_df):,} riders to rider_profiles_new.csv")

# =============================================================================
# GENERATE PICKERS (~80 per store)
# =============================================================================

NUM_PICKERS = len(DARK_STORES) * 80  # ~4560 pickers
print(f"\n{'='*70}")
print(f"GENERATING {NUM_PICKERS:,} PICKER PROFILES")
print(f"{'='*70}")

total_weight = sum(s['weight'] for s in PICKER_SEGMENTS.values())
picker_segment_counts = {name: int(NUM_PICKERS * seg['weight'] / total_weight) for name, seg in PICKER_SEGMENTS.items()}
diff = NUM_PICKERS - sum(picker_segment_counts.values())
picker_segment_counts['PART_TIME_STUDENT'] += diff

pickers = []
for segment_name, segment in PICKER_SEGMENTS.items():
    count = picker_segment_counts[segment_name]
    print(f"  Generating {segment_name}: {count} pickers...")
    
    for _ in range(count):
        gender = 'M' if random.random() < segment['gender_ratio'] else 'F'
        age = random.randint(*segment['age_range'])
        birth_year = 2024 - age
        community = random.choices(['telugu', 'muslim', 'north'], weights=[0.55, 0.30, 0.15])[0]
        first_name, last_name = get_name(gender, community)
        experience_months = random.randint(*segment['experience_months_range'])
        join_date = datetime(2024, 12, 1) - timedelta(days=experience_months * 30)
        assigned_store = random.choice(DARK_STORES)
        shift_start, shift_end = generate_shift_times(segment['shift_type'])
        
        if experience_months >= 18 and segment_name == 'FULL_TIME_SENIOR':
            role = random.choice(['SENIOR_PICKER', 'TEAM_LEAD', 'QUALITY_CHECKER'])
        elif experience_months >= 6: role = 'PICKER'
        else: role = 'TRAINEE_PICKER'
        
        avg_pick_time = round(random.uniform(*segment['avg_pick_time_range']), 1)
        daily_orders = random.randint(*segment['daily_orders_range'])
        accuracy_rate = round(random.uniform(*segment['accuracy_rate_range']), 4)
        items_per_hour = random.randint(*segment['items_per_hour_range'])
        days_worked = int(experience_months * 22 * random.uniform(0.7, 0.95))
        total_orders = int(days_worked * daily_orders * random.uniform(0.8, 1.1))
        avg_items_per_order = random.randint(4, 12)
        total_items_picked = total_orders * avg_items_per_order
        mispick_rate = round(1 - accuracy_rate, 4)
        total_mispicks = int(total_items_picked * mispick_rate)
        hourly_rate = random.uniform(*segment['hourly_rate'])
        hours_per_day = 8 if segment['shift_type'] == 'FULL_TIME' else 4
        total_hours = days_worked * hours_per_day
        total_earnings = int(total_hours * hourly_rate)
        
        if experience_months < 1: status = 'TRAINING'
        elif accuracy_rate < 0.94: status = 'PROBATION'
        elif accuracy_rate > 0.995 and items_per_hour > 200: status = 'STAR_PERFORMER'
        else: status = 'ACTIVE'
        
        last_active = datetime(2024, 12, 4) - timedelta(hours=random.randint(0, 72))
        
        pickers.append({
            'picker_id': generate_picker_id(),
            'first_name': first_name,
            'last_name': last_name,
            'full_name': f"{first_name} {last_name}",
            'gender': gender,
            'age': age,
            'phone_number': generate_phone(),
            'email': generate_email(first_name, last_name, birth_year),
            'community': community.upper(),
            'store_id': assigned_store['store_id'],
            'store_node_id': assigned_store['node_id'],
            'store_name': assigned_store['name'],
            'store_location': assigned_store['location'],
            'service_zone': assigned_store['zone'],
            'picker_segment': segment_name,
            'role': role,
            'shift_type': segment['shift_type'],
            'shift_start': shift_start,
            'shift_end': shift_end,
            'experience_months': experience_months,
            'join_date': join_date.strftime('%Y-%m-%d'),
            'status': status,
            'last_active': last_active.strftime('%Y-%m-%d %H:%M'),
            'avg_picking_time_sec': avg_pick_time,
            'items_per_hour': items_per_hour,
            'daily_orders_picked': daily_orders,
            'accuracy_rate': accuracy_rate,
            'mispick_rate': mispick_rate,
            'total_orders_picked': total_orders,
            'total_items_picked': total_items_picked,
            'total_mispicks': total_mispicks,
            'hourly_rate': round(hourly_rate, 2),
            'total_earnings': total_earnings,
            'total_hours_worked': int(total_hours),
            'zone_familiarity': round(random.uniform(0.6, 0.99) if experience_months > 3 else random.uniform(0.3, 0.7), 2),
            'multitask_ability': random.choice(['LOW', 'MEDIUM', 'HIGH']),
            'physical_fitness': random.choice(['AVERAGE', 'GOOD', 'EXCELLENT']),
            'temperature_zone_trained': random.choice([True, True, True, False]),
            'fragile_handling_certified': random.choice([True, True, False]),
        })

pickers_df = pd.DataFrame(pickers)
pickers_df = pickers_df.sample(frac=1, random_state=42).reset_index(drop=True)
pickers_df.to_csv('picker_profiles_new.csv', index=False)
print(f"\nSaved {len(pickers_df):,} pickers to picker_profiles_new.csv")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "="*70)
print("SUMMARY")
print("="*70)

print("\n--- STORE SYSTEM ---")
print(f"Master Warehouse: 1 (Shamshabad)")
print(f"Dark Stores: {len(DARK_STORES)}")
print(f"Warehouse Connections: {len(warehouse_edges_df)}")
print(f"Store-to-Store Edges: {len(edges_df)}")

print("\n--- RIDERS ---")
print(f"Total: {len(riders_df):,}")
print(f"Male: {len(riders_df[riders_df['gender']=='M']):,} ({len(riders_df[riders_df['gender']=='M'])/len(riders_df)*100:.1f}%)")
print(f"Female: {len(riders_df[riders_df['gender']=='F']):,} ({len(riders_df[riders_df['gender']=='F'])/len(riders_df)*100:.1f}%)")
print(f"Per Store (avg): {len(riders_df)/len(DARK_STORES):.0f}")

print("\n--- PICKERS ---")
print(f"Total: {len(pickers_df):,}")
print(f"Male: {len(pickers_df[pickers_df['gender']=='M']):,} ({len(pickers_df[pickers_df['gender']=='M'])/len(pickers_df)*100:.1f}%)")
print(f"Female: {len(pickers_df[pickers_df['gender']=='F']):,} ({len(pickers_df[pickers_df['gender']=='F'])/len(pickers_df)*100:.1f}%)")
print(f"Per Store (avg): {len(pickers_df)/len(DARK_STORES):.0f}")

# Verify store alignment
print("\n--- STORE ALIGNMENT CHECK ---")
rider_stores = set(riders_df['home_store_id'].unique())
picker_stores = set(pickers_df['store_id'].unique())
node_stores = set([f"HYD-DS-{n:03d}" for n in nodes_df['Node_ID']])

print(f"Stores in rider profiles: {len(rider_stores)}")
print(f"Stores in picker profiles: {len(picker_stores)}")
print(f"Stores in dark store nodes: {len(node_stores)}")
print(f"All aligned: {rider_stores == picker_stores == node_stores}")

print("="*70)
print("FILES CREATED/UPDATED:")
print("  - blinkit_stores_master.csv (new)")
print("  - blinkit_warehouse_connections.csv (new)")
print("  - rider_profiles_new.csv (updated)")
print("  - picker_profiles_new.csv (updated)")
print("="*70)
