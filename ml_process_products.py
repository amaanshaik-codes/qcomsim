"""
ML-Enhanced Product CSV Processor for Simulation
Uses embeddings, clustering, and learned patterns for realistic values
Outputs: final.csv
"""

import pandas as pd
import numpy as np
import re
import hashlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Load the data
print("Loading data...")
df = pd.read_csv('products.csv')
df.columns = df.columns.str.strip()

# Drop empty columns
df = df.drop(columns=[col for col in df.columns if 'Unnamed' in col], errors='ignore')

print(f"Loaded {len(df)} products")

# =============================================================================
# ML FEATURE ENGINEERING
# =============================================================================

print("\n[1/6] Building ML features...")

# Create text features for ML
df['text_features'] = (
    df['product'].fillna('') + ' ' + 
    df['category'].fillna('') + ' ' + 
    df['sub_category'].fillna('') + ' ' + 
    df['type'].fillna('') + ' ' +
    df['brand'].fillna('')
).str.lower()

# TF-IDF vectorization for product similarity
print("  - Building TF-IDF vectors...")
tfidf = TfidfVectorizer(max_features=500, stop_words='english', ngram_range=(1, 2))
tfidf_matrix = tfidf.fit_transform(df['text_features'])

# Cluster products into groups for better defaults
print("  - Clustering products into 50 groups...")
n_clusters = 50
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
df['product_cluster'] = kmeans.fit_predict(tfidf_matrix)

# =============================================================================
# REALISTIC WEIGHT EXTRACTION (ML-Enhanced)
# =============================================================================

print("\n[2/6] Extracting weights with ML enhancement...")

def extract_weight_ml(row):
    """ML-enhanced weight extraction."""
    name = str(row['product']).lower() if pd.notna(row['product']) else ''
    category = str(row['category']).lower() if pd.notna(row['category']) else ''
    sub_cat = str(row['sub_category']).lower() if pd.notna(row['sub_category']) else ''
    type_col = str(row['type']).lower() if pd.notna(row['type']) else ''
    
    # Skip weight patterns that are clearly NOT product weight
    # (baby weight ranges, dog weight ranges, etc.)
    skip_patterns = [
        r'\d+-\d+\s*kg',  # Weight ranges like "6-11 kg" for diapers
        r'for\s+\d+\s*kg',  # "for 25 kg dogs"
        r'\d+\s*kg\s*\+',  # Part of combo descriptions
        r'\d+\s*kg\s*dog',  # Dog weight
    ]
    
    for pattern in skip_patterns:
        if re.search(pattern, name):
            name = re.sub(pattern, '', name)
    
    # Extract weight with priority order
    patterns = [
        # Exact weight patterns
        (r'(\d+(?:\.\d+)?)\s*kg\b', lambda x: int(float(x) * 1000)),
        (r'(\d+(?:\.\d+)?)\s*gm?\b', lambda x: int(float(x))),
        (r'(\d+(?:\.\d+)?)\s*gram', lambda x: int(float(x))),
        (r'(\d+(?:\.\d+)?)\s*ml\b', lambda x: int(float(x))),  # Approximate
        (r'(\d+(?:\.\d+)?)\s*l\b(?!a|i|o|u|e)', lambda x: int(float(x) * 1000)),
        (r'(\d+(?:\.\d+)?)\s*litre', lambda x: int(float(x) * 1000)),
    ]
    
    for pattern, converter in patterns:
        matches = re.findall(pattern, name)
        if matches:
            try:
                # Take the most reasonable weight (filter out very small/large)
                weights = [converter(m) for m in matches]
                valid_weights = [w for w in weights if 5 <= w <= 25000]
                if valid_weights:
                    return max(valid_weights)  # Take largest valid weight
            except:
                pass
    
    return None

# Apply extraction
df['extracted_weight'] = df.apply(extract_weight_ml, axis=1)

