import pandas as pd
# import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno


def optain_data(path):
    with open(path,'r', encoding="utf8") as f:
        data = json.loads(f.read())
    df = pd.json_normalize(data, record_path =['releases'])
    df["ruc_contratante"]=df["buyer.id"].str.extract("EC-RUC-(\d+)")
    def awar_id(x):
        try:
            return x[0]['suppliers'][0]['id']
        except:
            pass
    df["awar_id"]=df['awards'].apply(awar_id)
    extra_ruc = r"(?:ID-|EC-RUC-)(\d+)"
    df["ruc"]=df["awar_id"].str.extract(extra_ruc )
    def awar_name(x):
        try:
            return x[0]['suppliers'][0]['name']
        except:
            pass
    df["nombre"]=df['awards'].apply(awar_name)
    def awar_amount(x):
        try:
            return x[0]['value']['amount']
        except:
            pass
    df["monto"]=df['awards'].apply(awar_amount)
    df["tag"]=df["tag"].astype(str)
    df_notag=df[df["tag"].str.contains("award")]
    select_df=df_notag[["nombre","ruc","monto","ocid","buyer.name","buyer.id","ruc_contratante","date","tender.procurementMethodDetails",
                 'tender.description']]
    select_df_name=select_df.rename(columns={'buyer.name':'contratante', 'buyer.id':'id_conrtatante','date':'fecha','tender.description':'obj_contrato'})
    return select_df_name


path_2021="Data_Json/10-01-2023/releases_2021.json"
path_2022="Data_Json/10-01-2023/releases_2022.json"

data_21=optain_data(path_2021)

data_22=optain_data(path_2022)

df_years = pd.concat([data_21,data_22])

df_years_not_CE=df_years[~df_years["tender.procurementMethodDetails"].str.contains("Catálogo electrónico")]

df_years_not_CE=df_years_not_CE.drop(columns=["tender.procurementMethodDetails"])

df_years.to_csv("data/procesos_2021_2022/proveedores_21_22.csv", index=False)

df_years_not_CE.to_csv("data/procesos_2021_2022/proveedores_21_22_not_CE.csv", index=False)

len(df_years_not_CE["ruc"].unique())

hcm=df_years[df_years["ruc_contratante"]=="0160006390001"]

hcm

hcm.to_csv("proveedores_21_22_hmc.csv", index=False)

# +
# df_years[df_years["ruc_contratante"]=="1768153530001"]
# -

plt.figure(figsize=(6, 3))
sns.heatmap(df_years .isnull(), cbar=False)

# # Comparación procesos SOCP y procesos datos abiertos

data_21_22_scp= pd.read_csv("data/revision/review_proce.csv")

data_21_22_scp

data_21_22_da= pd.read_csv("data/procesos_2021_2022/proveedores_21_22_not_CE.csv")

data_21_22_scp

data_21_22_da['Codigo']=data_21_22_da['ocid'].str.extract('ocds-5wno2w-(.*\w*.)-|', expand=True)

data_21_22_da



def review(lista,df_list):
    in_base_directori=[]
    no_in_directori=[]
    # Filtramos las empresas que ya han sido analizadas 
    def find_df(x):
        if df_list.isin([x]).any():
            in_base_directori.append(x)
        else:
            no_in_directori.append(x)

    for i in lista:
        find_df(i)
    return in_base_directori,no_in_directori


proces_no_in_DA=review(data_21_22_scp["Código"].unique(),data_21_22_da["Codigo"])[1]

len(proces_no_in_DA)

data_21_22_scp["Estado del Proceso"].unique()

data_21_22_da[data_21_22_da["Codigo"].str.contains("SIEA-GADMCG")]

data_21_22_scp[data_21_22_scp["Código"].str.contains("MCS-BDESZCP-001")]

to_reviewe_in_socp=data_21_22_scp[data_21_22_scp['Código'].isin(proces_no_in_DA)]

to_reviewe_in_socp

a_df=to_reviewe_in_socp[to_reviewe_in_socp["Estado del Proceso"]=="Finalizada"]

a_df[a_df["Código"].str.contains("SIE")]

# +
# select_df_name[select_df_name["ruc"].isnull()]

# +
# select_df_name[select_df_name["nombre"].isnull()]["tag"].value_counts()

# +
# select_df_name[select_df_name["nombre"].isnull()]
