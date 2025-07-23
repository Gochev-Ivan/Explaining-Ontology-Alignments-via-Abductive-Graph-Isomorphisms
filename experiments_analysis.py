from owlready2 import *

from Ontologies import Ontology, OntologyClass
from PythonOWL2expr import POWL2expr
from Utils import *
from isomorphisms import *
from owl2tree import expr2tree, signature
from tabulate import tabulate


df_results = pd.DataFrame(columns=["Alignment",
                                   "mean(#E) | median(#E) | max(#E)",
                                   "mean(|E|) | median(|E|) | max(|E|)",
                                   "mean(#A) | median(#A) | max(#A)",
                                   "mean(#C) | median(#C) | max(#C)",
                                   "mean(t[s]) | median(t[s]) | max(t[s])"])

df_snomed_ncit = pd.read_csv(r"C:\Users\goche\Desktop\IJCKG2025\GitHub Repo for IJCKG2025 paper\Explanations_snomed-ncit_test1\results_1.csv")
# df_snomed_fma = pd.read_csv(r"snomed-fma_results.csv")


df_results.loc[len(df_results)] = \
    ["snomed-ncit",
     f"{round(df_snomed_ncit['#E'].mean(), 2)} | {round(df_snomed_ncit['#E'].median(), 2)} | {round(df_snomed_ncit['#E'].max(), 2)}",
     f"{round(df_snomed_ncit['|E|'].mean(), 2)} | {round(df_snomed_ncit['|E|'].median(), 2)} | {round(df_snomed_ncit['|E|'].max(), 2)}",
     f"{round(df_snomed_ncit['#A'].mean(), 2)} | {round(df_snomed_ncit['#A'].median(), 2)} | {round(df_snomed_ncit['#A'].max(), 2)}",
     f"{round(df_snomed_ncit['#C'].mean(), 2)} | {round(df_snomed_ncit['#C'].median(), 2)} | {round(df_snomed_ncit['#C'].max(), 2)}",
     f"{round(df_snomed_ncit['t[s]'].mean(), 2)} | {round(df_snomed_ncit['t[s]'].median(), 2)} | {round(df_snomed_ncit['t[s]'].max(), 2)}"]

# df_results.loc[len(df_results)] = \
#     ["snomed-fma",
#      f"{round(df_snomed_fma['#E'].mean(), 2)} | {round(df_snomed_fma['#E'].median(), 2)} | {round(df_snomed_fma['#E'].max(), 2)}",
#      f"{round(df_snomed_fma['|E|'].mean(), 2)} | {round(df_snomed_fma['|E|'].median(), 2)} | {round(df_snomed_fma['|E|'].max(), 2)}",
#      f"{round(df_snomed_fma['#A'].mean(), 2)} | {round(df_snomed_fma['#A'].median(), 2)} | {round(df_snomed_fma['#A'].max(), 2)}",
#      f"{round(df_snomed_fma['#C'].mean(), 2)} | {round(df_snomed_fma['#C'].median(), 2)} | {round(df_snomed_fma['#C'].max(), 2)}",
#      f"{round(df_snomed_fma['t[s]'].mean(), 2)} | {round(df_snomed_fma['t[s]'].median(), 2)} | {round(df_snomed_fma['t[s]'].max(), 2)}"]

print_df(df_results)
