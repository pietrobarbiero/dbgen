from typing import Set

import pandas as pd
from mongoengine import Document, StringField, DateTimeField, FileField, ReferenceField, queryset_manager, QuerySet

from ..utils.config import _options


class Result(Document):
    """
    Result

    Attributes
    ----------
    :param tool: bioinformatic tool name
    :param version: bioinformatic tool version
    :param date: date when the result has been collected
    :param parameters: bioinformatic tool parameters
    :param raw_result: raw result provided by the bioinformatic tool
    :param sample: reference to the corresponding sample
    :param dataset: reference to the corresponding dataset
    :param species: reference to the corresponding species
    """
    tool = StringField(max_length=200, unique_with=["version", "parameters", "sample"])
    version = StringField(max_length=200, unique_with=["tool", "parameters", "sample"])
    date = DateTimeField()
    parameters = StringField(max_length=200, unique_with=["tool", "version", "sample"])
    raw_result = FileField()
    sample = ReferenceField('Sample', required=True, unique_with=["tool", "version", "parameters"])
    dataset = ReferenceField('Dataset', required=True)
    species = ReferenceField('Species', required=True)

    @queryset_manager
    def get_results(doc_cls, queryset: QuerySet, species_name=None, dataset_name=None, tool_name=None) -> pd.DataFrame:
        """
        Get samples' results

        :param species_name: name of the species
        :param dataset_name: name of the dataset
        :param phenotype_name: name of the phenotype
        """
        data = _options(queryset, species_name, dataset_name, tool_name)
        df = pd.DataFrame()
        for d in data:
            ds = _to_df(d)
            df = df.append(ds)
        return df

    @queryset_manager
    def get_tool_names(doc_cls, queryset: QuerySet, species_name=None, dataset_name=None) -> Set:
        """
        Get all tool names available

        :param species_name: name of the species
        :param dataset_name: name of the dataset
        """
        data = _options(queryset, species_name, dataset_name)
        names = set()
        for d in data:
            names.add(d.name)
        return names


def _to_df(res: Result):
    d = {res.sample.pk: (res.species.name, res.dataset.name,
                         res.tool, res.version, res.parameters, res.raw_result)}
    df = pd.DataFrame.from_dict(d, orient="index",
                                columns=["species", "dataset", "tool", "version", "parameters", "raw result"])
    return df