# Build category-specific weight distributions from extracted data
print("  - Learning weight distributions from data...")
weight_by_cluster = df.groupby('product_cluster')['extracted_weight'].agg(['median', 'mean', 'std']).fillna(0)

# Realistic category defaults (research-based)
CATEGORY_WEIGHTS = {
    # Fresh produce (per typical purchase unit)
    'fresh vegetables': (300, 100),  # mean, std
    'fresh fruits': (400, 150),
    'cuts & sprouts': (250, 50),
    'exotic fruits': (300, 100),
    
    # Dairy
    'milk': (500, 200),
    'curd': (400, 100),
    'cheese': (200, 100),
    'butter': (100, 50),
    'paneer': (200, 50),
    'ice cream': (500, 200),
    
    # Staples
    'rice': (1000, 500),
    'atta': (1000, 500),
    'dal': (500, 250),
    'oil': (1000, 500),
    'ghee': (500, 250),
    'sugar': (1000, 500),
    
    # Beverages
    'juice': (500, 250),
    'soft drink': (500, 300),
    'water': (1000, 500),
    'tea': (250, 100),
    'coffee': (200, 100),
    
    # Snacks
    'chips': (100, 50),
    'biscuit': (150, 75),
    'chocolate': (100, 75),
    'namkeen': (200, 100),
    'noodles': (200, 100),
    
    # Personal care
    'shampoo': (200, 100),
    'soap': (100, 50),
    'lotion': (200, 100),
    'cream': (50, 25),
    'deo': (150, 50),
    
    # Cleaning
    'detergent': (1000, 500),
    'dishwash': (500, 250),
    'cleaner': (500, 250),
    
    # Baby
    'diaper': (1500, 500),
    'baby food': (400, 200),
    
    # Meat & Fish
    'chicken': (500, 200),
    'mutton': (500, 200),
    'fish': (500, 200),
    'egg': (360, 60),  # ~6 eggs
    'sausage': (250, 100),
    
    # Pet
    'pet food': (1000, 500),
    'dog': (500, 300),
    'cat': (400, 200),
}

def get_realistic_weight(row):
    """Get realistic weight using ML cluster + category fallback."""
    # First try extracted weight
    if pd.notna(row['extracted_weight']) and 10 <= row['extracted_weight'] <= 20000:
        return int(row['extracted_weight'])
    
    # Try cluster median
    cluster = row['product_cluster']
    cluster_median = weight_by_cluster.loc[cluster, 'median']
    if cluster_median > 0:
        # Add some variance
        std = weight_by_cluster.loc[cluster, 'std']
        if std > 0:
            weight = np.random.normal(cluster_median, std * 0.3)
            return int(np.clip(weight, 20, 15000))
    
    # Category-based fallback
    text = f"{row['category']} {row['sub_category']} {row['type']}".lower()
    
    for key, (mean, std) in CATEGORY_WEIGHTS.items():
        if key in text:
            weight = np.random.normal(mean, std * 0.5)
            return int(np.clip(weight, 20, 15000))
    
    # Default
    return int(np.random.normal(300, 100))

df['weight_g'] = df.apply(get_realistic_weight, axis=1)

# =============================================================================
# STORAGE TYPE (ML-Enhanced Classification)
# =============================================================================

print("\n[3/6] Classifying storage types...")

# Training data for storage classification
FROZEN_KEYWORDS = ['frozen', 'ice cream', 'ice-cream', 'kulfi', 'popsicle', 'gelato', 'sorbet']
CHILLED_KEYWORDS = ['milk', 'curd', 'yogurt', 'yoghurt', 'cheese', 'paneer', 'butter', 'cream cheese',
                    'fresh cream', 'whipped cream', 'tofu', 'dahi', 'lassi', 'chaas', 'buttermilk',
                    'egg', 'chicken', 'mutton', 'lamb', 'pork', 'fish', 'seafood', 'prawn', 'shrimp',
                    'salmon', 'tuna', 'crab', 'lobster', 'meat', 'sausage', 'bacon', 'ham', 'salami',
                    'fresh vegetable', 'fresh fruit', 'cut fruit', 'cut vegetable', 'salad',
                    'juice fresh', 'smoothie', 'marinades']

