import re
import subprocess
from pathlib import Path

from latch import medium_task, message, workflow
from latch.resources.launch_plan import LaunchPlan
from latch.types import LatchDir, LatchFile

from .docs import antismash_docs
from .types import GeneFindingTool, Taxon
from .utils import _capture_output


@medium_task
def run_antismash(
    sample_name: str,
    antismash_input: LatchFile,
    taxon: Taxon,
    genefinding_tool: GeneFindingTool,
) -> LatchDir:

    _down_cmd = [
        "download-antismash-databases",
    ]

    message("info", {"title": "Downloading antiSMASH databases"})

    subprocess.run(_down_cmd, check=True)

    output_name = f"{sample_name}_results"
    output_dir = Path(output_name).resolve()

    _run_cmd = [
        "antismash",
        "--cb-general",
        "--cb-knownclusters",
        "--cb-subclusters",
        "--asf",
        "--pfam2go",
        "--smcog-trees",
        antismash_input.local_path,
        "--output-dir",
        str(output_dir),
        "--cpus",
        "32",
        "--genefinding-tool",
        genefinding_tool.value,
        "--taxon",
        taxon.value,
    ]

    running_cmd = " ".join(_run_cmd)

    message(
        "info",
        {
            "title": f"Running antiSMASH for input {sample_name}",
            "body": f"Command: {running_cmd}",
        },
    )

    return_code, stdout = _capture_output(_run_cmd)

    if return_code != 0:
        errors = re.findall("ERROR.*", stdout[1])

        for error in errors:
            message(
                "error",
                {
                    "title": f"An error was raised while running antiSMASH for {sample_name}",
                    "body": error,
                },
            )

        raise Exception("Failed while running antiSMASH")

    return LatchDir(str(output_dir), f"latch:///antismash_results/{output_name}")


@workflow(antismash_docs)
def antismash(
    sample_name: str,
    antismash_input: LatchFile,
    taxon: Taxon = Taxon.bacteria,
    genefinding_tool: GeneFindingTool = GeneFindingTool.prodigal,
) -> LatchDir:
    """The antibiotics and Secondary Metabolite Analysis SHell

    antiSMASH
    ----

    antiSMASH allows the rapid genome-wide identification,
    annotation and analysis of secondary metabolite biosynthesis
    gene clusters in bacterial and fungal genomes.

    It integrates and cross-links with a large number of in silico
    secondary metabolite analysis tools that have been published earlier [^1].

    [^1]: Kai Blin, Simon Shaw, Alexander M Kloosterman, Zach Charlop-Powers,
    Gilles P van Wezel, Marnix H Medema, Tilmann Weber, antiSMASH 6.0: improving
    cluster detection and comparison capabilities, Nucleic Acids Research,
    Volume 49, Issue W1, 2 July 2021, Pages W29–W35,
    https://doi.org/10.1093/nar/gkab335
    """

    return run_antismash(
        sample_name=sample_name,
        antismash_input=antismash_input,
        taxon=taxon,
        genefinding_tool=genefinding_tool,
    )


LaunchPlan(
    antismash,
    "Streptomyces coelicolor genome (FASTA format)",
    {
        "sample_name": "s_coelicolor",
        "antismash_input": LatchFile(
            "s3://latch-public/test-data/4318/s_coelicolor.fasta"
        ),
        "taxon": Taxon.bacteria,
        "genefinding_tool": GeneFindingTool.prodigal,
    },
)

LaunchPlan(
    antismash,
    "Streptomyces coelicolor genome (GBK format)",
    {
        "sample_name": "s_coelicolor",
        "antismash_input": LatchFile(
            "s3://latch-public/test-data/4318/s_coelicolor.gbk"
        ),
        "taxon": Taxon.bacteria,
        "genefinding_tool": GeneFindingTool.none,
    },
)
