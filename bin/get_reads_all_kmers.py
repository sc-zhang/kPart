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


def write_kmers(in_fq, ks, out_kmer):
	kmer_db = {}
	cnt = 0
	time_print("\tGenerating %s"%in_fq)
	with open(in_fq, 'r') as fin:
		with open(out_kmer, 'w') as fout:
			for line in fin:
				if cnt%4 == 1:
					seq = line.strip()
					for i in range(0, len(seq)-ks+1):
						kmer = seq[i: i+ks]
						rev_kmer = reverse_kmer(kmer)
						if kmer not in kmer_db:
							kmer_db[kmer] = 0
						if rev_kmer not in kmer_db:
							kmer_db[rev_kmer] = 0
						kmer_db[kmer] += 1
						kmer_db[rev_kmer] += 1
				cnt += 1
			
			for kmer in sorted(kmer_db):
				fout.write("%s\t%d\n"%(kmer, kmer_db[kmer]))


def get_all_kmers(in_fq_dir, ks, out_kmer_dir, ts):
	if not os.path.exists(out_kmer_dir):
		os.makedirs(out_kmer_dir)
	kmer_db = {}
	cnt = 0
	time_print("Loading reads and generating kmers")
	pool = multiprocessing.Pool(processes=ts)
	for fn in os.listdir(in_fq_dir):
		in_fq = os.path.join(in_fq_dir, fn)
		kmer_fn = fn.split('.')
		kmer_fn[-1] = 'kmers'
		kmer_fn = '.'.join(kmer_fn)
		out_kmer = os.path.join(out_kmer_dir, kmer_fn)
		pool.apply_async(write_kmers, (in_fq, ks, out_kmer,))
	pool.close()
	pool.join() 

	time_print("Finished")


if __name__ == "__main__":
	if len(sys.argv) < 5:
		print("Usage: python "+sys.argv[0]+" <in_fq_dir> <kmer_size> <out_kmer_dir> <threads>")
	else:
		in_fq_dir, kmer_size, out_kmer_dir, ts = sys.argv[1:]
		get_all_kmers(in_fq_dir, int(kmer_size), out_kmer_dir, int(ts))
