def generate_explanations():
    from owlready2 import IRIS, Thing, rdfs
    from Utils import clean_expr, print_isomorphisms_str
    from isomorphisms import Isomorphisms
    import pandas as pd
    from Ontologies import Ontology, OntologyClass
    from PythonOWL2expr import POWL2expr
    from owl2tree import expr2tree, signature
    from tabulate import tabulate

    prefixes = []

    # Load the first ontology:
    # O1_folder_path = input("Input the folder of the first ontology: ")
    # O1_file_path = input("Input the name of the first ontology (.owl): ")
    O1_folder_path = r"C:\Users\goche\Desktop\IJCKG2025\Experiments\snomed-ncit.pharm\\"
    O1_file_path = "snomed.pharm.owl"
    O1 = Ontology(O1_folder_path, O1_file_path)

    print(f"O1 = {O1}")

    # Load the second ontology:
    # O2_folder_path = input("Input the folder of the second ontology: ")
    # O2_file_path = input("Input the name of the second ontology (.owl): ")
    O2_folder_path = r"C:\Users\goche\Desktop\IJCKG2025\Experiments\snomed-ncit.pharm\\"
    O2_file_path = "ncit.pharm.owl"
    O2 = Ontology(O2_folder_path, O2_file_path)

    print(f"O2 = {O2}")

    # sub_mappings_file = input("Input the file of the generated subsumption mappings (.csv): ")
    sub_mappings_file = r"C:\Users\goche\Desktop\IJCKG2025\GitHub Repo for IJCKG2025 paper\Obtained Subsumption Mappings\snomed_ncit_subs_mappings.csv"
    df_sub_mappings = pd.read_csv(sub_mappings_file)

    # explanations_results_folder = input("Input the folder in which you want to save all explanations/correspondence: ")
    explanations_results_folder = r"C:\Users\goche\Desktop\IJCKG2025\GitHub Repo for IJCKG2025 paper\Explanations_snomed-ncit_test1\\"

    prefixes.extend([O1_folder_path, O2_folder_path])

    # for i in range(len(df_sub_mappings[:20])):

    labeled_expressions = {"O1": {}, "O2": {}}

    for i in range(len(df_sub_mappings)):
        row = df_sub_mappings.iloc[i]
        C1 = OntologyClass(iri=row['O1'], cls=IRIS[row['O1']])
        C2 = OntologyClass(iri=row['O2'], cls=IRIS[row['O2']])

        print(f"c = ({C1}, {C2}, SubClassOf)")
        print()
        print(f"C1 = {C1} <{C1.get_annotations()}>")
        print(f"C2 = {C2} <{C2.get_annotations()}>")
        print()

        D1 = C1.hierarchy()
        D2 = C2.hierarchy()

        # TODO: FINALIZE THE GENERATION OF EXPLANATIONS:
        for d1 in D1:

            M1 = []
            for expr in d1:
                if str(expr) != "owl.Thing":
                    if expr not in labeled_expressions["O1"]:
                        labeled_expressions["O1"][expr] = O1.get_expr_labels(POWL2expr(clean_expr(expr, prefixes)))
                    M1.append(labeled_expressions["O1"][expr])
            # M1 = [O1.get_expr_labels(POWL2expr(clean_expr(expr, prefixes))) for expr in d1
            #       if str(expr) != "owl.Thing"]

            print(" -- is_a --> ".join(M1))

            for d2 in D2:
                # print(f"{d1=}")
                # print(f"{d2=}")
                # for expr in d1:
                #     print(f"{type(expr)=}")
                #     if str(expr) != "owl.Thing":
                #         print(f"{expr=}")
                #         print(f"{clean_expr(expr, prefixes)=}")
                #         print(f"{POWL2expr(clean_expr(expr, prefixes))=}")
                #         print(f"{O1.get_expr_labels(POWL2expr(clean_expr(expr, prefixes)))=}")
                #         print()
                M2 = []
                for expr in d2:
                    if str(expr) != "owl.Thing":
                        if expr not in labeled_expressions["O2"]:
                            labeled_expressions["O2"][expr] = O2.get_expr_labels(POWL2expr(clean_expr(expr, prefixes)))
                        M2.append(labeled_expressions["O2"][expr])

                # M2 = [O2.get_expr_labels(POWL2expr(clean_expr(expr, prefixes))) for expr in d2
                #       if str(expr) != "owl.Thing"]
                print("\t" + " -- is_a --> ".join(M2))
            print()

        # print("D1 = ")
        # for d1 in D1:
        #     print(f"\t{clean_expr(d1, prefixes)}")
        # print("D2 = ")
        # for d2 in D2:
        #     print(f"\t{clean_expr(d2, prefixes)}")
        print("|" + ("=" * 300) + "|")
        print("_" + ("_" * 300) + "_")
    """
    for i in range(len(df_sub_mappings[:10])):
    # for i in range(len(df_sub_mappings)):
        txt_file_output = ""

        row = df_sub_mappings.iloc[i]
        C1 = OntologyClass(iri=row['O1'], cls=IRIS[row['O1']])
        C2 = OntologyClass(iri=row['O2'], cls=IRIS[row['O2']])

        all_hypotheses = ""

        all_explanations = ""

        num_all_hypotheses = 0
        for definition_1 in set(C1.get_equivalentToClasses() + C1.get_supClasses(direct=False)):
            txt_file_output += f"O1 := {O1}\n"
            txt_file_output += f"O2 := {O2}\n\n"
            txt_file_output += f"C1 = {C1}, rdfs.label: {C1.get_annotations()}\n"
            txt_file_output += f"C2 = {C2}, rdfs.label: {C2.get_annotations()}\n\n"
            txt_file_output += f"Relation: {C1} SubClassOf {C2} ({C1.get_annotations()} SubClassOf {C2.get_annotations()})\n\n"
            for definition_2 in set(C2.get_equivalentToClasses() + C2.get_supClasses()):
                if definition_1 == Thing or definition_2 == Thing:
                    continue
                def_1 = POWL2expr(clean_expr(definition_1, prefixes))
                def_2 = POWL2expr(clean_expr(definition_2, prefixes))

                txt_file_output += "\n" + (10 * "|") + f" Definition of concept {C1} {C1.get_annotations()}\n" \
                                   + f"{C1} := {def_1}\n"

                T1 = expr2tree(def_1, inputted_vertex_notation='v')

                txt_file_output += "\n" + (10 * "|") + f" Tree of concept {C1} {C1.get_annotations()}\n" \
                                   + f"T1 = T_{C1} := \n"
                txt_file_output += T1.display_str() + "\n"
                txt_file_output += "\n" + (10 * "|") + f" Definition of concept {C2} {C2.get_annotations()}\n" \
                                   + f"{C2} := {def_2}\n"

                T2 = expr2tree(def_2, inputted_vertex_notation='w')

                txt_file_output += "\n" + (10 * "|") + f" Tree of concept {C2} {C2.get_annotations()}\n" \
                                   + f"T2 = T_{C2} := \n"
                txt_file_output += T2.display_str() + "\n"

                AP = Isomorphisms(T1=T1, T2=T2)
                isomorphisms, isomorphisms_df = AP.heuristics_subtree_isomorphisms()

                txt_file_output += "\n" + (10 * "|") + " Evaluation of the Heuristics \n" \
                                   + tabulate(isomorphisms_df, headers='keys', tablefmt='psql') + "\n"
                txt_file_output += "\n" + (10 * "|") + " Isomorphisms \n" + print_isomorphisms_str(isomorphisms)
                txt_file_output += "\n" + (10 * "|") + " Hypotheses \n" \
                                   + f"Relation to explain: {C1} SubClassOf {C2} " \
                                   + f"({C1.get_annotations()} SubClassOf {C2.get_annotations()})\n" \
                                   + "Hypotheses : "

                for num, h in enumerate(AP.construct_hypotheses()):
                    all_hypotheses += f"H{num_all_hypotheses}= " + "{ "

                    txt_file_output += f"H{num}= " + "{"

                    len_print = 1
                    for axiom in h:
                        print(f"{axiom=}")
                        axiom_to_display = axiom
                        lhs, rhs = axiom.split("SubClassOf")
                        classes_1, properties_1 = signature(lhs)
                        classes_2, properties_2 = signature(rhs)
                        for el in classes_1.union(properties_1):
                            if el == 'T':
                                continue
                            axiom_to_display = axiom_to_display\
                                .replace(el, rdfs.label[O1.ontology.search(iri=f"*{el}")[0]][0])
                        for el in classes_2.union(properties_2):
                            if el == 'T':
                                continue
                            axiom_to_display = axiom_to_display\
                                .replace(el, rdfs.label[O2.ontology.search(iri=f"*{el}")[0]][0])

                        if len(axiom + " " + axiom_to_display) > len_print:
                            len_print = len(axiom + " " + axiom_to_display)

                        all_hypotheses += f"{axiom} ({axiom_to_display})\n"

                        txt_file_output += f"{axiom} ({axiom_to_display})\n"

                    all_hypotheses += " " * \
                                      (len(f"H{num_all_hypotheses}= ") + len_print + len("    ")) \
                                      + " }\n\n"

                    num_all_hypotheses += 1

                    txt_file_output += " " * (len(f"H{num}= ") + len_print + len("    ")) + " }\n\n"

                txt_file_output += "+" * 170

        txt_file_output += "\n" + (10 * "|") \
                           + f" All Hypotheses (Explanations) for {C1} SubClassOf {C2} " \
                           + f"({C1.get_annotations()} SubClassOf {C2.get_annotations()})\n"
        txt_file_output += all_hypotheses + "\n"
        txt_file_output += "=" * 200 + "\n"
        txt_file_output += all_explanations
        txt_file_output += "=" * 200 + "\n"
        with open(explanations_results_folder + f"{C1}-{C2}.txt", "w") as output_file:
            output_file.write(txt_file_output)
        output_file.close()
    """
