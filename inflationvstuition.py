#!/usr/bin/env python
# coding: utf-8

# In[67]:


import pandas as pd 
tuition_data = pd.read_csv("schoolsdata.csv")
inflation_data = pd.read_csv("InflationRates.csv")

#first lets take the average value of the inflation rates in each year so that we can shorten down the data and make it more compact
# We Calculate average inflation rate by year
avg_inflation_by_year = inflation_data.groupby('Year')['Ave'].mean().reset_index()

# Display the average inflation rate by year
print(avg_inflation_by_year)


#Okay now we are gonna calculate the average value of the tuton rates statewise and shorten down the data 
# Group by 'State' and calculate the average tuition fee
avg_tuition_by_state = tuition_data.groupby("Year")['Value'].mean().reset_index().round(2)

# Display the average tuition fee by state
print(avg_tuition_by_state)

# Merge the two DataFrames on the common column (Year for inflation and State for tuition)
# This assumes you want to compare inflation rates and tuition fees on a yearly basis
merged_data = pd.merge(avg_inflation_by_year, avg_tuition_by_state, on='Year')

# Calculate correlation coefficient
correlation_coefficient = merged_data['Ave'].corr(merged_data['Value'])

print()

# Print correlation coefficient
print("The Correlation Coefficient between average inflation rates and average tuition fees:", correlation_coefficient)


#finally we are using some visulaisation to figure out how inflation and tution fees go together

import matplotlib.pyplot as plt

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot average tuition fees
ax1.plot(merged_data['Year'], merged_data['Value'], label='Average Tuition Fees', color='red')
ax1.set_xlabel('Year')
ax1.set_ylabel('Average Tuition Fees', color='red')
ax1.tick_params(axis='y', labelcolor='red')

# Create a secondary y-axis for inflation rates
ax2 = ax1.twinx()
ax2.plot(merged_data['Year'], merged_data['Ave'], label='Average Inflation Rate', color='blue')
ax2.set_ylabel('Average Inflation Rate', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

# Adding legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

# Adding title
plt.title('Average Inflation Rate vs Average Tuition Fees Over Time')

# Showing plot
plt.grid(True)
plt.show()



# In[61]:





# In[57]:





# In[15]:





# In[40]:





# In[ ]:





# In[ ]:




