import time
import unittest


class Test(unittest.TestCase):
    def test_dbgen(self):
        import os
        import dbgen

        configs = dbgen.load_cfg()
        dbgen.start_db(configs)
        dbgen.drop_db(configs)
        dbgen.print_db()

        dbgen.connect_db(configs)
        dbgen.import_data(configs)
        dbgen.print_db()

        s1 = dbgen.Sample.get_raw_data(species_name="species2", dataset_name="2009_AuthorName3")
        s2 = dbgen.Sample.get_raw_data(dataset_name="2009_AuthorName3")
        s3 = dbgen.Sample.get_raw_data(species_name="species2")
        u1 = dbgen.Sample.get_download_urls(dataset_name="2009_AuthorName3")
        u2 = dbgen.Sample.get_download_urls(species_name="species2")
        u3 = dbgen.Sample.get_download_urls(species_name="species2", dataset_name="2009_AuthorName3")
        p0 = dbgen.Phenotype.get_phenotype_names(species_name="species2")
        p1 = dbgen.Phenotype.get_phenotypes(species_name="species2", phenotype_name="Mupirocin")
        p2 = dbgen.Phenotype.get_phenotypes(dataset_name="2009_AuthorName3", phenotype_name="Mupirocin")
        p3 = dbgen.Phenotype.get_phenotypes(species_name="species2",
                                            dataset_name="2009_AuthorName3",
                                            phenotype_name="Mupirocin")

        # dbgen.Sample.download_raw_data(species_name="species2", dataset_name="2009_AuthorName3")
        #
        # s1 = dbgen.Sample.get_raw_data(species_name="species2", dataset_name="2009_AuthorName3")
        # s2 = dbgen.Sample.get_raw_data(dataset_name="2009_AuthorName3")
        # s3 = dbgen.Sample.get_raw_data(species_name="species2")
        # raw_data_files1 = [f.name for f in s1.iloc[0, -1]]
        # raw_data_files2 = [f.name for f in s1.iloc[1, -1]]
        # self.assertTrue(raw_data_files1 == ['ERR410034_1.fastq.gz', 'ERR410034_2.fastq.gz'])
        # self.assertTrue(raw_data_files2 == ['ERR410035_1.fastq.gz', 'ERR410035_2.fastq.gz'])

        root_path = "./test/db/cooked/"
        if not os.path.exists(root_path):
            os.makedirs(root_path)
        for k, v in s1.iterrows():
            tool_name = "AMRFinder+"
            version = "0.0.1"
            date = "2019-09-02"
            parameters = "-c 20 -v 39"
            file_path = os.path.join(root_path, "testfile_%s.txt" % v["run accession"])
            raw_result = open(file_path, "w")
            raw_result.write("Hello %s" % v["run accession"])
            raw_result.write("This is our new text file")
            raw_result.write("and this is another line.")
            raw_result.write("Why? Because we can.")
            raw_result.close()
            raw_result_path = os.path.abspath(file_path)

            dbgen.Sample.save_result(k, tool_name, version,
                                     date, parameters, raw_result_path)

        res0 = dbgen.Result.get_results(species_name="species2", dataset_name="2009_AuthorName3")
        res1 = dbgen.Result.get_results(species_name="species2")
        res2 = dbgen.Result.get_results(dataset_name="2009_AuthorName3")

        self.assertTrue(len(p0) == 18)
        self.assertTrue(p1.shape == (191, 3))
        self.assertTrue(p2.shape == (92, 3))
        self.assertTrue(p3.shape == (92, 3))
        self.assertTrue(s1.shape == (92, 5))
        self.assertTrue(s2.shape == (92, 5))
        self.assertTrue(s3.shape == (191, 5))
        self.assertTrue(u1.shape == (92, 5))
        self.assertTrue(u2.shape == (191, 5))
        self.assertTrue(u3.shape == (92, 5))
        self.assertTrue(res0.shape == (92, 6))
        self.assertTrue(res1.shape == (92, 6))
        self.assertTrue(res2.shape == (92, 6))

        dbgen.shutdown_db(configs)

        return


if __name__ == '__main__':
    unittest.main()