def classify_storage(row):
    """ML-enhanced storage classification."""
    text = f"{row['product']} {row['category']} {row['sub_category']} {row['type']}".lower()
    
    # Explicit frozen
    if any(kw in text for kw in FROZEN_KEYWORDS):
        return 'FROZEN'
    
    # Explicit chilled
    if any(kw in text for kw in CHILLED_KEYWORDS):
        # But not if it's a powder or long-life version
        if any(x in text for x in ['powder', 'masala', 'mix', 'instant', 'uht', 'tetra', 'long life']):
            return 'AMBIENT'
        return 'CHILLED'
    
    # Category-based
    if 'dairy' in text and 'masala' not in text:
        if 'ghee' in text or 'butter' in text.split():
            return 'AMBIENT'  # Ghee is shelf-stable
        return 'CHILLED'
    
    if row['sub_category'] in ['Fresh Vegetables', 'Fresh Fruits', 'Cuts & Sprouts', 
                                'Exotic Fruits & Veggies', 'Organic Fruits & Vegetables']:
        return 'CHILLED'
    
    if row['category'] == 'Eggs, Meat & Fish':
        return 'CHILLED'
    
    return 'AMBIENT'

df['storage_type'] = df.apply(classify_storage, axis=1)

# =============================================================================
# SHELF LIFE (Realistic Model)
# =============================================================================

print("\n[4/6] Calculating shelf life...")

SHELF_LIFE_HOURS = {
    # Ultra-fresh (1-3 days)
    'fresh milk': 72,
    'cut fruit': 24,
    'cut vegetable': 48,
    'salad': 24,
    'fresh juice': 24,
    
    # Fresh (3-7 days)
    'bread': 72,
    'cake': 48,
    'pastry': 48,
    'curd': 120,
    'yogurt': 168,
    'paneer': 120,
    'cheese soft': 168,
    'tofu': 120,
    'fresh fruit': 120,
    'fresh vegetable': 120,
    'organic vegetable': 96,  # Organic often shorter
    'organic fruit': 96,
    
    # Short (1-2 weeks)
    'egg': 336,  # 14 days
    'chicken': 72,  # Raw, refrigerated
    'fish': 48,
    'meat': 72,
    'butter': 336,
    'cream': 168,
    'sausage': 168,
    
    # Frozen (1-3 months)
    'frozen': 2160,
    'ice cream': 2160,
    
    # Medium shelf (1-6 months)
    'cheese hard': 2160,
    'juice tetra': 2160,
    'uht milk': 2160,
    'biscuit': 2160,
    'cookie': 1440,
    'chips': 1440,
    'namkeen': 1440,
    'chocolate': 4320,
    'noodles': 4320,
    
    # Long shelf (6-12+ months)
    'rice': 8760,
    'atta': 4320,
    'dal': 8760,
    'oil': 8760,
    'ghee': 8760,
    'sugar': 17520,
    'salt': 17520,
    'pickle': 8760,
    'jam': 8760,
    'sauce': 8760,
    'spice': 8760,
    'masala': 4320,
    'canned': 17520,
    'tinned': 17520,
    
    # Non-food
    'soap': 17520,
    'shampoo': 17520,
    'detergent': 17520,
    'cleaner': 17520,
}

def get_shelf_life(row):
    """Get realistic shelf life based on product characteristics."""
    text = f"{row['product']} {row['category']} {row['sub_category']} {row['type']}".lower()
    storage = row['storage_type']
    
    # Check specific patterns first
    for key, hours in sorted(SHELF_LIFE_HOURS.items(), key=lambda x: -len(x[0])):
        if key in text:
            # Add some variance (±20%)
            variance = np.random.uniform(0.8, 1.2)
            return int(hours * variance)
    
    # Storage-based defaults
    if storage == 'FROZEN':
        return int(np.random.uniform(1800, 2520))  # 75-105 days
    elif storage == 'CHILLED':
        return int(np.random.uniform(72, 168))  # 3-7 days
    else:
        return int(np.random.uniform(2160, 4320))  # 90-180 days

