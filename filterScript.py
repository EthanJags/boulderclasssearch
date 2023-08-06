import pandas as pd

# Load the CSV file
df = pd.read_csv('CUScrape_with_embeddingsformatted.csv')

# Function to classify class code
def classify_class_type(class_code):
    class_number = int(class_code.split(' ')[1][0]) # Split class code and get the first digit of the number

    if class_number in [1, 2]:
        return ['lower']
    elif class_number in [3, 4]:
        return ['upper']
    elif class_number in [5, 6]:
        return ['masters']
    elif class_number in [7, 8]:
        return ['doctorate']
    else:
        return ['other']

# Apply the function to the class code column
df['Class Type'] = df['Class Code'].apply(classify_class_type)

# Save the modified dataframe to a new CSV file
df.to_csv('CUScrapeFilters.csv', index=False)
