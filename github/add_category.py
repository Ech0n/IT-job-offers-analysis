import pandas as pd
colors_dict = {
            'programming' : '#2F3C7E',
            'SQL' : '#99F443',
            'framework' : '#FEE715',
            'database' : '#CCF381',
            'game' : '#00FFFF',
            'open source': 'green',
            'operating system' : 'blue',
            'automation' : '#CBD18F',
            'command-line' : 'yellow',
            'learning' : 'purple',
            'control' : '#FFA351',
            'cloud' : '#8A307F',
            'web' : '#201E20',
            'language': '#1E2761',
            'graphics' : 'pink',
            '' : 'red'
        }

df = pd.read_csv('github_data29_05_2023.csv')
category = []
for d in df['desc']:
            for key in colors_dict.keys():
                if key.lower() in d.lower():
                    if key != '':
                        category.append(key)
                    else: category.append('other')
                    break
df.insert(2, "category", category)

df.to_csv("github_data29_05_2023_with_category.csv")