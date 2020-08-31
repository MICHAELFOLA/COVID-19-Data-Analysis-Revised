import tabula
import pandas as pd

file_pattern = 'county_reports'
date = '20200524'
path_to_csv = f'{file_pattern}_{date}.csv'
data = pd.read_csv(path_to_csv)

# Race/Ethnicity column
RaceEth = ['Total White',
           'White Hispanic',
           'White Non-Hispanic',
           'White Unknown',
           'Total Black',
           'Black Hispanic',
           'Black Non-Hispanic',
           'Black Unknown',
           'Total Other',
           'Other Hispanic',
           'Other Non-Hispanic',
           'Other Unknown',
           'Total Unknown',
           'Unknown Hispanic',
           'Unknown Non-Hispanic',
           'Unknown Unknown',
           'Total All'
           ]

# County names for forming column names
countyNames = ['Alachua',
               'Baker',
               'Bay',
               'Bradford',
               'Brevard',
               'Broward',
               'Calhoun',
               'Charlotte',
               'Citrus',
               'Clay',
               'Collier',
               'Columbia',
               'DeSoto',
               'Dixie',
               'Duval',
               'Escambia',
               'Flagler',
               'Franklin',
               'Gadsden',
               'Gilchrist',
               'Glades',
               'Gulf',
               'Hamilton',
               'Hardee',
               'Hendry',
               'Hernando',
               'Highlands',
               'Hillsborough',
               'Holmes',
               'Indian River',
               'Jackson',
               'Jefferson',
               'Lafayette',
               'Lake',
               'Lee',
               'Leon',
               'Levy',
               'Liberty',
               'Madison',
               'Manatee',
               'Marion',
               'Martin',
               'Miami-Dade',
               'Monroe',
               'Nassau',
               'Okaloosa',
               'Okeechobee',
               'Orange',
               'Osceola',
               'Palm Beach',
               'Pasco',
               'Pinellas',
               'Polk',
               'Putnam',
               'Santa Rosa',
               'Sarasota',
               'Seminole',
               'St. Johns',
               'St. Lucie',
               'Sumter',
               'Suwannee',
               'Taylor',
               'Union',
               'Volusia',
               'Wakulla',
               'Walton',
               'Washington']

allCounties = []

for i in countyNames:
    name = i + " Cases"
    allCounties.append(name)
    name = i + " Hospitalizations"
    allCounties.append(name)
    name = i + " Deaths"
    allCounties.append(name)

# Creates empty data frame using these as columns
final = pd.DataFrame(columns=allCounties, index=RaceEth)

pattern_length = 17


# function for carving up main DF into mini DF
def create_df1(dataframe, row, col):
    df1 = dataframe.iloc[row:row + pattern_length, col].copy()
    df1.index = RaceEth
    return df1


# # carves up main DF into mini DF, then collates them back into the main DF
col = 0
row = 0

# To get the rows stacked side-by-side
# 1206 rows in "data", 67 * 18 = 1206
lower = 0
for i in range(lower, len(data), pattern_length+1):
    for j in range(3):
        final.iloc[lower:pattern_length, j + col] = create_df1(data, i, j + 1)

    col += 3

# the new, formatted df spanning many many columns is "final"
save_file = 'side_by_side.csv'
try:
    final.to_csv(save_file, index=True, header=True)
except (PermissionError, FileExistsError) as e:
    print(f'{save_file} already exists')

# To get the rows in separate files (cases, deaths, hospitalizations)
# columns = RaceEth
# rows = counties
cases_df = pd.DataFrame(columns=RaceEth, index=countyNames)
deaths_df = pd.DataFrame(columns=RaceEth, index=countyNames)
hospitalizations_df = pd.DataFrame(columns=RaceEth, index=countyNames)

categories = [cases_df, deaths_df, hospitalizations_df]

row = 0

for i in range(lower, final.shape[1], 3):
    for j in range(len(categories)):
        categories[j].iloc[row, lower:pattern_length] = final.iloc[lower:pattern_length, i + j]

    row += 1

# to save the dataframes to files
cases_file = 'Cases.csv'
deaths_file = 'Deaths.csv'
hospitalizations_file = 'Hospitalizations.csv'

try:
    cases_df.to_csv(cases_file, index=True, header=True)
except (PermissionError, FileExistsError) as e:
    print(f'{cases_file} already exists')

try:
    deaths_df.to_csv(deaths_file, index=True, header=True)
except (PermissionError, FileExistsError) as e:
    print(f'{deaths_file} already exists')

try:
    hospitalizations_df.to_csv(hospitalizations_file, index=True, header=True)
except (PermissionError, FileExistsError) as e:
    print(f'{hospitalizations_file} already exists')
