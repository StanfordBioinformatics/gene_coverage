import argparse
import progressbar

COVERAGE_DEPTH_THRESHOLDS=[5, 10, 15, 20]
CHROMOSOME_NAMES=['chr1','chr2','chr3','chr4','chr5','chr6','chr7','chr8','chr9','chr10','chr11','chr12','chr13','chr14','chr15','chr16','chr17','chr18','chr19','chr20','chr21','chr22','chrX','chrY']

def gene_coverage():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("exons_bedfile", help="bedfile mapping positions to gene names")
    parser.add_argument("genelist", help="list of genes to include in the output")
    parser.add_argument("coverage_file", help="per-position coverage file from GATK DepthOfCoverage")
    args = parser.parse_args()

    # Read genelist and create dict
    genes = {}
    with open(args.genelist) as g:
        for line in g:
            gene = line.strip()
            genes[gene] = {'total_bases':0,'exons':0}
            for threshold in COVERAGE_DEPTH_THRESHOLDS:
                genes[gene][threshold] = 0

    # Read exons bedfile and create dict
    exons = {}
    for chrom in CHROMOSOME_NAMES:
        exons[chrom] = []
    unmatched_genes = set(genes.keys())
    with open(args.exons_bedfile) as e:
        for line in e:
            chrom,start,end,gene = line.strip().split() 
            if chrom not in CHROMOSOME_NAMES:
                raise Exception("%s contains unrecognized chromosome: %s" % (args.exons_bedfile, chrom))
            if gene in genes:
                exons[chrom].append([start,end,gene])
                genes[gene]['exons'] += 1
                genes[gene]['chrom'] = chrom
                if gene in unmatched_genes:
                    unmatched_genes.remove(gene)
    if len(unmatched_genes) > 0:
        print 'Warning: genes in %s not found in %s and will not be included in output:' % (args.genelist, args.exons_bedfile)
        for unmatched_gene in unmatched_genes:
            print unmatched_gene
            del(genes[unmatched_gene])

    # Sort exons by start and end positions
    for chrom in exons:
        exons[chrom].sort()

    # Get number of lines in coverage file
    with open(args.coverage_file) as coverage_file:
        num_lines = 0
        for line in coverage_file:
            num_lines += 1

    # Keep pointers to current starting exons for each chromosome; these will only increase 
    # since both exons and DepthOfCoverage input are sorted by position
    starting_exons = {chrom : 0 for chrom in CHROMOSOME_NAMES}

    # Scan through coverage file 
    with open(args.coverage_file) as coverage_file:
        # Ignore header line
        header = coverage_file.readline()
        bar = progressbar.ProgressBar(max_value=num_lines)
        for line in bar(coverage_file):
            locus,total_depth,average_depth,sample_depth = line.strip().split()
            chrom,pos = locus.split(':')
            if chrom not in CHROMOSOME_NAMES:
                raise Exception("%s contains unrecognized chromosome: %s" % (args.coverage_file, chrom))
            else:
                # Get gene(s) for current position
                current_genes = set()

                # Advance to first exon that ends at or after pos
                exons_index = starting_exons[chrom]
                while exons_index < len(exons[chrom]) and exons[chrom][exons_index][1] < pos: 
                    exons_index += 1
                starting_exons[chrom] = exons_index
                
                # Check all exons that start at or before pos
                while exons_index < len(exons[chrom]) and exons[chrom][exons_index][0] <= pos:
                    if pos <= exons[chrom][exons_index][1]:
                        current_genes.add(exons[chrom][exons_index][2])
                    exons_index += 1

                # Add to coverage counts
                for current_gene in current_genes:
                    genes[current_gene]['total_bases'] += 1
                    for threshold in COVERAGE_DEPTH_THRESHOLDS:
                        if total_depth < threshold:
                            genes[current_gene][threshold] += 1
                        
    # Print header line
    header = ['gene','chr','exons','total_bases']
    header.extend(['bases<%dx' % threshold for threshold in COVERAGE_DEPTH_THRESHOLDS])
    header.extend(['%%bases<%dx' % threshold for threshold in COVERAGE_DEPTH_THRESHOLDS])
    print '\t'.join(header)

    # Print gene rows
    for gene in sorted(genes):
        row = [gene, genes[gene]['chrom'], genes[gene]['exons'], genes[gene]['total_bases']]
        row.extend([genes[gene][threshold] for threshold in COVERAGE_DEPTH_THRESHOLDS])
        row.extend([float(genes[gene][threshold])/float(genes[gene]['total_bases']) if genes[gene]['total_bases'] > 0 else 0.0 for threshold in COVERAGE_DEPTH_THRESHOLDS])
        row = map(str, row)
        print '\t'.join(row)

if __name__ == '__main__': gene_coverage()
