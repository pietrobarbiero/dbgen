import time
import unittest


class Test(unittest.TestCase):
    def test_dbgen(self):
        import os
        import dbgen

        configs = dbgen.load_cfg()
        dbgen.start_db(configs)
        # dbgen.drop_db()
        # dbgen.print_db()

        dbgen.connect_db()
        # dbgen.import_data(configs)
        # dbgen.print_db()

        s1 = dbgen.Sample.get_raw_data(species_name="Species 1", dataset_name="Species_Name_2009_AuthorName")
        s2 = dbgen.Sample.get_raw_data(dataset_name="Species_Name_2009_AuthorName")
        s3 = dbgen.Sample.get_raw_data(species_name="Species 1")
        u1 = dbgen.Sample.get_download_urls(dataset_name="Species_Name_2009_AuthorName")
        u2 = dbgen.Sample.get_download_urls(species_name="Species 1")
        u3 = dbgen.Sample.get_download_urls(species_name="Species 1", dataset_name="Species_Name_2009_AuthorName")
        p0 = dbgen.Phenotype.get_phenotype_names(species_name="Species 1")
        p1 = dbgen.Phenotype.get_phenotypes(species_name="Species 1", phenotype_name="Mupirocin")
        p2 = dbgen.Phenotype.get_phenotypes(dataset_name="Species_Name_2009_AuthorName", phenotype_name="Mupirocin")
        p3 = dbgen.Phenotype.get_phenotypes(species_name="Species 1",
                                            dataset_name="Species_Name_2009_AuthorName",
                                            phenotype_name="Mupirocin")

        root_path = "./test/data/db/cooked/"
        if not os.path.exists(root_path):
            os.makedirs(root_path)
        for k, v in s1.iterrows():
            tool_name = "AMRFinder+"
            version = "0.0.1"
            date = "2019-09-02"
            parameters = "-c 20 -v 39"
            file_path = os.path.join(root_path, "testfile_%s.txt" % v["run_accession"])
            raw_result = open(file_path, "w")
            raw_result.write("Hello %s" % v["run_accession"])
            raw_result.write("This is our new text file")
            raw_result.write("and this is another line.")
            raw_result.write("Why? Because we can.")
            raw_result.close()
            raw_result_path = os.path.join(os.getcwd(), file_path)

            dbgen.Sample.save_result(k, tool_name, version,
                                     date, parameters, raw_result_path)

        res0 = dbgen.Sample.get_results(species_name="Species 1", dataset_name="Species_Name_2009_AuthorName")
        res1 = dbgen.Sample.get_results(species_name="Species 1")
        res2 = dbgen.Sample.get_results(dataset_name="Species_Name_2009_AuthorName")

        self.assertTrue(len(p0) == 23)
        self.assertTrue(p1.shape == (282, 3))
        self.assertTrue(p2.shape == (92, 3))
        self.assertTrue(p3.shape == (92, 3))
        self.assertTrue(s1.shape == (92, 4))
        self.assertTrue(s2.shape == (92, 4))
        self.assertTrue(s3.shape == (282, 4))
        self.assertTrue(u1.shape == (92, 4))
        self.assertTrue(u2.shape == (282, 4))
        self.assertTrue(u3.shape == (92, 4))
        self.assertTrue(res0.shape == (92, 8))
        self.assertTrue(res1.shape == (92, 8))
        self.assertTrue(res2.shape == (92, 8))

        dbgen.shutdown_db(configs)

        return

    def test_start_mongo(self):
        import dbgen
        import sys

        sys.argv.extend(["-p", "test"])
        configs = dbgen.load_cfg()
        dbgen.start_db(configs)
        dbgen.shutdown_db(configs)

        return


if __name__ == '__main__':
    unittest.main()
