# gene_coverage
Calculates gene-level breadth-of-coverage at several depth-of-coverage thresholds.

## Installation

Only one external package is needed:
```
pip install progressbar2
```

## Usage
```
usage: gene_coverage.py [-h] exons_bedfile genelist coverage_file

positional arguments:
  exons_bedfile  bedfile mapping positions to gene names
  genelist       list of genes to include in the output
  coverage_file  per-position coverage file from GATK DepthOfCoverage
```
Expected format for exons_bedfile:
```
chr1	11873	12227	DDX11L1
chr1	12612	12721	DDX11L1
chr1	13220	14409	DDX11L1
chr1	14361	14829	WASH7P
chr1	14969	15038	WASH7P
chr1	15795	15947	WASH7P
chr1	16606	16765	WASH7P
chr1	16857	17055	WASH7P
chr1	17232	17368	WASH7P
chr1	17368	17436	MIR6859-1
```
Expected format for genelist:
```
A2M
A4GALT
AAAS
AANAT
AARS
AARS2
AASS
ABAT
ABCA1
ABCA12
```
Expected format for coverage_file:
```
Locus	Total_Depth	Average_Depth_sample	Depth_for_NA12878
chr1:11874	91	91.00	91
chr1:11875	93	93.00	93
chr1:11876	91	91.00	91
chr1:11877	91	91.00	91
chr1:11878	89	89.00	89
chr1:11879	93	93.00	93
chr1:11880	96	96.00	96
chr1:11881	95	95.00	95
chr1:11882	97	97.00	97
```
## Output
Output goes to stdout. You can save it to a file using a redirect:
```
gene_coverage.py exons_bedfile genelist coverage_file > outputfile
```
Example output:
```
gene    chr exons   total_bases bases<5x    bases<10x   bases<15x   bases<20x   %bases<5x   %bases<10x  %bases<15x  %bases<20x
A2ML1   chr12   61  5   0   0   0   0   0.00    0.00    0.00    0.00
A4GALT  chr22   3   2092    0   0   19  87  0.00    0.00    0.91    4.16
AAED1   chr9    6   1225    0   0   0   0   0.00    0.00    0.00    0.00
AAGAB   chr15   30  3406    0   0   0   4   0.00    0.00    0.00    0.12
ABHD17C chr15   3   2360    0   0   0   3   0.00    0.00    0.00    0.13
ABHD2   chr15   26  9133    1   1   1   6   0.01    0.01    0.01    0.07
ABHD3   chr18   9   3   0   0   0   0   0.00    0.00    0.00    0.00
ABHD4   chr14   7   2509    0   0   0   0   0.00    0.00    0.00    0.00
ABHD5   chr3    7   0   0   0   0   0   0.00    0.00    0.00    0.00
ABHD6   chr3    9   0   0   0   0   0   0.00    0.00    0.00    0.00
```