df['shelf_life_hours'] = df.apply(get_shelf_life, axis=1)

# Freshness decay is inverse of shelf life
df['freshness_decay'] = np.clip(1 - (df['shelf_life_hours'] / 8760), 0.05, 0.95).round(2)

# =============================================================================
# PHYSICS PROPERTIES
# =============================================================================

print("\n[5/6] Computing physics properties...")

# Volume estimation using product-specific density
def estimate_volume(row):
    """Estimate volume based on product density characteristics."""
    text = f"{row['product']} {row['category']} {row['sub_category']} {row['type']}".lower()
    weight = row['weight_g']
    
    # Density multipliers (volume per gram)
    if any(x in text for x in ['chips', 'popcorn', 'puff', 'kurkure', 'cheetos']):
        multiplier = np.random.uniform(7, 10)  # Very airy
    elif any(x in text for x in ['cereal', 'flakes', 'granola', 'muesli', 'oats']):
        multiplier = np.random.uniform(4, 6)  # Airy
    elif any(x in text for x in ['bread', 'bun', 'pav', 'cake', 'muffin']):
        multiplier = np.random.uniform(2.5, 4)  # Light
    elif any(x in text for x in ['biscuit', 'cookie', 'wafer', 'rusk']):
        multiplier = np.random.uniform(2, 3)  # Medium-light
    elif any(x in text for x in ['oil', 'ghee', 'milk', 'juice', 'water', 'liquid']):
        multiplier = np.random.uniform(1.0, 1.2)  # Dense liquid
    elif any(x in text for x in ['rice', 'dal', 'atta', 'flour', 'sugar', 'salt']):
        multiplier = np.random.uniform(1.3, 1.6)  # Dense powder/grain
    elif any(x in text for x in ['meat', 'chicken', 'fish', 'mutton']):
        multiplier = np.random.uniform(1.1, 1.4)  # Dense solid
    else:
        multiplier = np.random.uniform(1.5, 2.5)  # Default
    
    return int(weight * multiplier)

df['volume_cm3'] = df.apply(estimate_volume, axis=1)

# Fragility score
def get_fragility(row):
    """Calculate fragility score with ML-like inference."""
    text = f"{row['product']} {row['category']} {row['sub_category']} {row['type']}".lower()
    
    fragility_scores = [
        (['egg', 'glass', 'ceramic', 'crystal', 'crockery', 'porcelain'], 0.95),
        (['chips', 'wafer', 'crisp', 'papad', 'pappadam', 'kurkure'], 0.85),
        (['bread', 'cake', 'pastry', 'croissant', 'donut', 'muffin'], 0.75),
        (['banana', 'tomato', 'grape', 'strawberry', 'berry', 'peach'], 0.70),
        (['biscuit', 'cookie', 'rusk'], 0.55),
        (['fruit', 'vegetable'], 0.50),
        (['bottle', 'jar'], 0.40),
        (['pouch', 'packet', 'pack', 'sachet'], 0.20),
        (['can', 'tin', 'canned', 'tinned'], 0.10),
        (['rice', 'atta', 'dal', 'oil', 'ghee', 'detergent'], 0.10),
    ]
    
    for keywords, score in fragility_scores:
        if any(kw in text for kw in keywords):
            return round(score + np.random.uniform(-0.05, 0.05), 2)
    
    return round(np.random.uniform(0.25, 0.40), 2)

df['fragility_score'] = df.apply(get_fragility, axis=1)

