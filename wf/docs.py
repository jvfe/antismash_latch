from latch.types.metadata import (
    LatchAuthor,
    LatchMetadata,
    LatchParameter,
    LatchRule,
    Params,
    Section,
    Spoiler,
    Text,
)

PARAMS = {
    "sample_name": LatchParameter(display_name="Sample name", batch_table_column=True),
    "antismash_input": LatchParameter(
        display_name="Genome",
        detail="(.fa, .fasta, .fna, .gb, .gbk)",
        rules=[
            LatchRule(
                regex="(.gb|.gbk|.fa|.fna|.fasta)$",
                message="Must be a valid FASTA or GenBank file",
            )
        ],
        batch_table_column=True,
    ),
    "taxon": LatchParameter(
        display_name="Taxonomic classification of input sequence",
        batch_table_column=True,
    ),
    "genefinding_tool": LatchParameter(
        display_name="Gene finding options (ignored when ORFs are annotated)"
    ),
}

FLOW = [
    Section(
        "Samples",
        Text(
            "Sample provided has to include an identifier for the sample (Sample name)"
            " and one or two files corresponding to the contiguous sequences"
            " these are GenBank (gbk) files."
            " Additionally, choose if the sample belongs to bacterial or fungal taxa."
        ),
        Params("sample_name", "antismash_input", "taxon"),
    ),
    Spoiler(
        "Gene Finding Tool",
        Text(
            "Specify algorithm used for gene finding: GlimmerHMM, Prodigal"
            " Prodigal Metagenomic/Anonymous mode, or none."
            " The 'none' option will not run genefinding."
            " **This is required when dealing with FASTA data.**"
        ),
        Params("genefinding_tool"),
    ),
]

antismash_docs = LatchMetadata(
    display_name="antiSMASH",
    documentation="https://github.com/jvfe/antismash_latch/blob/main/README.md",
    author=LatchAuthor(
        name="jvfe",
        github="https://github.com/jvfe",
    ),
    repository="https://github.com/jvfe/antismash_latch",
    license="MIT",
    parameters=PARAMS,
    tags=["metagenomics", "BGC", "MAGs"],
    flow=FLOW,
)
