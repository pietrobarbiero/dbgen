import os

import dbgen


def main():

    try:
        os.chdir("./examples")
    except:
        pass

    configs = dbgen.load_cfg()
    dbgen.start_db(configs)
    dbgen.drop_db()
    dbgen.print_db()

    dbgen.connect_db()
    dbgen.import_data(configs)
    dbgen.print_db()

    s1 = dbgen.Sample.get_fastq_dirs(species_name="Staphylococcus Aureus")
    s2 = dbgen.Sample.get_fastq_dirs(dataset_name="S_aureus_2014_Everitt")
    p0 = dbgen.Phenotype.get_phenotype_names(species_name="Staphylococcus Aureus")
    p1 = dbgen.Phenotype.get_phenotypes(species_name="Staphylococcus Aureus", phenotype_name="Mupirocin")
    p2 = dbgen.Phenotype.get_phenotypes(dataset_name="S_aureus_2014_Everitt", phenotype_name="Mupirocin")
    p3 = dbgen.Phenotype.get_phenotypes(species_name="Staphylococcus Aureus", dataset_name="S_aureus_2014_Everitt", phenotype_name="Mupirocin")

    dbgen.shutdown_db(configs)

    return


if __name__ == "__main__":
    main()
