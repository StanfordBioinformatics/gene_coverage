# gene_coverage
Calculates gene-level breadth-of-coverage at several depth-of-coverage thresholds.

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
Locus	Total_Depth	Average_Depth_sample	Depth_for_case0078
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
