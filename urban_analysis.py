import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuration ---
# Provided survey.dict (mapping original TPURP to simplified land use codes)
survey_dict_provided = {
    1: 1, 2: 1, 3: 6, 4: 6, 5: 4, 6: 4, 7: 11, 8: 11, 9: 11, 10: 11, 11: 6,
    12: 6, 13: 9, 14: 9, 15: 11, 16: 6, 17: 9, 18: 7, 19: 8, 20: 10, 21: 1,
    24: 11, 97: 12
}

# Optional: Define names for your simplified land use codes if you know them from the paper
# This will make plots more readable. Example:
land_use_code_names = {
    1: "Residential",
    2: "Residential - Other Home Activities",
    21: "Residential - Visit Friends & Relatives",
    3: "Work/Job",
    4: "Work - Other Activities",
    11: "Work - Business Related",
    12: "Service - Private Vehicle",
    16: "Personal Business",
    5: "Education - Attending Class",
    6: "Education - Other School Activities",
    7: "Transportation - Change Type/Transfer",
    8: "Transportation - Dropped Off Passenger",
    9: "Transportation - Picked Up Passenger",
    10: "Transportation - Other",
    13: "Shopping - Routine",
    14: "Shopping - Major Purchases",
    17: "Shopping - Eat Meal Outside",
    18: "Service - Health Care",
    19: "Civic/Religious Activities",
    20: "Recreation/Entertainment",
    24: "Recreation - Loop Trip",
    97: "Other/Specify",
    # Not identifiable categories omitted or marked as undefined
    "Hotel": "Unknown/Undefined",
    "Land Use Mix": "Unknown/Undefined",
    "Universities": "Unknown/Undefined"
}


# File paths (adjust if your files are elsewhere)
file_survey = '580081\D2_survey_pr.csv\D2_survey_pr.csv'
file_tweets_macro = '580081\D3_macro_signatures.csv\D3_macro_signatures.csv'
file_tweets_clusters = '580081/D4_clusters_signatures.csv/D4_clusters_signatures.csv'

# --- Helper Function for Plotting ---
def save_plot(title, filename):
    plt.savefig(filename, bbox_inches='tight')
    print(f"Saved plot: {filename}")
    plt.close()

# --- Phase 1: Analyzing Traditional Survey Data (D2_survey_pr.csv) ---
print("\n--- Phase 1: Analyzing Traditional Survey Data ---")

