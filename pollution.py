#pollution.py library----

import numpy as np

#######################################################################
# Function: calc_total_emissions
# Description: Calculates the total amount of emissions
# Parameters: The values of all pollutants (nitrogen oxide, sulphur dioxide, carbon monoxide, organic carbon, nmvocs, black carbon, and ammonia)
# Return values: The sum of all the pollutants
# Pre-Conditions: The values are all real, whole numbers
# Post-Conditions: The sum of all the pollutants is a real, whole number
#######################################################################
def calc_total_emissions(nitrogen, sulfur, carbon, organic, nmvocs, black, ammonia):
    return nitrogen + sulfur + carbon + organic + nmvocs + black + ammonia

#######################################################################
# Function: percent_change_first_last_year
# Description: Calculates the percent change of the air pollution's emission value between 1750 (first value) to 2019 (last value)
# Parameters: df (pollution data), country (country name), pollutant (pollutant name)
# Return values: The percent change, as well as the values for the first year (1750) and last year (2019)
# Pre-Conditions: The pollutant must be one of the ones listed above
# Post-Conditions: The percent change is a real, whole number (and the period from 1750 to 2019 is valid)
#######################################################################
def percent_change_first_last_year(df, country, pollutant):
    country_data = df[df['Country'] == country].sort_values('Year')
    first = country_data[pollutant].iloc[0]
    last = country_data[pollutant].iloc[-1]
    change = ((last - first) / first) * 100
    start_year = country_data['Year'].iloc[0]
    end_year = country_data['Year'].iloc[-1]
    return change, start_year, end_year

#######################################################################
# Function: yearly_country_totals
# Description: Finds the yearly total emissions and pollutant totals for a specific country (this being the United States)
# Parameters: df (pollution data), country (country name), pollutant (pollutant name)
# Return values: The yearly lists of totals for the country
# Pre-Conditions: Each of the values sought for exist in the data set
# Post-Conditions: The yearly lists of totals for the country all exist
#######################################################################
def yearly_country_totals(df, country, pollutant):
    years, total_emissions, pollutant_emissions = [], [], []
    country_data = df[df['Country'] == country]
    unique_years = sorted(country_data['Year'].unique())
    for year in unique_years:
        year_data = country_data[country_data['Year'] == year]
        total = 0
        for _, row in year_data.iterrows():
            total += calc_total_emissions(
                row['Nitrogen Oxide'], row['Sulphur Dioxide'], row['Carbon Monoxide'], 
                row['Organic Carbon'], row['NMVOCs'], row['Black Carbon'], row['Ammonia']
            )
        pollutant_sum = year_data[pollutant].sum()
        years.append(year)
        total_emissions.append(total)
        pollutant_emissions.append(pollutant_sum)
    return years, total_emissions, pollutant_emissions

#######################################################################
# Function: analyze_pollution_for_country
# Description: Calculates average and max total pollution for a specific country (this being the United States)
# Parameters: df (pollution data), country (country name)
# Return values: The list of years analyzed, average pollution value, and the max pollution number
# Pre-Conditions: Each of the values sought for exist in the data set
# Post-Conditions: The pollution data is valid for the specific country (United States)
#######################################################################
def analyze_pollution_for_country(df, country):
    country_data = df[df['Country'] == country]
    years = country_data['Year'].values
    totals = []
    for _, row in country_data.iterrows():
        total = calc_total_emissions(
            row['Nitrogen Oxide'], row['Sulphur Dioxide'], row['Carbon Monoxide'], 
            row['Organic Carbon'], row['NMVOCs'], row['Black Carbon'], row['Ammonia']
        )
        totals.append(total)
    avg_total = np.mean(totals)
    max_total = np.max(totals)
    return years, avg_total, max_total

#######################################################################
# Function: average_pollution_by_country
# Description: Finds and stores average total pollution for each country for future use
# Parameters: df (pollution data), top_n=10 (top 10 countries needed to analyze)
# Return values: The average air pollution emission data by each country
# Pre-Conditions: Each of the values sought for exist in the data set
# Post-Conditions: The average air pollution emission data by each country
#######################################################################
def average_pollution_by_country(df, top_n=10):
    exclude = {"Asia", "Europe", "World", "Upper-middle-income countries", "Lower-middle-income countries", "High-income countries", "Low-income countries", "North America", "Africa", "South America"}
    country_sums, country_counts = {}, {}
    for _, row in df.iterrows():
        country = row['Country']
        if country not in exclude:
            total = calc_total_emissions(
                row['Nitrogen Oxide'], row['Sulphur Dioxide'], row['Carbon Monoxide'], 
                row['Organic Carbon'], row['NMVOCs'], row['Black Carbon'], row['Ammonia']
            )
            country_sums[country] = country_sums.get(country, 0) + total
            country_counts[country] = country_counts.get(country, 0) + 1
    averages = []
    for country in country_sums:
        avg = country_sums[country] / country_counts[country]
        averages.append((country, avg))
    averages.sort(key=lambda x: x[1], reverse=True)
    return averages[:top_n]

#######################################################################
# Function: get_top_polluters
# Description: Takes the data from the previous function and gathers the top polluting countries and their respective average pollution amounts
# Parameters: df (pollution data), top_n=10 (top 10 countries with high emissions)
# Return values: The list of country names as well as their average pollution values
# Pre-Conditions: Each of the values sought for exist in the data set
# Post-Conditions: The list of country names as well as their average pollution values
#######################################################################
def get_top_polluters(df, top_n=10):
    top_list = average_pollution_by_country(df, top_n)
    countries = [item[0] for item in top_list]
    values = [item[1] for item in top_list]
    return countries, values
