## README

### Introduction

This package is used for classifying contig into groups based on kmers from parents.

### Dependencies

Python modules:

- pysam

### Installation

``` shell
cd /path/to/install
git clone https://github.com/sc-zhang/Contig_trio_classifier.git
cd Contig_trio_classifier/bin
chmod +x *.py

# Optional
echo 'export PATH=/path/to/install/Contig_trio_classifier/bin:$PATH' >> ~/.bash_profile
source ~/.bash_profile
```

### Usage

#### 1. Simple usage with pipeline

```shell
contig_classifier.py <in_bam_folder> <reference_fasta> <kmer_size> <wrk_dir> <threads>
```

**<in_bam_folder>** is a folder only contain two sorted and indexed bam, with name like AA.sorted.bam, AA is the name of parents. bam file is generate by mapping parents' reads to reference_fasta.

**<reference_fasta>** is the contig file of child.

#### 2. Run some steps separately

If you have a cluster, you can run some steps separately to save time.

**Step 1. generate reference kmers**

```shell
get_seq_all_kmers.py <ref_fasta> <kmer_size> <out_ref_kmer_dir> <threads>
```

**Step 2. generate parents' kmers**

```shell
# Extract reads into different groups with contig
group_reads_with_bam.py <bam_file> <out_fastq_dir> <threads>
# <bam_file> must be sorted and indexed

# Generate kmers with reads
get_reads_all_kmers.py <fq_dir> <kmer_size> <out_qry_kmer_dir> <threads>
# <fq_dir> is same as <out_fastq_dir> above
```

**Notice:** You can run step 1 and step 2 separately, also you can run step 2 for parents separately.

**Step 3. classify contigs**

```shell
stat_kmer_dist.py <ref_kmer_dir> <father_kmer_dir,mother_kmer_dir> <stat_file> <threads>
# <father_kmer_dir,mother_kmer_dir> is the directorys of father's kmers and mother's kmers separated by comma

classify_result.py <stat_file> <classify_file>
```

#### 3. Result

You will get a csv file with 6 columns like:

ContigName|No. of Kmers|No. of Kmers shared by parents|No. of Kmers present only in father|No. of Kmers present only in mother|Classification
-|-|-|-|-|-
tig00000002|104260|81698|8366|252|Father
tig00000005|57940|37234|426|448|Undetermined

**Notice:** if kmers from contig only present in one sample is greater than that in the other sample more than 2 folds, we mark the contig with this sample, or we mark it "Undetermined".