try:
    df_survey = pd.read_csv(file_survey)

    # Map TPURP to simplified land use codes
    df_survey['land_use_code'] = df_survey['TPURP'].map(survey_dict_provided)

    # Drop rows where mapping didn't occur (if any TPURP not in dict)
    df_survey.dropna(subset=['land_use_code'], inplace=True)
    df_survey['land_use_code'] = df_survey['land_use_code'].astype(int)

    # Use defined names if available, otherwise use codes
    df_survey['land_use_label'] = df_survey['land_use_code'].map(land_use_code_names).fillna(df_survey['land_use_code'].astype(str))


    print("\nSurvey Data: Basic Info")
    df_survey.info()
    print("\nSurvey Data: Sample Data with Land Use Code")
    print(df_survey[['TPURP', 'ACTDUR', 'land_use_code', 'land_use_label']].head())

    # 1. Descriptive Statistics of Activity Duration (ACTDUR) per Land Use
    print("\nSurvey Data: Activity Duration (ACTDUR) Statistics per Land Use")
    survey_actdur_stats = df_survey.groupby('land_use_label')['ACTDUR'].agg(['mean', 'median', 'std', 'count']).sort_values(by='median', ascending=False)
    print(survey_actdur_stats)

    # 2. Visualize Activity Duration Distributions
    # Box plot for ACTDUR by land use
    plt.figure(figsize=(14, 8))
    sns.boxplot(x='land_use_label', y='ACTDUR', data=df_survey, order=survey_actdur_stats.index) # Order by median duration
    plt.title('Survey: Activity Duration (ACTDUR) by Land Use')
    plt.xlabel('Land Use Type')
    plt.ylabel('Activity Duration (minutes)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    save_plot('Survey Activity Duration by Land Use', 'survey_actdur_boxplot.png')


    # Histograms/KDEs for ACTDUR for each land use (showing top N for brevity)
    print("\nGenerating Survey Activity Duration Histograms...")
    top_n_land_uses = survey_actdur_stats.head(6).index # Visualize top 6 by median duration
    for luc_label in top_n_land_uses:
        plt.figure(figsize=(8, 5))
        subset = df_survey[df_survey['land_use_label'] == luc_label]
        # Limit duration for better visualization if there are extreme outliers
        sns.histplot(subset[subset['ACTDUR'] < subset['ACTDUR'].quantile(0.99)]['ACTDUR'], kde=True, bins=30)
        plt.title(f'Survey: Activity Duration Distribution for {luc_label}')
        plt.xlabel('Activity Duration (minutes)')
        plt.ylabel('Frequency')
        plt.tight_layout()
        save_plot(f'Survey Activity Duration for {luc_label}', f'survey_actdur_hist_{luc_label.replace("/", "_")}.png')

except FileNotFoundError:
    print(f"Error: Survey data file '{file_survey}' not found.")
except Exception as e:
    print(f"An error occurred during survey data analysis: {e}")


# --- Phase 2: Analyzing Twitter Data ---
print("\n\n--- Phase 2: Analyzing Twitter Data ---")

# --- Analyzing D3_macro_signatures.csv (Individual Tweets) ---
print("\n--- Analyzing D3_macro_signatures.csv (Tweet-level) ---")
try:
    df_tweets_macro = pd.read_csv(file_tweets_macro)
    # Assuming 'luse' in D3 is already the simplified code (1-12)
    # If not, you'd need to map it similarly to survey data
    df_tweets_macro['land_use_label'] = df_tweets_macro['luse'].map(land_use_code_names).fillna(df_tweets_macro['luse'].astype(str))


    print("\nTwitter Macro Data: Basic Info")
    df_tweets_macro.info()
    print("\nTwitter Macro Data: Sample Data with Land Use")
    print(df_tweets_macro[['luse', 'hour', 'dow', 'land_use_label']].head())

    # 1. Hourly Tweet Patterns per Land Use
    print("\nGenerating Twitter Macro Hourly Tweet Pattern Plots...")
    hourly_tweets_macro = df_tweets_macro.groupby(['land_use_label', 'hour']).size().reset_index(name='tweet_count')

    plt.figure(figsize=(15, 9))
    for luc_label in hourly_tweets_macro['land_use_label'].unique():
        subset = hourly_tweets_macro[hourly_tweets_macro['land_use_label'] == luc_label]
        # Normalize tweet counts per land use for better comparison if desired
        # subset['tweet_count_normalized'] = subset['tweet_count'] / subset['tweet_count'].sum()
        plt.plot(subset['hour'], subset['tweet_count'], label=luc_label, marker='o', linestyle='-')
    plt.title('Twitter (D3): Hourly Tweet Counts by Land Use')
    plt.xlabel('Hour of Day (0-23)')
    plt.ylabel('Total Tweet Count')
    plt.xticks(range(24))
    plt.legend(title='Land Use', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    save_plot('Twitter D3 Hourly Patterns', 'twitter_d3_hourly_patterns.png')


    # 2. Day of the Week (dow) Tweet Patterns per Land Use
    # dow: 1 for Sunday, 2 for Monday, ..., 7 for Saturday
    print("\nGenerating Twitter Macro Day of Week Tweet Pattern Plots...")
    dow_tweets_macro = df_tweets_macro.groupby(['land_use_label', 'dow']).size().reset_index(name='tweet_count')
    dow_names = {1: 'Sun', 2: 'Mon', 3: 'Tue', 4: 'Wed', 5: 'Thu', 6: 'Fri', 7: 'Sat'}
    dow_tweets_macro['day_name'] = dow_tweets_macro['dow'].map(dow_names)

    plt.figure(figsize=(15, 9))
    # Using seaborn for easier categorical plotting here
    sns.lineplot(data=dow_tweets_macro, x='day_name', y='tweet_count', hue='land_use_label', marker='o', sort=False)
    plt.title('Twitter (D3): Tweet Counts by Day of Week and Land Use')
    plt.xlabel('Day of Week')
    plt.ylabel('Total Tweet Count')
    plt.legend(title='Land Use', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    save_plot('Twitter D3 Day of Week Patterns', 'twitter_d3_dow_patterns.png')


except FileNotFoundError:
    print(f"Error: Twitter macro data file '{file_tweets_macro}' not found.")
except Exception as e:
    print(f"An error occurred during Twitter macro data analysis: {e}")


# --- Analyzing D4_clusters_signatures.csv (Aggregated Cluster Signatures) ---
print("\n\n--- Analyzing D4_clusters_signatures.csv (Cluster-level Hourly) ---")
try:
    df_clusters = pd.read_csv(file_tweets_clusters)
    # The column name for land use is 'land use' (with a space)
    df_clusters.rename(columns={'land use': 'land_use_code'}, inplace=True)
    df_clusters['land_use_label'] = df_clusters['land_use_code'].map(land_use_code_names).fillna(df_clusters['land_use_code'].astype(str))

    print("\nTwitter Cluster Data: Basic Info")
    df_clusters.info()
    print("\nTwitter Cluster Data: Sample Data")
    print(df_clusters[['land_use_code', 'land_use_label', 'h0', 'h1', 'h23']].head())

    hourly_cols = [f'h{i}' for i in range(24)]

    # Aggregate hourly counts per land use type (summing tweets from all clusters of that type)
    cluster_hourly_agg = df_clusters.groupby('land_use_label')[hourly_cols].sum()

    plt.figure(figsize=(15, 9))
    for luc_label, row_data in cluster_hourly_agg.iterrows():
        plt.plot(range(24), row_data.values, label=luc_label, marker='.', linestyle='-')
    plt.title('Twitter (D4): Aggregated Hourly Tweet Patterns by Land Use (Sum of Cluster Tweets)')
    plt.xlabel('Hour of Day (0-23)')
    plt.ylabel('Aggregated Tweet Count')
    plt.xticks(range(24))
    plt.legend(title='Land Use', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    save_plot('Twitter D4 Aggregated Hourly Patterns', 'twitter_d4_hourly_patterns.png')


except FileNotFoundError:
    print(f"Error: Twitter cluster data file '{file_tweets_clusters}' not found.")
except Exception as e:
    print(f"An error occurred during Twitter cluster data analysis: {e}")


print("\n\n--- Analysis Complete ---")
print("Please check the generated .png files for visualizations.")
print("Now, visually compare the survey data plots (activity durations) with Twitter data plots (temporal tweet patterns).")
print("Consider questions like:")
print(" - Do land uses with longer survey activity durations also show prolonged Twitter activity peaks?")
print(" - Are peak Twitter activity times consistent with how you'd expect those land uses to be busy?")
print(" - How do weekday/weekend patterns from Twitter (D3) align with general expectations for different land uses?")