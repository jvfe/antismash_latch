from latch.types.metadata import (
    LatchAuthor,
    LatchMetadata,
    LatchParameter,
    LatchRule,
    Params,
    Section,
    Text,
)

PARAMS = {
    "sample_name": LatchParameter(display_name="Sample name", batch_table_column=True),
    "antismash_input": LatchParameter(
        display_name="AntiSMASH input",
        detail="(.gb, .gbk)",
        rules=[
            LatchRule(
                regex="(.gb|.gbk)$",
                message="Must be a valid GenBank file",
            )
        ],
        batch_table_column=True,
    ),
}

FLOW = [
    Section(
        "Samples",
        Text(
            "Sample provided has to include an identifier for the sample (Sample name)"
            " and one or two files corresponding to the contiguous sequences"
            " these are GenBank (gbk) files."
        ),
        Params("sample_name", "antismash_input"),
    )
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
