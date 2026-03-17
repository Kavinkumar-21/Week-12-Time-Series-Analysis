def nulltypeconversion(filename):
    import pandas as pd
    import numpy as np
    dataset=pd.read_csv(filename)
    dataset=dataset.drop('Temp',axis=1)
    for column in dataset.columns:
        dataset[column]=dataset[column].replace("None",np.nan)
    dataset["From Date"]=pd.to_datetime(dataset["From Date"],infer_datetime_format=True)
    dataset["To Date"]=pd.to_datetime(dataset["To Date"],infer_datetime_format=True)
    columnname=dataset.columns[2:(len(dataset.columns))]
    for columns in columnname:
        dataset[columns]=pd.to_numeric(dataset[columns])
    import numpy as np
    from sklearn.impute import SimpleImputer
    imputer=SimpleImputer(missing_values=np.nan,strategy='mean') 
    imputer.fit(dataset.iloc[:,2:len(dataset.columns)])
    dataset.iloc[:,2:len(dataset.columns)]=imputer.transform(dataset.iloc[:,2:len(dataset.columns)])
    #dataset.to_csv("{}Pre.csv".format(filename),index=False)
    return dataset
def nulltypeconversionTemp(filename):
    import pandas as pd
    import numpy as np
    dataset=pd.read_csv(filename)
    #dataset=dataset.drop('Temp',axis=1)
    for column in dataset.columns:
        dataset[column]=dataset[column].replace("None",np.nan)
    dataset["From Date"]=pd.to_datetime(dataset["From Date"],infer_datetime_format=True)
    dataset["To Date"]=pd.to_datetime(dataset["To Date"],infer_datetime_format=True)
    columnname=dataset.columns[2:(len(dataset.columns))]
    for columns in columnname:
        dataset[columns]=pd.to_numeric(dataset[columns])
    import numpy as np
    from sklearn.impute import SimpleImputer
    imputer=SimpleImputer(missing_values=np.nan,strategy='mean') 
    imputer.fit(dataset.iloc[:,2:len(dataset.columns)])
    dataset.iloc[:,2:len(dataset.columns)]=imputer.transform(dataset.iloc[:,2:len(dataset.columns)])
    #dataset.to_csv("{}Pre.csv".format(filename),index=False)
    return dataset

def AirCalculation(dataset,filename):
    import pandas as pd
    dataset.index=dataset["From Date"]
    dataset.index = pd.to_datetime(dataset.index)
    dataset=dataset.resample('D').mean()
    daily_pollutants=dataset[["PM10","CO","PM2.5","NH3","NO","NO2","NOx","SO2"]]
    from airFunctions import get_PM10_subindex,get_PM25_subindex,get_SO2_subindex
    from airFunctions import get_NOx_subindex,get_NH3_subindex,get_CO_subindex,get_O3_subindex
    daily_pollutants["PM2.5_subIndex"]= daily_pollutants["PM2.5"].apply(lambda x: get_PM25_subindex(x))
    daily_pollutants["PM10_subIndex"]= daily_pollutants["PM10"].apply(lambda x: get_PM10_subindex(x))
    daily_pollutants["CO_subIndex"]= daily_pollutants["CO"].apply(lambda x: get_CO_subindex(x))
    daily_pollutants["NH3_subIndex"]= daily_pollutants["NH3"].apply(lambda x: get_NH3_subindex(x))
    daily_pollutants["SO2_subIndex"]= daily_pollutants["SO2"].apply(lambda x: get_SO2_subindex(x))
    daily_pollutants["NOx_subIndex"]= daily_pollutants["NOx"].apply(lambda x: get_NOx_subindex(x))
    daily_pollutants["AQI_calculated"] = round(daily_pollutants[["PM2.5_subIndex", "PM10_subIndex", "SO2_subIndex", "NOx_subIndex",
                                     "NH3_subIndex", "CO_subIndex"]].max(axis=1))
    dataset["AQI_calculated"]=daily_pollutants["AQI_calculated"]
    dataset.to_csv("{}_preprocessed.csv".format(filename),index=False)
    return dataset