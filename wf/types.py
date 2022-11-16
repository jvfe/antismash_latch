from enum import Enum


class Taxon(Enum):
    bacteria = "bacteria"
    fungi = "fungi"


class GeneFindingTool(Enum):
    glimmerhmm = "glimmerhmm"
    prodigal = "prodigal"
    prodigal_m = "prodigal-m"
    none = "none"
