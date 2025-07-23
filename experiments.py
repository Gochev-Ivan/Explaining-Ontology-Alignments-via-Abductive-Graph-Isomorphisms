from owlready2 import *
from Utils import *
from isomorphisms import *


def experiments():
    from Ontologies import Ontology, OntologyClass
    from PythonOWL2expr import POWL2expr
    from owl2tree import expr2tree, signature
    import time

    O1_folder_path = input("Input the folder of the first ontology: ")
    O1_file_path = input("Input the name of the first ontology (.owl): ")
    O1 = Ontology(O1_folder_path, O1_file_path)

    O2_folder_path = input("Input the folder of the second ontology: ")
    O2_file_path = input("Input the name of the second ontology (.owl): ")
    O2 = Ontology(O2_folder_path, O2_file_path)

    sub_mappings_file = input("Input the file of the generated subsumption mappings (.csv): ")
    df_sub_mappings = pd.read_csv(sub_mappings_file)

    results_file = input("Input the file in which to save the results (.csv): ")

    results = pd.DataFrame(columns=["#E", "|E|", "#A", "#C", "t[s]"])
    for i in range(len(df_sub_mappings)):
        row = df_sub_mappings.iloc[i]
        print(f"{[*row]=}")
        C1 = OntologyClass(iri=row['O1'], cls=IRIS[row['O1']])
        C2 = OntologyClass(iri=row['O2'], cls=IRIS[row['O2']])

        num_E = 0
        card_E = []
        num_A = 0
        num_R = 0
        time_s = 0
        for definition_1 in set(C1.get_equivalentToClasses() + C1.get_supClasses()):
            for definition_2 in set(C2.get_equivalentToClasses() + C2.get_supClasses()):
                if definition_1 == Thing or definition_2 == Thing:
                    continue
                def_1 = POWL2expr(clean_expr(definition_1))
                def_2 = POWL2expr(clean_expr(definition_2))
                T1 = expr2tree(def_1, inputted_vertex_notation='v')
                T2 = expr2tree(def_2, inputted_vertex_notation='w')
                AP = Isomorphisms(T1=T1, T2=T2)
                start_time = time.time()
                _, _ = AP.heuristics_subtree_isomorphisms()
                time_s += time.time() - start_time
                for num, h in enumerate(AP.construct_hypotheses()):
                    for axiom in h:
                        lhs, rhs = axiom.split("SubClassOf")
                        classes_1, properties_1 = signature(lhs)
                        classes_2, properties_2 = signature(rhs)
                        num_A = len(classes_1) + len(classes_2)
                        num_R = len(properties_1) + len(properties_2)
                    card_E.append(len(h))
                    num_E += 1
        results.loc[len(results)] = [num_E, sum(card_E) / len(card_E), num_A, num_R, time_s]
    print_df(results)
    results.to_csv(results_file)
