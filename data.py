# import csv

# header = ['name', 'area', 'country_code2', 'country_code3']
# data = [
#     ['Albania', 28748, 'AL', 'ALB'],
#     ['Algeria', 2381741, 'DZ', 'DZA'],
#     ['American Samoa', 199, 'AS', 'ASM'],
#     ['Andorra', 468, 'AD', 'AND'],
#     ['Angola', 1246700, 'AO', 'AGO']
# ]

# with open('csv/log.csv', 'w', encoding='UTF8', newline='') as f:
#     writer = csv.writer(f)

#     # write the header
#     writer.writerow(header)

#     # write multiple rows
#     writer.writerows(data)

import pandas as pd
 
# data of Player and their performance
data = {
    'name': ['Hardik', 'Pollard', 'Bravo'],
    'area': [50, 63, ''],
    'country_code2': [0, 2, ''],
    'country_code3': [4, 2, '']
}
 
# Make data frame of above data
df = pd.DataFrame(data)
 
# append data frame to CSV file
df.to_csv('csv/countries.csv', mode='a', index=False, header=False)
 
# print message
print("Data appended successfully.")