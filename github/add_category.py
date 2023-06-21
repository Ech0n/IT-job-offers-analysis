import pandas as pd
import re
category_dict = {
            'programming language' : 'programming language',
            'scripting language' : 'scripting language',
            'superset of JavaScript': 'programming language',
            'library' : 'library',
            'SQL' : 'SQL',
            'automation' : 'automation',
            'automated' : 'automation',
            'automate' : 'automation',
            'automating' : 'automation',
            'framework' : 'framework',
            'tool' : 'framework',
            'database' : 'database',
            'game' : 'game',
            
            'operating system' : 'operating system',
            
            'build' : 'automation',
            'command-line' : 'command-line',
            'commands' : 'command-line',
            'learning' : 'learning',
            'control' : 'control',
            'cloud' : 'cloud',
            'web' : 'web',
            'language': 'language',
            'graphics' : 'graphics',
            'javascript': 'framework',
            'java' : 'framework',
            'css' : 'web',
            'data' : 'data',
            'library' : 'framework',
            'open source': 'open source',
            'front end' : 'web',
            '' : 'other'
        }

df = pd.read_csv('github_data29_05_2023.csv')
category = []
for d in df['desc']:
            for key in category_dict.keys():
                if key.lower() in d.lower():
                    if key != '':
                        category.append(category_dict[key])
                    else: category.append('other')
                    break
df.insert(2, "category", category)

def replaceMethod(value : str):
    if 'k' in value:
            value = value.replace('k', '000')
    return value

df['stars'] = df['stars'].replace('k', '', regex=True)
df['stars'] = df['stars'].apply(lambda x : int(float(x) * 1000))

df = df.drop(columns=['Unnamed: 0'])


df.to_csv("github_data29_05_2023_with_category.csv")