# List of input files
input_files = [
    'jamii_users_SOC01.txt',
    'jamii_users_SOC02.txt',
    'jamii_users_SOC03.txt',
    'jamii_users_SOC04.txt'
]

# Set to store unique names
unique_names = set()

# Read each file and add names to the set
for file in input_files:
    with open(file, 'r') as f:
        for line in f:
            name = line.strip()
            if name:  # Avoid empty lines
                unique_names.add(name)

# Write the unique names to a new file
with open('jamii_users_SOC04.txt', 'w') as f:
    for name in sorted(unique_names):  # Sorting is optional
        f.write(f'{name}\n')

print(f'Combined {len(unique_names)} unique names into combined_jamii_users.txt')