# Spill risk
def get_spill_risk(row):
    """Determine spill risk."""
    text = f"{row['product']} {row['sub_category']} {row['type']}".lower()
    
    liquid_keywords = ['oil', 'liquid', 'juice', 'milk', 'water', 'syrup', 'sauce', 
                       'ketchup', 'shampoo', 'lotion', 'gel', 'wash', 'drink', 
                       'beverage', 'ghee', 'honey', 'pickle', 'squash', 'soup',
                       'cream', 'yogurt', 'lassi', 'buttermilk']
    
    # Check if in solid/safe packaging
    safe_packaging = ['powder', 'bar', 'tablet', 'capsule', 'can', 'tin', 'tetra']
    
    if any(kw in text for kw in liquid_keywords):
        if any(pkg in text for pkg in safe_packaging):
            return False
        return True
    return False

df['spill_risk'] = df.apply(get_spill_risk, axis=1)

# Prep time
def get_prep_time(row):
    """Estimate picker prep time in seconds."""
    text = f"{row['category']} {row['sub_category']} {row['type']}".lower()
    storage = row['storage_type']
    weight = row['weight_g']
    
    base_time = 8  # Base scan and pick time
    
    # Add time for special handling
    if 'fresh vegetable' in text or 'fresh fruit' in text:
        base_time += np.random.randint(30, 45)  # Weighing, selection
    elif 'cuts & sprouts' in text:
        base_time += np.random.randint(20, 30)
    elif storage == 'FROZEN':
        base_time += np.random.randint(10, 20)  # Freezer access
    elif storage == 'CHILLED':
        base_time += np.random.randint(5, 12)  # Chiller access
    elif 'meat' in text or 'fish' in text or 'chicken' in text:
        base_time += np.random.randint(25, 40)
    elif weight > 5000:
        base_time += np.random.randint(8, 15)  # Heavy item
    
    # Fragile items need more care
    if row['fragility_score'] > 0.7:
        base_time += np.random.randint(5, 10)
    
    return int(base_time)

df['prep_time_sec'] = df.apply(get_prep_time, axis=1)

# =============================================================================
# PSYCHOLOGY LAYER (ML-Enhanced)
# =============================================================================

print("\n[6/6] Computing psychology layer...")

# Brand tier using price percentile within category
df['price_percentile'] = df.groupby('category')['sale_price'].transform(
    lambda x: x.rank(pct=True)
)

BUDGET_BRANDS = ['bb royal', 'bb home', 'bb popular', 'fresho', 'super saver', 'value', 
                  'everyday', 'home brand', 'best price']
PREMIUM_BRANDS = ['organic', 'premium', 'gold', 'signature', 'artisan', 'gourmet',
                   'imported', 'special', 'luxury', 'pro', 'professional']

def get_brand_tier(row):
    """Classify brand tier using multiple signals."""
    brand = str(row['brand']).lower() if pd.notna(row['brand']) else ''
    product = str(row['product']).lower()
    price_pct = row['price_percentile']
    
    # Explicit brand indicators
    if any(b in brand for b in BUDGET_BRANDS):
        return 'BUDGET'
    if any(p in brand or p in product for p in PREMIUM_BRANDS):
        return 'PREMIUM'
    
    # Price-based
    if price_pct >= 0.75:
        return 'PREMIUM'
    elif price_pct <= 0.25:
        return 'BUDGET'
    else:
        return 'MASS'

df['brand_tier'] = df.apply(get_brand_tier, axis=1)

# Impulse score using category + product characteristics
IMPULSE_CATEGORIES = {
    'chocolate': 0.92,
    'candy': 0.90,
    'ice cream': 0.88,
    'chips': 0.85,
    'namkeen': 0.82,
    'biscuit': 0.75,
    'cookie': 0.78,
    'soft drink': 0.80,
    'cold drink': 0.80,
    'juice': 0.65,
    'snack': 0.80,
    'dessert': 0.85,
    'cake': 0.75,
    'perfume': 0.60,
    'deo': 0.55,
    'gum': 0.90,
    'mint': 0.88,
    
    # Low impulse
    'rice': 0.10,
    'atta': 0.10,
    'dal': 0.12,
    'oil': 0.12,
    'ghee': 0.15,
    'detergent': 0.08,
    'cleaner': 0.10,
    'toilet': 0.05,
    'salt': 0.05,
    'sugar': 0.10,
}

