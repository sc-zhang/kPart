#!/usr/bin/env python
import sys
import os
import time


def time_print(str):
	print("\033[32m%s\033[0m %s"%(time.strftime('[%H:%M:%S]',time.localtime(time.time())), str))


def pre_assign(in_bam_dir, ref_fa, kmer_size, wrk_dir, threads):
	script_dir = sys.path[0]
	if not os.path.exists(wrk_dir):
		os.mkdir(wrk_dir)
	kmer_dir = os.path.join(wrk_dir, "kmers")
	ref_kmer_dir = os.path.join(kmer_dir, "ref")
	time_print("Generating reference kmers")
	os.system("%s/get_seq_all_kmers.py %s %d %s %d"%(script_dir, ref_fa, kmer_size, ref_kmer_dir, threads))

	time_print("Grouping reads with bam")
	reads_dir = os.path.join(wrk_dir, 'grouped_reads')
	for bam in os.listdir(in_bam_dir):
		time_print("\tDealing %s"%bam)
		bam_name = bam.split('.')[0]
		fn = os.path.join(in_bam_dir, bam)
		out_dir = os.path.join(reads_dir, bam_name)
		os.system("%s/group_reads_with_bam.py %s %s %d"%(script_dir, fn, out_dir, threads))
	
	time_print("Generating reads kmers")
	qry_kmer_dirs = []
	for sample in os.listdir(reads_dir):
		time_print("\tDealing %s"%sample)
		fq_dir = os.path.join(reads_dir, sample)
		out_dir = os.path.join(kmer_dir, sample)
		qry_kmer_dirs.append(out_dir)
		os.system("%s/get_reads_all_kmers.py %s %d %s %d"%(script_dir, fq_dir, kmer_size, out_dir, threads))
	
	time_print("Statistic kmer dist")
	qry_kmer_dir = ','.join(qry_kmer_dirs)
	stat_file = os.path.join(wrk_dir, 'kmer_dist.csv')
	os.system("%s/stat_kmer_dist.py %s %s %s %d"%(script_dir, ref_kmer_dir, qry_kmer_dir, stat_file, threads))

	time_print("Classifying contigs")
	classify_file = os.path.join(wrk_dir, 'kmer_dist_classified.csv')
	os.system("%s/classify_result.py %s %s"%(stat_file, classify_file))

	time_print("Finished")


if __name__ == "__main__":
	if len(sys.argv) < 6:
		print("Usage: python %s <in_bam_folder> <reference_fasta> <kmer_size> <wrk_dir> <threads>"%sys.argv[0])
		print("Notice: bam_file must be sorted and indexed")
	else:
		in_bam_dir, ref_fa, kmer_size, wrk_dir, threads = sys.argv[1:]
		threads = int(threads)
		kmer_size = int(kmer_size)
		pre_assign(in_bam_dir, ref_fa, kmer_size, wrk_dir, threads)
