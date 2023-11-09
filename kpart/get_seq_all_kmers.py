#!/usr/bin/env python
import sys
import os
import multiprocessing
import time


def time_print(str):
	print("\033[32m%s\033[0m %s"%(time.strftime('[%H:%M:%S]',time.localtime(time.time())), str))


def reverse_kmer(kmer):
	rev_kmer = ""
	base_db = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
	for base in kmer.upper()[::-1]:
		if base in base_db:
			rev_kmer += base_db[base]
		else:
			rev_kmer += base
	return rev_kmer


def write_kmers(seq, ks, fn):
	kmer_db = {}
	time_print("\tGenerating %s"%fn)
	with open(fn, 'w') as fout:
		for i in range(0, len(seq)-ks+1):
			kmer = seq[i: i+ks]
			rev_kmer = reverse_kmer(kmer)
			if kmer not in kmer_db:
				kmer_db[kmer] = 0
			if rev_kmer not in kmer_db:
				kmer_db[rev_kmer] = 0
			kmer_db[kmer] += 1
			kmer_db[rev_kmer] += 1
		
		for kmer in sorted(kmer_db):
			fout.write("%s\t%d\n"%(kmer, kmer_db[kmer]))


def get_all_kmers(in_fa, ks, out_dir, ts):
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)

	fa_db = {}
	time_print("Loading fasta and generating kmers")
	with open(in_fa, 'r') as fin:
		for line in fin:
			if line[0] == '>':
				id = line.strip().split()[0][1:]
				fa_db[id] = []
			else:
				fa_db[id].append(line.strip())
	
	time_print("Generating kmers")
	pool = multiprocessing.Pool(processes=ts)
	for id in fa_db:
		seq = ''.join(fa_db[id])
		fn = os.path.join(out_dir, id+".kmers")
		pool.apply_async(write_kmers, (seq, ks, fn,))
	pool.close()
	pool.join()
	time_print("Finished")


if __name__ == "__main__":
	if len(sys.argv) < 5:
		print("Usage: python "+sys.argv[0]+" <in_fa> <kmer_size> <out_dir> <threads>")
	else:
		in_fa, kmer_size, out_dir, ts = sys.argv[1:]
		get_all_kmers(in_fa, int(kmer_size), out_dir, int(ts))
