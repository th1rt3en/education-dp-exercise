import unittest
import pandas as pd

from app.utils import parse_data, enrich_data


class TestDataProcessing(unittest.TestCase):

    def setUp(self) -> None:
        self.df = pd.read_csv("data-2018.txt", sep="\t")

    def test_data_parse(self):
        parsed_df = parse_data(self.df)
        for col in parsed_df.columns:
            self.assertFalse(parsed_df[col].isnull().values.any())

    def test_data_enrich(self):
        parsed_df = parse_data(self.df)
        for _idx, row in parsed_df.sample(5).iterrows():
            enriched_row = enrich_data(row.to_dict())
            self.assertTrue("description" in enriched_row)
            self.assertTrue("url" in enriched_row)


if __name__ == '__main__':
    unittest.main()
