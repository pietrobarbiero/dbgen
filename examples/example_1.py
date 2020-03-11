import os

import dbgen


def main():

    try:
        os.chdir("./examples")
    except:
        pass

    configs = dbgen.load_cfg()
    dbgen.start_db(configs)
    # dbgen.drop_db()
    # dbgen.print_db()

    dbgen.connect_db()
    # dbgen.import_data(configs)
    # dbgen.print_db()

    s1 = dbgen.Sample.get_raw_data(species_name="Staphylococcus Aureus", dataset_name="S_aureus_2014_Everitt")
    s2 = dbgen.Sample.get_raw_data(dataset_name="S_aureus_2014_Everitt")
    u2 = dbgen.Sample.get_download_urls(dataset_name="S_aureus_2014_Everitt")
    p0 = dbgen.Phenotype.get_phenotype_names(species_name="Staphylococcus Aureus")
    p1 = dbgen.Phenotype.get_phenotypes(species_name="Staphylococcus Aureus", phenotype_name="Mupirocin")
    p2 = dbgen.Phenotype.get_phenotypes(dataset_name="S_aureus_2014_Everitt", phenotype_name="Mupirocin")
    p3 = dbgen.Phenotype.get_phenotypes(species_name="Staphylococcus Aureus", dataset_name="S_aureus_2014_Everitt", phenotype_name="Mupirocin")

    root_path = "./bacteria/db/cooked/"
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    for k, v in s1.iterrows():
        tool_name = "AMRFinder+"
        version = "0.0.1"
        date = "2019-09-02"
        parameters = "-c 20 -v 39"
        file_path = os.path.join(root_path, "testfile.txt")
        raw_result = open(file_path, "w")
        raw_result.write("Hello %s" % v["run_accession"])
        raw_result.write("This is our new text file")
        raw_result.write("and this is another line.")
        raw_result.write("Why? Because we can.")
        raw_result.close()
        raw_result_path = os.path.join(os.getcwd(), file_path)

        dbgen.Sample.save_result(k, tool_name, version,
                                 date, parameters, raw_result_path)

    res0 = dbgen.Sample.get_results(species_name="Staphylococcus Aureus", dataset_name="S_aureus_2014_Everitt")
    res1 = dbgen.Sample.get_results(species_name="Staphylococcus Aureus")

    dbgen.shutdown_db(configs)

    return


if __name__ == "__main__":
    main()
