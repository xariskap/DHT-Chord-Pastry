from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pandas as pd
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression




def importData():
    df =pd.read_excel('./tour_occ_ninat.xlsx')
    

    # Isoalation of useful data
    df = df.rename(columns=df.loc[7])
    df = df.loc[8:]
    df= df.replace(':',None)
    df_original = df.transpose()
    
    #Reorganize dataframe after transpose
    df_original.reset_index(inplace=True)
    df_original = df_original.rename(columns=df_original.loc[0])
    df_original = df_original.loc[1:]
    print(df_original.isnull().sum().sort_values(ascending=False))

    df_original['Switzerland'] = df_original['Switzerland'].fillna(0)
    df_original['Turkey'] = df_original['Turkey'].fillna(df_original['Turkey'].mean())
    df_original['Montenegro'] = df_original['Montenegro'].fillna(df_original['Montenegro'].mean())
    df_original['Serbia'] = df_original['Serbia'].fillna(df_original['Serbia'].mean())
    df_original['Ireland'] = df_original['Ireland'].fillna(df_original['Ireland'].mean())
    df_original['United Kingdom'] = df_original['United Kingdom'].\
        fillna(df_original['United Kingdom'].mean())
    df_original['Former Yugoslav Republic of Macedonia, the'] =\
          df_original['Former Yugoslav Republic of Macedonia, the'].\
            fillna(df_original['Former Yugoslav Republic of Macedonia, the'].mean())
    #None value handling
    """ for index,row in df_original.iterrows():
        df_original.loc[index] = df_original.loc[index].fillna(df_original.loc[index].mean()) """
    return df_original

df = importData()
print(df.head(10))

spark = SparkSession.builder.appName('W1').getOrCreate()

sdf = spark.createDataFrame(df)
# Filter the DataFrame to include only the years from 2007 to 2014
filtered_df = sdf.filter((F.col("GEO/TIME") >= 2007) & (F.col("GEO/TIME") <= 2014))

# Calculate the mean for each country
mean_df = filtered_df.select(
    [F.mean(col_name).alias(col_name) for col_name in sdf.columns[1:]]
)
mean_df.show(20)
# Next steps
#Pivot the table
# Get the mean of the table
# Replace every missing value