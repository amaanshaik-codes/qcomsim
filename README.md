I am Amaan Shaik, a 20 year old Business Analytics student at Tapasya Degree College, Hyderabad, India.
This is my first ever repository on Github, Actually I have created a few repositories before but never added a README file to them personally. 
This project is a simulation of a Quick Commerce platform using Agent Based Modelling (ABM) techniques.
As a business analytics student, the main objective of this project is to understand the dynamics of quick commerce platforms and how various factors influence their operations and customer satisfaction. 

I also got to experience working with huge datasets, cleaning them and preparing them for the simulation.




# Quick Commerce Simulation 

This a sandbox simulation uses Agent Based Modelling (ABM) to explore the dynamics of a quick commerce platform like Blinkit or Zepto. The simulation models the interactions between customers, delivery agents, and inventory to analyze factors such as delivery times, customer satisfaction, and operational efficiency. 

The user will be able to control various parameters of the simulation such as:
- Number of customers
- Number of delivery agents
- Inventory levels
- Pay per delivery agent
- Total cash to start with

## Agents
This project will combine a few variety of virtual characters that include:
- Customers: who place orders for groceries and other essentials.
- Delivery Agents: who pick up orders from warehouses and deliver them to customers. 
- Pickers: who are responsible for collecting items from the warehouse shelves to fulfill customer orders. 
- Warehouses: which store the inventory and manage stock levels of the entire city operations.
- Darkstores: small fulfillment centres located across the city for faster delivery times. 

To understand how this simulation works, we will be using the Mesa Framework, a popular Python library for building agent-based models.

There are some .csv files that will be used as a payload for this simulation. These payload will contain the data necessary for this simulation to run properly. While the title of this project is Quick Commerce Simulation, the data used as the payload is taken from two different sources: 

1. An actual quick commerce inventory dataset obtained from Kaggle. This dataset contains over 20k SKUs covering wide variety of categories and sub-categories. 
2. A synthetic customer dataset generated using Python libraries such as Faker and Pandas. This dataset contains over 50k unique customer profiles with various attributes.

## Payload 
We need to simulate a virtual city with multiple agents interacting with each other. And to simulate a city we need to have data about the entities present in the city. The payload is not business's actual data, but rather datasets that mimic real world data to create a realistic simulation environment.  

 To do this, we will be using the following payload files:

### customer_profiles.csv
There are a total of 150,000 synthetic customers with their own unique characteristics and demographics generated randomly and stored in the file named `customers.csv`. This contains few sensitive attributes like customer's religion, income, family size etc which were added to make this simulation realistic, and it may not be a standard practice to collect in real-world scenarios. Although this data is randomly generated, it was created by following real distribution of demographics in Hyderabad, India. 

Customers will have data attributes such as:
    1. customer_id
    2. first_name
    3. last_name
    4. full_name
    5. gender
    6. age
    7. birth_year
    8. community
    9. phone
    10. email
    11. locality
    12. city
    13. state
    14. pincode
    15. latitude
    16. longitude
    17. household_size
    18. monthly_income
    19. annual_income
    20. income_bracket
    21. customer_segment
    22. lifestyle
    23. brand_preference
    24. cooking_frequency
    25. health_consciousness
    26. price_sensitivity
    27. tech_savviness
    28. impulse_tendency
    29. weekend_preference
    30. orders_per_month
    31. avg_basket_value
    32. primary_order_hour
    33. account_created date
    34. last_order_date
    35. lifetime_orders
    36. lifetime_value
    37. loyalty_tier
    38. app_sessions_monthly
    39. preffered_payment
    40. preffered_delivery
    41. has_subscription
    42. preffered_category_1
    43. preffered_category_2
    44. avg_items_per_order
    45. morning_order_tendency
    46. evening_order_tendency

### products.csv
This dataset contains over 20,000 unique products available in the quick commerce platform's inventory. Each product has various attributes such as:
    1. index
    2. sku_id
    3. product
    4. product_name_clean
    5. category
    6. sub_category
    7. brand
    8. type
    9. sale_price
    10. market_price
    11. rating
    12. rating
    13. weight_g
    14. volume_cm3
    15. fragility_score
    16. storage_type
    17. spill_risk_hours
    18. freshness_decay
    19. prep_time_sec
    20. brand_tier
    21. impulse_score
    22. substitute_group
    23. morning_demand
    24. evening_demand

### rider_profiles.csv
A total of 8500 delivery agents with unique attributes such as:
    1. rider_id
    2. first_name
    3. last_name
    4. full_name
    5. gender
    6. age
    7. phone_number
    8. email
    9. community
    10. vehicle type
    11. vehicle_number
    12. engine_cc
    13. home_store_id
    14. service_zone
    15. home_lat
    16. home_lng
    17. rider_segment
    18. shift_type
    19. shift_start
    20. shift_end
    21. experience_months
    22. join_date_
    23. status
    24. last_active
    25. on_time_delivery_rate
    26. order_acceptance_rate
    27. cancellation_rate
    28. average_delivery_time_mins
    29. customer_rating
    30. total_orders_delivered
    31. daily_avg_orders
    32. total_earnings
    33. avg_earnings_per_order
    34. peak_hour_preference
    35. weekend_availability
    36. has_insulated_bag
    37. has_rain_gear
    38. knows_english
    39. knows_english
    40. knows_hindi 
    41. knows_telugu



### picker_profiles.csv
a total of 300 pickers with unique attributes such as:
    1. picker_id
    2. first_name
    3. last_name
    4. full_name
    5. gender
    6. age
    7. phone_number
    8. email
    9. community
    10. store_id
    11. store_name
    12. service_zone
    13. picker_segment
    14. role
    15. shift_type
    16. shift_start
    17. shift_end
    18. experience_months
    19. join_date
    20. status
    21. last_active
    22. avg_picking_time_sec
    23. items_per_hour
    24. daily_orders_picked
    25. accuracy_rate
    26. mispick_rate
    27. total_orders_picked
    28. total_items_picked
    29. total_mispicks
    30. hourly_rate
    31. total_earnings
    32. total_hours_worked
    33. zone_familiarity
    32. multitask_ability
    33. physical_fitness
    34. temperature_zone_trained
    35. fragile_handling_certified