def get_impulse_score(row):
    """Calculate impulse purchase likelihood."""
    text = f"{row['category']} {row['sub_category']} {row['type']}".lower()
    
    for key, score in sorted(IMPULSE_CATEGORIES.items(), key=lambda x: -len(x[0])):
        if key in text:
            return round(score + np.random.uniform(-0.05, 0.05), 2)
    
    return round(np.random.uniform(0.35, 0.50), 2)

df['impulse_score'] = df.apply(get_impulse_score, axis=1)
df['impulse_score'] = df['impulse_score'].clip(0, 1)

# Substitute group - using product clusters + type
def get_substitute_group(row):
    """Generate substitute group ID based on ML clustering."""
    # Combine cluster with type for granular grouping
    cluster = row['product_cluster']
    type_hash = hashlib.md5(str(row['type']).encode()).hexdigest()[:4]
    return f"GRP-{cluster:02d}-{type_hash.upper()}"

df['substitute_group'] = df.apply(get_substitute_group, axis=1)

# Time-based demand patterns
MORNING_HIGH = ['milk', 'bread', 'egg', 'cereal', 'breakfast', 'tea', 'coffee',
                'curd', 'yogurt', 'butter', 'jam', 'juice', 'oats', 'corn flakes']
EVENING_HIGH = ['snack', 'chips', 'chocolate', 'ice cream', 'soft drink', 'beer',
                'wine', 'namkeen', 'frozen', 'ready to eat', 'instant', 'pizza',
                'burger', 'fries', 'popcorn', 'dessert', 'cake']

def get_demand_patterns(row):
    """Calculate morning and evening demand factors."""
    text = f"{row['product']} {row['sub_category']} {row['type']}".lower()
    
    morning = 0.40
    evening = 0.50
    
    if any(kw in text for kw in MORNING_HIGH):
        morning = round(np.random.uniform(0.75, 0.95), 2)
    if any(kw in text for kw in EVENING_HIGH):
        evening = round(np.random.uniform(0.80, 0.95), 2)
    
    # Inverse relationship
    if morning > 0.7:
        evening = min(evening, 0.40)
    if evening > 0.7:
        morning = min(morning, 0.35)
    
    # Add small variance
    morning = round(morning + np.random.uniform(-0.05, 0.05), 2)
    evening = round(evening + np.random.uniform(-0.05, 0.05), 2)
    
    return pd.Series({'morning_demand': np.clip(morning, 0.1, 0.95), 
                      'evening_demand': np.clip(evening, 0.1, 0.95)})

demand_df = df.apply(get_demand_patterns, axis=1)
df['morning_demand'] = demand_df['morning_demand']
df['evening_demand'] = demand_df['evening_demand']

# =============================================================================
# CLEANUP COLUMNS
# =============================================================================

print("\n[7/7] Generating clean IDs and names...")

# SKU ID generation
CAT_CODES = {
    'beauty & hygiene': 'BEA',
    'kitchen, garden & pets': 'KGP',
    'cleaning & household': 'CLN',
    'gourmet & world food': 'GWF',
    'snacks & branded foods': 'SNK',
    'foodgrains, oil & masala': 'FOM',
    'beverages': 'BEV',
    'bakery, cakes & dairy': 'BCD',
    'fruits & vegetables': 'FNV',
    'eggs, meat & fish': 'EMF',
    'baby care': 'BAB',
}

def generate_sku(row):
    """Generate clean SKU ID."""
    cat = str(row['category']).lower().strip()
    cat_code = CAT_CODES.get(cat, 'OTH')
    
    sub = str(row['sub_category']).strip()[:3].upper()
    sub = ''.join(c for c in sub if c.isalpha()) or 'GEN'
    
    return f"{cat_code}-{sub}-{row['index']:05d}"

