"""
Hyderabad-Specific Customer Profile Generator for Blinkit Simulation
Based on real market research data
Target: 1.5 million customers
Outputs: customer_profiles.csv
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
print("HYDERABAD BLINKIT CUSTOMER PROFILE GENERATOR")
print("Target: 1.5 Million Users")
print("="*70)

# =============================================================================
# HYDERABAD-SPECIFIC NAME DATABASE
# =============================================================================

# Telugu Names (majority - ~60%)
TELUGU_MALE_NAMES = [
    'Venkat', 'Srinivas', 'Ravi', 'Krishna', 'Naresh', 'Suresh', 'Ramesh', 'Mahesh',
    'Rajesh', 'Ganesh', 'Sai', 'Karthik', 'Arun', 'Vijay', 'Prasad', 'Chandra',
    'Harsha', 'Pavan', 'Srikanth', 'Vamsi', 'Naveen', 'Anil', 'Kumar', 'Raju',
    'Srinath', 'Murali', 'Sekhar', 'Mohan', 'Hari', 'Satish', 'Praveen', 'Ashok',
    'Sunil', 'Ramana', 'Kishore', 'Gopal', 'Bhanu', 'Phani', 'Naga', 'Siva',
    'Vinay', 'Rakesh', 'Dinesh', 'Manoj', 'Sudheer', 'Jagadish', 'Nagaraj', 'Shiva',
    'Teja', 'Vishal', 'Rohit', 'Nikhil', 'Akhil', 'Rahul', 'Aditya', 'Abhi',
    'Varun', 'Tarun', 'Arjun', 'Pranav', 'Siddharth', 'Kiran', 'Ajay', 'Surya',
    'Chaitanya', 'Kalyan', 'Sandeep', 'Pradeep', 'Deepak', 'Sanjay', 'Ranganath',
    'Balaji', 'Venu', 'Madhav', 'Raghav', 'Shankar', 'Ranga', 'Nagendra', 'Rambabu'
]

TELUGU_FEMALE_NAMES = [
    'Lakshmi', 'Padma', 'Swathi', 'Priya', 'Divya', 'Keerthi', 'Mounika', 'Sahithi',
    'Anusha', 'Lavanya', 'Sravani', 'Bhavana', 'Sowmya', 'Kavitha', 'Sunitha', 'Sirisha',
    'Radhika', 'Pallavi', 'Sravya', 'Harika', 'Manasa', 'Varsha', 'Pranathi', 'Tejaswi',
    'Vaishnavi', 'Nandini', 'Chandana', 'Sushma', 'Rekha', 'Padmaja', 'Jyothi', 'Aruna',
    'Ramya', 'Sindhu', 'Madhavi', 'Vijaya', 'Anitha', 'Shravya', 'Sridevi', 'Vasantha',
    'Tulasi', 'Saritha', 'Rajani', 'Surekha', 'Usha', 'Lalitha', 'Kalyani', 'Bhavani',
    'Spandana', 'Meghana', 'Niharika', 'Deepthi', 'Shruthi', 'Sneha', 'Pooja', 'Nikitha',
    'Shalini', 'Amrutha', 'Haritha', 'Navya', 'Akshitha', 'Teja', 'Sahaja', 'Vyshnavi'
]

TELUGU_SURNAMES = [
    'Reddy', 'Rao', 'Naidu', 'Sharma', 'Kumar', 'Chowdary', 'Varma', 'Raju',
    'Prasad', 'Murthy', 'Sastry', 'Goud', 'Kamma', 'Velama', 'Kapu', 'Setty',
    'Chetty', 'Pillai', 'Nayak', 'Babu', 'Swamy', 'Gupta', 'Agarwal', 'Jain',
    'Patel', 'Shetty', 'Kulkarni', 'Deshmukh', 'Patil', 'Iyer', 'Iyengar',
    'Venkatesh', 'Subramanyam', 'Raghunath', 'Srinivasan', 'Krishnamurthy',
    'Ramachandran', 'Narasimha', 'Venkata', 'Gopala', 'Anjaneyulu', 'Mallikarjun'
]

# Muslim Names (significant in Hyderabad - ~20%)
MUSLIM_MALE_NAMES = [
    'Mohammed', 'Ahmed', 'Abdul', 'Syed', 'Khalid', 'Imran', 'Farhan', 'Irfan',
    'Asif', 'Salman', 'Faisal', 'Rizwan', 'Zaheer', 'Shahid', 'Adnan', 'Arshad',
    'Waseem', 'Naseer', 'Jameel', 'Kareem', 'Rashid', 'Hameed', 'Anwar', 'Azhar',
    'Bilal', 'Danish', 'Feroz', 'Ghouse', 'Hafeez', 'Ismail', 'Junaid', 'Kashif',
    'Liaqat', 'Mazhar', 'Nadeem', 'Omar', 'Pasha', 'Qasim', 'Riyaz', 'Sameer',
    'Tanveer', 'Usman', 'Waqar', 'Yasir', 'Zubair', 'Aamir', 'Basit', 'Fahad',
    'Hasan', 'Ibrahim', 'Javeed', 'Kaleem', 'Mubeen', 'Noman', 'Owais', 'Rafiq'
]

MUSLIM_FEMALE_NAMES = [
    'Fatima', 'Ayesha', 'Zainab', 'Sana', 'Sara', 'Nazia', 'Shabana', 'Rubina',
    'Nasreen', 'Salma', 'Amina', 'Khadija', 'Mariam', 'Noor', 'Hina', 'Saba',
    'Tabassum', 'Uzma', 'Yasmeen', 'Zahida', 'Asma', 'Bushra', 'Dilshad', 'Farha',
    'Gulshan', 'Humera', 'Ishrat', 'Javeria', 'Khalida', 'Lubna', 'Mumtaz', 'Nafisa',
    'Parveen', 'Qamar', 'Reshma', 'Shagufta', 'Tahira', 'Waheeda', 'Zeba', 'Aliya',
    'Mehreen', 'Sameena', 'Afreen', 'Nahid', 'Rukhsar', 'Shabnam', 'Zara', 'Iqra'
]

MUSLIM_SURNAMES = [
    'Khan', 'Syed', 'Pasha', 'Baig', 'Mirza', 'Qureshi', 'Shaikh', 'Ansari',
    'Hashmi', 'Jafri', 'Kazmi', 'Naqvi', 'Rizvi', 'Siddiqui', 'Hussain', 'Ali',
    'Ahmed', 'Mohammed', 'Begum', 'Sultana', 'Khatoon', 'Fatima', 'Mohiuddin',
    'Salahuddin', 'Nizamuddin', 'Shamsuddin', 'Karimuddin', 'Habibuddin'
]

# North Indian Names (migrants - ~15%)
NORTH_INDIAN_MALE_NAMES = [
    'Amit', 'Rahul', 'Vikram', 'Rohit', 'Nitin', 'Gaurav', 'Kunal', 'Varun',
    'Akash', 'Harsh', 'Mayank', 'Rishabh', 'Sahil', 'Karan', 'Neeraj', 'Pankaj',
    'Rajat', 'Sachin', 'Tushar', 'Utkarsh', 'Vikas', 'Yash', 'Abhishek', 'Dhruv',
    'Ankit', 'Mohit', 'Tarun', 'Vivek', 'Aakash', 'Deepak', 'Himanshu', 'Kapil',
    'Lokesh', 'Manish', 'Nikhil', 'Om', 'Prashant', 'Ravi', 'Saurabh', 'Tanmay'
]

NORTH_INDIAN_FEMALE_NAMES = [
    'Priyanka', 'Neha', 'Nisha', 'Pooja', 'Riya', 'Simran', 'Tanvi', 'Ananya',
    'Bhavya', 'Charu', 'Diksha', 'Ekta', 'Garima', 'Ishika', 'Jhanvi', 'Khushi',
    'Mansi', 'Nidhi', 'Pallavi', 'Richa', 'Sakshi', 'Tanya', 'Urvashi', 'Vani',
    'Shreya', 'Megha', 'Komal', 'Kavya', 'Aishwarya', 'Disha', 'Kritika', 'Muskan'
]

NORTH_INDIAN_SURNAMES = [
    'Sharma', 'Verma', 'Gupta', 'Singh', 'Kumar', 'Agarwal', 'Jain', 'Bansal',
    'Mittal', 'Goel', 'Kapoor', 'Khanna', 'Malhotra', 'Chopra', 'Arora', 'Sethi',
    'Bhatia', 'Tandon', 'Saxena', 'Srivastava', 'Mathur', 'Dubey', 'Pandey', 'Tiwari',
    'Mishra', 'Shukla', 'Yadav', 'Chauhan', 'Thakur', 'Rathore', 'Rajput', 'Chaudhary'
]

# Christian Names (small but notable - ~5%)
CHRISTIAN_MALE_NAMES = [
    'John', 'David', 'Michael', 'Daniel', 'Joseph', 'Samuel', 'Thomas', 'Peter',
    'Paul', 'James', 'Robert', 'William', 'Charles', 'George', 'Edward', 'Francis',
    'Anthony', 'Andrew', 'Philip', 'Stephen', 'Christopher', 'Matthew', 'Mark', 'Luke',
    'Benjamin', 'Joshua', 'Timothy', 'Kevin', 'Brian', 'Patrick', 'Dennis', 'Ronald',
    'Vincent', 'Lawrence', 'Raymond', 'Gerald', 'Victor', 'Emmanuel', 'Dominic', 'Adrian'
]

CHRISTIAN_FEMALE_NAMES = [
    'Mary', 'Elizabeth', 'Sarah', 'Grace', 'Ruth', 'Rebecca', 'Rachel', 'Hannah',
    'Esther', 'Martha', 'Lydia', 'Priscilla', 'Miriam', 'Deborah', 'Naomi', 'Abigail',
    'Jennifer', 'Jessica', 'Michelle', 'Christina', 'Angela', 'Patricia', 'Catherine',
    'Margaret', 'Dorothy', 'Helen', 'Caroline', 'Jacqueline', 'Victoria', 'Stephanie',
    'Sharon', 'Susan', 'Linda', 'Lisa', 'Nancy', 'Betty', 'Sandra', 'Ashley', 'Emily'
]

CHRISTIAN_SURNAMES = [
    'Fernandes', 'Dsouza', 'Rodrigues', 'Pereira', 'Gomes', 'Lobo', 'Pinto', 'Mendes',
    'Sequeira', 'Mascarenhas', 'Miranda', 'Almeida', 'Dias', 'Costa', 'Noronha',
    'Williams', 'Johnson', 'Brown', 'Smith', 'Jones', 'David', 'Thomas', 'Philip',
    'Alexander', 'Daniel', 'Samuel', 'George', 'Joseph', 'James', 'Wilson', 'Martin'
]

# =============================================================================
# HYDERABAD LOCALITIES
# =============================================================================

HYDERABAD_AREAS = {
    'PREMIUM': [
        ('Jubilee Hills', 17.4325, 78.4072, 'HIGH'),
        ('Banjara Hills', 17.4156, 78.4347, 'HIGH'),
        ('Madhapur', 17.4486, 78.3908, 'UPPER_MIDDLE'),
        ('Gachibowli', 17.4401, 78.3489, 'UPPER_MIDDLE'),
        ('Kondapur', 17.4574, 78.3574, 'UPPER_MIDDLE'),
        ('Manikonda', 17.4043, 78.3835, 'UPPER_MIDDLE'),
        ('Hitech City', 17.4435, 78.3772, 'UPPER_MIDDLE'),
        ('Financial District', 17.4213, 78.3411, 'HIGH'),
        ('Kokapet', 17.4046, 78.3268, 'HIGH'),
        ('Narsingi', 17.3892, 78.3569, 'UPPER_MIDDLE'),
    ],
    'UPPER_MIDDLE': [
        ('Ameerpet', 17.4375, 78.4483, 'MIDDLE'),
        ('SR Nagar', 17.4401, 78.4516, 'MIDDLE'),
        ('Punjagutta', 17.4285, 78.4513, 'UPPER_MIDDLE'),
        ('Somajiguda', 17.4275, 78.4574, 'UPPER_MIDDLE'),
        ('Begumpet', 17.4436, 78.4671, 'UPPER_MIDDLE'),
        ('Secunderabad', 17.4399, 78.4983, 'MIDDLE'),
        ('Kukatpally', 17.4849, 78.4138, 'MIDDLE'),
        ('KPHB', 17.4947, 78.3996, 'UPPER_MIDDLE'),
        ('Miyapur', 17.4937, 78.3540, 'MIDDLE'),
        ('Chandanagar', 17.4963, 78.3269, 'MIDDLE'),
        ('Lingampally', 17.4916, 78.3175, 'MIDDLE'),
        ('Bachupally', 17.5457, 78.3819, 'MIDDLE'),
        ('Nizampet', 17.5183, 78.3871, 'MIDDLE'),
        ('Pragathi Nagar', 17.5012, 78.4012, 'MIDDLE'),
    ],
    'MIDDLE': [
        ('Dilsukhnagar', 17.3688, 78.5247, 'LOWER_MIDDLE'),
        ('LB Nagar', 17.3499, 78.5479, 'MIDDLE'),
        ('Kothapet', 17.3623, 78.5185, 'LOWER_MIDDLE'),
        ('Nagole', 17.3939, 78.5581, 'LOWER_MIDDLE'),
        ('Uppal', 17.4017, 78.5583, 'LOWER_MIDDLE'),
        ('Habsiguda', 17.4069, 78.5347, 'MIDDLE'),
        ('Tarnaka', 17.4269, 78.5347, 'MIDDLE'),
        ('Malkajgiri', 17.4504, 78.5215, 'MIDDLE'),
        ('AS Rao Nagar', 17.4583, 78.5433, 'LOWER_MIDDLE'),
        ('ECIL', 17.4697, 78.5658, 'MIDDLE'),
        ('Kompally', 17.5389, 78.4869, 'MIDDLE'),
        ('Alwal', 17.5044, 78.5097, 'MIDDLE'),
        ('Sainikpuri', 17.4858, 78.5558, 'MIDDLE'),
    ],
    'LOWER_MIDDLE': [
        ('Old City', 17.3616, 78.4747, 'LOW'),
        ('Charminar', 17.3616, 78.4747, 'LOW'),
        ('Falaknuma', 17.3315, 78.4527, 'LOW'),
        ('Yakutpura', 17.3583, 78.4873, 'LOW'),
        ('Malakpet', 17.3758, 78.4966, 'LOWER_MIDDLE'),
        ('Santosh Nagar', 17.3572, 78.5044, 'LOWER_MIDDLE'),
        ('Champapet', 17.3499, 78.5333, 'LOWER_MIDDLE'),
        ('Mehdipatnam', 17.3950, 78.4399, 'MIDDLE'),
        ('Tolichowki', 17.4008, 78.4266, 'MIDDLE'),
        ('Attapur', 17.3869, 78.4171, 'LOWER_MIDDLE'),
        ('Rajendranagar', 17.3244, 78.4180, 'LOWER_MIDDLE'),
        ('Shamshabad', 17.2403, 78.4294, 'LOWER_MIDDLE'),
        ('Vanasthalipuram', 17.3339, 78.5469, 'LOWER_MIDDLE'),
        ('Hayathnagar', 17.3339, 78.5833, 'LOWER_MIDDLE'),
    ],
}

# =============================================================================
# CUSTOMER SEGMENTS (Based on Research Data)
# =============================================================================

CUSTOMER_SEGMENTS = {
    # Students - Major segment per research
    'STUDENT_COLLEGE': {
        'age_range': (18, 24),
        'income_monthly_range': (0, 15000),  # Pocket money
        'gender_ratio': 0.62,  # 62% male per research
        'household_size': (1, 4),
        'lifestyle': 'STUDENT',
        'brand_preference': 'BUDGET',
        'cooking_frequency': 'LOW',
        'health_consciousness': 'LOW',
        'price_sensitivity': 'HIGH',
        'tech_savviness': 'HIGH',
        'impulse_tendency': 0.71,  # From research r=0.71
        'order_frequency_monthly': (3, 8),
        'avg_basket_size': (150, 350),
        'preferred_categories': ['Snacks & Branded Foods', 'Beverages', 'Beauty & Hygiene'],
        'peak_hours': [12, 13, 21, 22, 23],
        'weekend_preference': 0.6,
        'weight': 0.12,
        'name_distribution': {'telugu': 0.55, 'muslim': 0.20, 'north': 0.15, 'christian': 0.10},
    },
    
    'STUDENT_PG': {
        'age_range': (22, 28),
        'income_monthly_range': (15000, 35000),  # Part-time/internship
        'gender_ratio': 0.65,
        'household_size': (1, 3),
        'lifestyle': 'STUDENT',
        'brand_preference': 'BUDGET',
        'cooking_frequency': 'LOW',
        'health_consciousness': 'MEDIUM',
        'price_sensitivity': 'HIGH',
        'tech_savviness': 'HIGH',
        'impulse_tendency': 0.68,
        'order_frequency_monthly': (5, 12),
        'avg_basket_size': (200, 450),
        'preferred_categories': ['Snacks & Branded Foods', 'Beverages', 'Cleaning & Household'],
        'peak_hours': [20, 21, 22, 23],
        'weekend_preference': 0.55,
        'weight': 0.08,
        'name_distribution': {'telugu': 0.50, 'muslim': 0.15, 'north': 0.25, 'christian': 0.10},
    },
    
    # Young Working Professionals - Major segment
    'YOUNG_PROFESSIONAL_SINGLE': {
        'age_range': (23, 32),
        'income_monthly_range': (25000, 80000),
        'gender_ratio': 0.60,
        'household_size': (1, 2),
        'lifestyle': 'URBAN_FAST',
        'brand_preference': 'MASS',
        'cooking_frequency': 'LOW',
        'health_consciousness': 'MEDIUM',
        'price_sensitivity': 'MEDIUM',
        'tech_savviness': 'HIGH',
        'impulse_tendency': 0.65,
        'order_frequency_monthly': (8, 18),
        'avg_basket_size': (300, 700),
        'preferred_categories': ['Snacks & Branded Foods', 'Beverages', 'Beauty & Hygiene'],
        'peak_hours': [19, 20, 21, 22],
        'weekend_preference': 0.45,
        'weight': 0.18,
        'name_distribution': {'telugu': 0.50, 'muslim': 0.15, 'north': 0.25, 'christian': 0.10},
    },
    
    'YOUNG_PROFESSIONAL_COUPLE': {
        'age_range': (25, 35),
        'income_monthly_range': (60000, 200000),  # Combined
        'gender_ratio': 0.50,
        'household_size': (2, 2),
        'lifestyle': 'URBAN_PREMIUM',
        'brand_preference': 'PREMIUM',
        'cooking_frequency': 'MEDIUM',
        'health_consciousness': 'HIGH',
        'price_sensitivity': 'LOW',
        'tech_savviness': 'HIGH',
        'impulse_tendency': 0.55,
        'order_frequency_monthly': (10, 22),
        'avg_basket_size': (500, 1200),
        'preferred_categories': ['Gourmet & World Food', 'Fruits & Vegetables', 'Beverages'],
        'peak_hours': [19, 20, 21],
        'weekend_preference': 0.5,
        'weight': 0.10,
        'name_distribution': {'telugu': 0.45, 'muslim': 0.15, 'north': 0.30, 'christian': 0.10},
    },
    
    # Multi-generational Families
    'NUCLEAR_FAMILY_MIDDLE': {
        'age_range': (28, 45),
        'income_monthly_range': (40000, 100000),
        'gender_ratio': 0.45,  # More female decision makers
        'household_size': (3, 5),
        'lifestyle': 'SUBURBAN_BALANCED',
        'brand_preference': 'MASS',
        'cooking_frequency': 'HIGH',
        'health_consciousness': 'MEDIUM',
        'price_sensitivity': 'HIGH',
        'tech_savviness': 'MEDIUM',
        'impulse_tendency': 0.35,
        'order_frequency_monthly': (12, 25),
        'avg_basket_size': (500, 1200),
        'preferred_categories': ['Foodgrains, Oil & Masala', 'Bakery, Cakes & Dairy', 'Fruits & Vegetables'],
        'peak_hours': [10, 11, 18, 19],
        'weekend_preference': 0.3,
        'weight': 0.15,
        'name_distribution': {'telugu': 0.55, 'muslim': 0.25, 'north': 0.15, 'christian': 0.05},
    },
    
    'NUCLEAR_FAMILY_AFFLUENT': {
        'age_range': (30, 50),
        'income_monthly_range': (150000, 500000),
        'gender_ratio': 0.48,
        'household_size': (3, 5),
        'lifestyle': 'URBAN_PREMIUM',
        'brand_preference': 'PREMIUM',
        'cooking_frequency': 'MEDIUM',
        'health_consciousness': 'HIGH',
        'price_sensitivity': 'LOW',
        'tech_savviness': 'HIGH',
        'impulse_tendency': 0.50,
        'order_frequency_monthly': (15, 30),
        'avg_basket_size': (800, 2500),
        'preferred_categories': ['Gourmet & World Food', 'Fruits & Vegetables', 'Baby Care'],
        'peak_hours': [9, 10, 19, 20],
        'weekend_preference': 0.35,
        'weight': 0.06,
        'name_distribution': {'telugu': 0.50, 'muslim': 0.15, 'north': 0.25, 'christian': 0.10},
    },
    
    'JOINT_FAMILY_TRADITIONAL': {
        'age_range': (35, 55),
        'income_monthly_range': (50000, 150000),
        'gender_ratio': 0.40,
        'household_size': (5, 10),
        'lifestyle': 'TRADITIONAL',
        'brand_preference': 'BUDGET',
        'cooking_frequency': 'HIGH',
        'health_consciousness': 'LOW',
        'price_sensitivity': 'HIGH',
        'tech_savviness': 'LOW',
        'impulse_tendency': 0.20,
        'order_frequency_monthly': (8, 15),
        'avg_basket_size': (700, 1800),
        'preferred_categories': ['Foodgrains, Oil & Masala', 'Cleaning & Household', 'Bakery, Cakes & Dairy'],
        'peak_hours': [9, 10, 11],
        'weekend_preference': 0.25,
        'weight': 0.08,
        'name_distribution': {'telugu': 0.50, 'muslim': 0.35, 'north': 0.10, 'christian': 0.05},
    },
    
    # New Parents
    'NEW_PARENTS': {
        'age_range': (25, 38),
        'income_monthly_range': (50000, 180000),
        'gender_ratio': 0.40,
        'household_size': (3, 4),
        'lifestyle': 'SUBURBAN_BALANCED',
        'brand_preference': 'PREMIUM',
        'cooking_frequency': 'MEDIUM',
        'health_consciousness': 'HIGH',
        'price_sensitivity': 'MEDIUM',
        'tech_savviness': 'HIGH',
        'impulse_tendency': 0.45,
        'order_frequency_monthly': (15, 30),
        'avg_basket_size': (600, 1500),
        'preferred_categories': ['Baby Care', 'Bakery, Cakes & Dairy', 'Fruits & Vegetables'],
        'peak_hours': [10, 14, 15, 20],
        'weekend_preference': 0.4,
        'weight': 0.07,
        'name_distribution': {'telugu': 0.55, 'muslim': 0.20, 'north': 0.18, 'christian': 0.07},
    },
    
    # IT Professionals (Significant in Hyderabad)
    'IT_PROFESSIONAL': {
        'age_range': (24, 40),
        'income_monthly_range': (60000, 250000),
        'gender_ratio': 0.68,  # Male dominated
        'household_size': (1, 4),
        'lifestyle': 'URBAN_FAST',
        'brand_preference': 'MASS',
        'cooking_frequency': 'LOW',
        'health_consciousness': 'MEDIUM',
        'price_sensitivity': 'MEDIUM',
        'tech_savviness': 'HIGH',
        'impulse_tendency': 0.60,
        'order_frequency_monthly': (10, 22),
        'avg_basket_size': (400, 900),
        'preferred_categories': ['Snacks & Branded Foods', 'Beverages', 'Gourmet & World Food'],
        'peak_hours': [20, 21, 22, 23],
        'weekend_preference': 0.5,
        'weight': 0.12,
        'name_distribution': {'telugu': 0.45, 'muslim': 0.10, 'north': 0.35, 'christian': 0.10},
    },
    
    # Homemakers
    'HOMEMAKER': {
        'age_range': (25, 50),
        'income_monthly_range': (40000, 150000),  # Household income
        'gender_ratio': 0.05,  # Almost all female
        'household_size': (3, 6),
        'lifestyle': 'TRADITIONAL',
        'brand_preference': 'MASS',
        'cooking_frequency': 'HIGH',
        'health_consciousness': 'MEDIUM',
        'price_sensitivity': 'HIGH',
        'tech_savviness': 'MEDIUM',
        'impulse_tendency': 0.35,
        'order_frequency_monthly': (15, 30),
        'avg_basket_size': (450, 1100),
        'preferred_categories': ['Foodgrains, Oil & Masala', 'Fruits & Vegetables', 'Cleaning & Household'],
        'peak_hours': [10, 11, 12, 17],
        'weekend_preference': 0.25,
        'weight': 0.08,
        'name_distribution': {'telugu': 0.55, 'muslim': 0.30, 'north': 0.10, 'christian': 0.05},
    },
    
    # Late Night Cravers
    'LATE_NIGHT_CRAVER': {
        'age_range': (18, 35),
        'income_monthly_range': (15000, 100000),
        'gender_ratio': 0.70,
        'household_size': (1, 3),
        'lifestyle': 'URBAN_FAST',
        'brand_preference': 'MASS',
        'cooking_frequency': 'LOW',
        'health_consciousness': 'LOW',
        'price_sensitivity': 'MEDIUM',
        'tech_savviness': 'HIGH',
        'impulse_tendency': 0.85,
        'order_frequency_monthly': (5, 15),
        'avg_basket_size': (200, 500),
        'preferred_categories': ['Snacks & Branded Foods', 'Beverages', 'Bakery, Cakes & Dairy'],
        'peak_hours': [22, 23, 0, 1],
        'weekend_preference': 0.7,
        'weight': 0.04,
        'name_distribution': {'telugu': 0.45, 'muslim': 0.20, 'north': 0.25, 'christian': 0.10},
    },
    
    # Fitness Enthusiasts
    'FITNESS_ENTHUSIAST': {
        'age_range': (22, 42),
        'income_monthly_range': (40000, 180000),
        'gender_ratio': 0.55,
        'household_size': (1, 4),
        'lifestyle': 'HEALTH_FOCUSED',
        'brand_preference': 'PREMIUM',
        'cooking_frequency': 'MEDIUM',
        'health_consciousness': 'HIGH',
        'price_sensitivity': 'LOW',
        'tech_savviness': 'HIGH',
        'impulse_tendency': 0.30,
        'order_frequency_monthly': (12, 25),
        'avg_basket_size': (500, 1100),
        'preferred_categories': ['Fruits & Vegetables', 'Eggs, Meat & Fish', 'Gourmet & World Food'],
        'peak_hours': [7, 8, 18, 19],
        'weekend_preference': 0.45,
        'weight': 0.04,
        'name_distribution': {'telugu': 0.45, 'muslim': 0.10, 'north': 0.35, 'christian': 0.10},
    },
    
    # Senior Citizens
    'SENIOR_CITIZEN': {
        'age_range': (55, 75),
        'income_monthly_range': (25000, 80000),  # Pension
        'gender_ratio': 0.45,
        'household_size': (1, 3),
        'lifestyle': 'TRADITIONAL',
        'brand_preference': 'MASS',
        'cooking_frequency': 'HIGH',
        'health_consciousness': 'HIGH',
        'price_sensitivity': 'MEDIUM',
        'tech_savviness': 'LOW',
        'impulse_tendency': 0.15,
        'order_frequency_monthly': (6, 12),
        'avg_basket_size': (400, 800),
        'preferred_categories': ['Foodgrains, Oil & Masala', 'Fruits & Vegetables', 'Beauty & Hygiene'],
        'peak_hours': [9, 10, 11, 16],
        'weekend_preference': 0.3,
        'weight': 0.03,
        'name_distribution': {'telugu': 0.60, 'muslim': 0.25, 'north': 0.10, 'christian': 0.05},
    },
    
    # Budget Conscious (Low income but 57% spending increase per research)
    'BUDGET_CONSCIOUS': {
        'age_range': (22, 45),
        'income_monthly_range': (10000, 30000),
        'gender_ratio': 0.55,
        'household_size': (2, 5),
        'lifestyle': 'BUDGET_FOCUSED',
        'brand_preference': 'BUDGET',
        'cooking_frequency': 'HIGH',
        'health_consciousness': 'LOW',
        'price_sensitivity': 'HIGH',
        'tech_savviness': 'MEDIUM',
        'impulse_tendency': 0.40,  # Still impulse buy despite budget
        'order_frequency_monthly': (4, 10),
        'avg_basket_size': (150, 350),
        'preferred_categories': ['Foodgrains, Oil & Masala', 'Snacks & Branded Foods', 'Cleaning & Household'],
        'peak_hours': [11, 12, 18, 19],
        'weekend_preference': 0.35,
        'weight': 0.05,
        'name_distribution': {'telugu': 0.50, 'muslim': 0.35, 'north': 0.10, 'christian': 0.05},
    },
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_customer_id():
    return f"HYD-{hashlib.md5(str(random.random()).encode()).hexdigest()[:8].upper()}"

def generate_phone():
    prefixes = ['98', '97', '96', '95', '94', '93', '91', '90', '89', '88', '87', '86', '85', '84', '83', '82', '81', '80', '79', '78', '77', '76', '75', '74', '73', '72', '71', '70']
    return f"+91{random.choice(prefixes)}{random.randint(10000000, 99999999)}"

def generate_email(first_name, last_name, birth_year):
    domains = ['gmail.com', 'gmail.com', 'gmail.com', 'gmail.com', 'yahoo.com', 
               'yahoo.co.in', 'hotmail.com', 'outlook.com', 'rediffmail.com']
    patterns = [
        f"{first_name.lower()}.{last_name.lower()}",
        f"{first_name.lower()}{last_name.lower()}",
        f"{first_name.lower()}{random.randint(1, 999)}",
        f"{first_name.lower()}.{last_name.lower()}{str(birth_year)[-2:]}",
        f"{first_name.lower()}_{last_name.lower()}",
        f"{last_name.lower()}.{first_name.lower()}",
    ]
    return f"{random.choice(patterns)}@{random.choice(domains)}"

def get_name_by_community(gender, community):
    if community == 'telugu':
        if gender == 'M':
            return random.choice(TELUGU_MALE_NAMES), random.choice(TELUGU_SURNAMES)
        else:
            return random.choice(TELUGU_FEMALE_NAMES), random.choice(TELUGU_SURNAMES)
    elif community == 'muslim':
        if gender == 'M':
            return random.choice(MUSLIM_MALE_NAMES), random.choice(MUSLIM_SURNAMES)
        else:
            return random.choice(MUSLIM_FEMALE_NAMES), random.choice(MUSLIM_SURNAMES)
    elif community == 'north':
        if gender == 'M':
            return random.choice(NORTH_INDIAN_MALE_NAMES), random.choice(NORTH_INDIAN_SURNAMES)
        else:
            return random.choice(NORTH_INDIAN_FEMALE_NAMES), random.choice(NORTH_INDIAN_SURNAMES)
    else:  # christian
        if gender == 'M':
            return random.choice(CHRISTIAN_MALE_NAMES), random.choice(CHRISTIAN_SURNAMES)
        else:
            return random.choice(CHRISTIAN_FEMALE_NAMES), random.choice(CHRISTIAN_SURNAMES)

def get_location_by_income(income_monthly):
    if income_monthly > 100000:
        area_type = random.choices(['PREMIUM', 'UPPER_MIDDLE'], weights=[0.6, 0.4])[0]
    elif income_monthly > 50000:
        area_type = random.choices(['UPPER_MIDDLE', 'MIDDLE'], weights=[0.5, 0.5])[0]
    elif income_monthly > 25000:
        area_type = random.choices(['MIDDLE', 'LOWER_MIDDLE'], weights=[0.6, 0.4])[0]
    else:
        area_type = random.choices(['MIDDLE', 'LOWER_MIDDLE'], weights=[0.3, 0.7])[0]
    
    area = random.choice(HYDERABAD_AREAS[area_type])
    return area

def get_income_bracket(income_monthly):
    if income_monthly < 15000:
        return 'LOW'
    elif income_monthly < 30000:
        return 'LOWER_MIDDLE'
    elif income_monthly < 60000:
        return 'MIDDLE'
    elif income_monthly < 150000:
        return 'UPPER_MIDDLE'
    else:
        return 'HIGH'

def score_with_variance(base, variance=0.12):
    return round(np.clip(base + np.random.uniform(-variance, variance), 0.05, 0.98), 2)

def generate_customer(segment_name, segment):
    # Gender based on segment ratio
    gender = 'M' if random.random() < segment['gender_ratio'] else 'F'
    
    # Age
    age = random.randint(*segment['age_range'])
    birth_year = 2024 - age
    
    # Community selection based on segment distribution
    communities = list(segment['name_distribution'].keys())
    weights = list(segment['name_distribution'].values())
    community = random.choices(communities, weights=weights)[0]
    
    # Name
    first_name, last_name = get_name_by_community(gender, community)
    
    # Income
    income_monthly = int(np.random.uniform(*segment['income_monthly_range']))
    income_monthly = round(income_monthly / 1000) * 1000
    income_annual = income_monthly * 12
    
    # Location
    area_name, lat, lng, expected_income = get_location_by_income(income_monthly)
    lat += random.uniform(-0.008, 0.008)
    lng += random.uniform(-0.008, 0.008)
    
    # Household
    household_size = random.randint(*segment['household_size'])
    
    # Behavioral scores
    health_map = {'LOW': 0.25, 'MEDIUM': 0.50, 'HIGH': 0.80}
    price_map = {'LOW': 0.25, 'MEDIUM': 0.50, 'HIGH': 0.80}
    tech_map = {'LOW': 0.30, 'MEDIUM': 0.60, 'HIGH': 0.90}
    
    health_consciousness = score_with_variance(health_map[segment['health_consciousness']])
    price_sensitivity = score_with_variance(price_map[segment['price_sensitivity']])
    tech_savviness = score_with_variance(tech_map[segment['tech_savviness']])
    impulse_tendency = score_with_variance(segment['impulse_tendency'])
    
    # Order patterns
    order_freq = random.randint(*segment['order_frequency_monthly'])
    avg_basket = int(np.random.uniform(*segment['avg_basket_size']))
    
    # Account info
    account_created = datetime(2020, 6, 1) + timedelta(days=random.randint(0, 1600))
    last_order = datetime(2024, 12, 1) - timedelta(days=random.randint(0, 45))
    months_active = max(1, (datetime(2024, 12, 1) - account_created).days // 30)
    total_orders = int(order_freq * months_active * random.uniform(0.6, 1.1))
    total_orders = max(1, total_orders)
    
    lifetime_value = total_orders * avg_basket
    
    # Loyalty tier
    if lifetime_value > 150000:
        loyalty_tier = 'PLATINUM'
    elif lifetime_value > 75000:
        loyalty_tier = 'GOLD'
    elif lifetime_value > 30000:
        loyalty_tier = 'SILVER'
    else:
        loyalty_tier = 'BRONZE'
    
    # App engagement
    app_sessions_monthly = int(order_freq * random.uniform(2.5, 5))
    
    # Payment preference (UPI dominant in India)
    payment_methods = ['UPI', 'CARD', 'COD', 'WALLET', 'NETBANKING']
    if income_monthly > 80000:
        payment_weights = [0.40, 0.35, 0.08, 0.12, 0.05]
    elif income_monthly > 30000:
        payment_weights = [0.50, 0.20, 0.15, 0.10, 0.05]
    else:
        payment_weights = [0.45, 0.10, 0.30, 0.10, 0.05]
    preferred_payment = random.choices(payment_methods, weights=payment_weights)[0]
    
    # Delivery preference
    delivery_prefs = ['EXPRESS', 'SCHEDULED', 'NO_PREFERENCE']
    delivery_weights = [0.55, 0.15, 0.30]
    preferred_delivery = random.choices(delivery_prefs, weights=delivery_weights)[0]
    
    # Subscription
    has_subscription = random.random() < (0.20 if income_monthly > 60000 else 0.08)
    
    # Peak hours
    primary_order_hour = random.choice(segment['peak_hours'])
    
    return {
        'customer_id': generate_customer_id(),
        'first_name': first_name,
        'last_name': last_name,
        'full_name': f"{first_name} {last_name}",
        'gender': gender,
        'age': age,
        'birth_year': birth_year,
        'community': community.upper(),
        'phone': generate_phone(),
        'email': generate_email(first_name, last_name, birth_year),
        
        'locality': area_name,
        'city': 'Hyderabad',
        'state': 'Telangana',
        'pincode': f"5000{random.randint(10, 99)}",
        'latitude': round(lat, 6),
        'longitude': round(lng, 6),
        
        'household_size': household_size,
        'monthly_income': income_monthly,
        'annual_income': income_annual,
        'income_bracket': get_income_bracket(income_monthly),
        
        'customer_segment': segment_name,
        'lifestyle': segment['lifestyle'],
        'brand_preference': segment['brand_preference'],
        'cooking_frequency': segment['cooking_frequency'],
        
        'health_consciousness': health_consciousness,
        'price_sensitivity': price_sensitivity,
        'tech_savviness': tech_savviness,
        'impulse_tendency': impulse_tendency,
        'weekend_preference': round(segment['weekend_preference'] + random.uniform(-0.08, 0.08), 2),
        
        'orders_per_month': order_freq,
        'avg_basket_value': avg_basket,
        'primary_order_hour': primary_order_hour,
        
        'account_created_date': account_created.strftime('%Y-%m-%d'),
        'last_order_date': last_order.strftime('%Y-%m-%d'),
        'total_orders': total_orders,
        'lifetime_value': lifetime_value,
        'loyalty_tier': loyalty_tier,
        
        'app_sessions_monthly': app_sessions_monthly,
        'preferred_payment': preferred_payment,
        'preferred_delivery': preferred_delivery,
        'has_subscription': has_subscription,
        
        'preferred_category_1': segment['preferred_categories'][0],
        'preferred_category_2': segment['preferred_categories'][1] if len(segment['preferred_categories']) > 1 else '',
        'preferred_category_3': segment['preferred_categories'][2] if len(segment['preferred_categories']) > 2 else '',
        
        'avg_items_per_order': max(1, int(avg_basket / 120)),
        'morning_order_tendency': round(0.7 if primary_order_hour < 12 else 0.3 + random.uniform(-0.1, 0.1), 2),
        'evening_order_tendency': round(0.7 if primary_order_hour >= 18 else 0.3 + random.uniform(-0.1, 0.1), 2),
    }

# =============================================================================
# GENERATE 1.5 MILLION CUSTOMERS
# =============================================================================

NUM_CUSTOMERS = 1_500_000
BATCH_SIZE = 50000

# Calculate segment counts
total_weight = sum(s['weight'] for s in CUSTOMER_SEGMENTS.values())
segment_counts = {
    name: int(NUM_CUSTOMERS * seg['weight'] / total_weight)
    for name, seg in CUSTOMER_SEGMENTS.items()
}

# Adjust to match exact count
diff = NUM_CUSTOMERS - sum(segment_counts.values())
largest = max(segment_counts, key=segment_counts.get)
segment_counts[largest] += diff

print(f"\nGenerating {NUM_CUSTOMERS:,} customers...")
print("\nSegment distribution:")
for name, count in sorted(segment_counts.items(), key=lambda x: -x[1]):
    pct = count / NUM_CUSTOMERS * 100
    print(f"  {name}: {count:,} ({pct:.1f}%)")

# Generate in batches for memory efficiency
all_customers = []
customers_generated = 0

for segment_name, segment in CUSTOMER_SEGMENTS.items():
    count = segment_counts[segment_name]
    print(f"\nGenerating {segment_name}: {count:,} customers...")
    
    segment_customers = []
    for i in range(count):
        customer = generate_customer(segment_name, segment)
        segment_customers.append(customer)
        
        if (i + 1) % 100000 == 0:
            print(f"  Progress: {i+1:,}/{count:,}")
    
    all_customers.extend(segment_customers)
    customers_generated += count
    print(f"  Done! Total: {customers_generated:,}/{NUM_CUSTOMERS:,}")

# Convert to DataFrame
print(f"\nConverting to DataFrame...")
df = pd.DataFrame(all_customers)

# Shuffle
print("Shuffling...")
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save
output_file = 'customer_profiles.csv'
print(f"Saving to {output_file}...")
df.to_csv(output_file, index=False)

print("\n" + "="*70)
print(f"SUCCESS: Generated {len(df):,} customer profiles")
print("="*70)

# Statistics
print(f"\nColumns: {len(df.columns)}")
print(f"\nGender: M={len(df[df['gender']=='M']):,} ({len(df[df['gender']=='M'])/len(df)*100:.1f}%), F={len(df[df['gender']=='F']):,} ({len(df[df['gender']=='F'])/len(df)*100:.1f}%)")
print(f"Age: {df['age'].min()}-{df['age'].max()} (mean: {df['age'].mean():.1f})")
print(f"Monthly Income: ₹{df['monthly_income'].min():,} - ₹{df['monthly_income'].max():,}")

print("\nIncome Distribution:")
for bracket in ['LOW', 'LOWER_MIDDLE', 'MIDDLE', 'UPPER_MIDDLE', 'HIGH']:
    count = len(df[df['income_bracket'] == bracket])
    print(f"  {bracket}: {count:,} ({count/len(df)*100:.1f}%)")

print("\nCommunity Distribution:")
for comm in df['community'].unique():
    count = len(df[df['community'] == comm])
    print(f"  {comm}: {count:,} ({count/len(df)*100:.1f}%)")

print("\nTop 10 Localities:")
for loc, count in df['locality'].value_counts().head(10).items():
    print(f"  {loc}: {count:,} ({count/len(df)*100:.1f}%)")
