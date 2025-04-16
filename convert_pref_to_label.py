import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

ANNOTATORS = [
    'kushan',
    'dz',
    'hannah'
]
df = pd.read_csv('data.csv')
averaged_df_counts = None

for annotator in ANNOTATORS:
    selection_file = f'selections_{annotator}.csv'
    selections = pd.read_csv(selection_file)
    df['choice'] = selections['choice']
    
    df["{}_label".format(annotator)] = df.apply(lambda row: "tie" if row["choice"].lower() == "tie" else 
                                               "plan_from_rewrite" if row["choice"] == row["rewrite_label"] else 
                                               "plan_from_conv", axis=1)
    df_counts = df.groupby("challenge")["{}_label".format(annotator)].value_counts().unstack(fill_value=0)
    category_order = ["num_rounds_short", "num_rounds_medium", "num_rounds_long", "intent_shift", "noisy"]
    df_counts = df_counts.reindex(category_order)
    column_order = ["plan_from_conv", "tie", "plan_from_rewrite"]
    df_counts = df_counts[column_order]

    if averaged_df_counts is None:
        averaged_df_counts = df_counts
    else:
        averaged_df_counts += df_counts  

    df = df.drop(columns=['choice'])

df.to_csv('data_labeled.csv', index=False)  

averaged_df_counts = averaged_df_counts / len(ANNOTATORS)
df_percentages = averaged_df_counts.div(averaged_df_counts.sum(axis=1), axis=0) * 100

palette = sns.color_palette("Set2", 3)  
colors = {"plan_from_conv": palette[0], "tie": "gray", "plan_from_rewrite": palette[2]}

ax = df_percentages.plot(kind="bar", figsize=(10,6), color=[colors[col] for col in column_order], width=0.8)
plt.ylabel("Average Preference Percentage")
plt.legend(title="Preference Label")
plt.xticks(rotation=360, fontsize=6)
plt.show()
# averaged_df_counts.to_csv('averaged_data.csv', index=True)