df['sku_id'] = df.apply(generate_sku, axis=1)

# Clean product name
def clean_name(name):
    """Remove noise from product name."""
    if pd.isna(name):
        return ''
    name = str(name)
    
    # Remove common noise patterns
    patterns = [
        r'\s*-\s*\d+\s*(?:mg|g|gm|gram|kg|ml|l|litre|liter|pc|pcs|pack)s?\b',
        r'\s*\d+\s*(?:mg|g|gm|gram|kg|ml|l|litre|liter|pc|pcs|pack)s?\s*$',
        r'\s*\d+-\d+\s*(?:kg|g)\s*',  # Weight ranges
        r'\s*(?:vegetarian\s+)?capsule\s*',
        r'\s*\(pack of \d+\)\s*',
        r'\s*\(\s*\)',
    ]
    
    for pattern in patterns:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)
    
    return ' '.join(name.split()).strip()

df['product_name_clean'] = df['product'].apply(clean_name)

# =============================================================================
# FINAL OUTPUT
# =============================================================================

# Select and order columns
output_cols = [
    'index', 'sku_id', 'product', 'product_name_clean',
    'category', 'sub_category', 'brand', 'type',
    'sale_price', 'market_price', 'rating',
    # Physics
    'weight_g', 'volume_cm3', 'fragility_score', 'storage_type', 'spill_risk',
    # Time & Decay
    'shelf_life_hours', 'freshness_decay', 'prep_time_sec',
    # Psychology
    'brand_tier', 'impulse_score', 'substitute_group', 'morning_demand', 'evening_demand'
]

df_final = df[output_cols].copy()

# Save
df_final.to_csv('final.csv', index=False)

print("\n" + "="*70)
print("✓ SAVED TO final.csv")
print("="*70)
print(f"Total products: {len(df_final):,}")
print(f"Total columns: {len(df_final.columns)}")

print("\n" + "="*70)
print("VALIDATION SUMMARY")
print("="*70)

# Storage validation
print("\nStorage Distribution:")
print(df_final['storage_type'].value_counts().to_string())

# Weight validation
print("\nWeight Stats by Category:")
weight_stats = df_final.groupby('category')['weight_g'].agg(['mean', 'min', 'max']).round(0)
print(weight_stats.to_string())

# Shelf life validation
print("\nShelf Life by Storage:")
shelf_stats = df_final.groupby('storage_type')['shelf_life_hours'].agg(['mean', 'min', 'max']).round(0)
print(shelf_stats.to_string())

# Brand tier
print("\nBrand Tier Distribution:")
print(df_final['brand_tier'].value_counts().to_string())

print("\n" + "="*70)
print("SPOT CHECKS")
print("="*70)

# Check specific products
checks = [
    ("Milk", df_final[df_final['product'].str.contains('Milk', case=False, na=False) & 
                       ~df_final['product'].str.contains('Powder|Bikis|Coconut', case=False, na=False)]),
    ("Eggs", df_final[df_final['sub_category'] == 'Eggs']),
    ("Ice Cream", df_final[df_final['type'].str.contains('Ice Cream', case=False, na=False)]),
    ("Chips", df_final[df_final['type'].str.contains('Chips|Nachos', case=False, na=False)]),
    ("Rice", df_final[df_final['sub_category'].str.contains('Rice', case=False, na=False)]),
]

for name, subset in checks:
    if len(subset) > 0:
        print(f"\n{name} ({len(subset)} items):")
        print(f"  Storage: {dict(subset['storage_type'].value_counts())}")
        print(f"  Shelf Life: {subset['shelf_life_hours'].mean():.0f}h avg")
        print(f"  Morning/Evening Demand: {subset['morning_demand'].mean():.2f} / {subset['evening_demand'].mean():.2f}")
        print(f"  Weight: {subset['weight_g'].mean():.0f}g avg")
