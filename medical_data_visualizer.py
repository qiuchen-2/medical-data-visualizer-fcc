import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('medical_examination.csv')

# 2
# Height is currently in cm, convert to m using 1m = 100cm (so [cm]*[1m/100cm])
df['height'] = df['height']/100

# Calculate their BMI = weight [kg]/(height^2) [m^2]
df['BMI'] = df['weight']/(df['height']**2)

#If the BMI > 25 the person is overweight (return 0 for NOT and 1 for overweight)
df['overweight'] = df['BMI'].apply(lambda x: 1 if x>25 else 0)

# 3: Normalize the data so 0 is always good and 1 is always bad. If gluc or cholestrol is 1, set value to 0. If value is more than 1, set to 1
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x ==1 else 1)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x ==1 else 1)

# 4 Draw the Categorical Plot
def draw_cat_plot():
    # 5
    df_cat= pd.melt(df, id_vars=['cardio'], value_vars = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # 6
    df_cat['total'] = 1
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).count()
    

    # 7
    fig = sns.catplot(data = df_cat, x= "variable", y= 'total', hue= 'value', kind='bar', col= 'cardio').fig


    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & 
                (df['height'] >= df['height'].quantile(0.025)) & 
                (df['height'] <= df['height'].quantile(0.975)) & 
                (df['weight'] >= df['weight'].quantile(0.025)) & 
                (df['weight'] <= df['weight'].quantile(0.975))
                ]

    # 12
    corr = df_heat.corr()

    # 13
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14
    fig, ax = plt.subplots(figsize=(12,12))

    # 15
    sns.heatmap(corr, mask=mask, annot=True, fmt='.1f', center=0, square=True, linewidths=1)  


    # 16
    fig.savefig('heatmap.png')
    return fig
