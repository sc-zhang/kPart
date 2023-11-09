#!/usr/bin/env python
import sys
import os
import pysam
import multiprocessing
from utils import time_print


def write_reads(in_bam, out_dir, ctg):
	with open(os.path.join(out_dir, ctg+".fq"), 'w') as fout:
		with pysam.AlignmentFile(in_bam, 'rb') as bam:
			for line in bam.fetch(contig=ctg):
				rn = line.query_name
				seq = line.query_sequence
				ctg = line.reference_name
				qual = pysam.qualities_to_qualitystring(line.query_qualities)
				if line.mapq == 0 or line.mapq == 255:
					continue
				fout.write("@%s\n%s\n+\n%s\n"%(rn, seq, qual))


def filter_reads(in_bam, out_dir, threads):
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	
	time_print("Filter reads")
	with pysam.AlignmentFile(in_bam, 'rb') as bam:
		ctg_list = []
		for item in bam.header["SQ"]:
			item = dict(item)
			ctg_list.append(item['SN'])

	pool = multiprocessing.Pool(processes=threads)
	for ctg in ctg_list:
		pool.apply_async(write_reads, (in_bam, out_dir, ctg, ))
	
	pool.close()
	pool.join()

	time_print("Finished")


if __name__ == "__main__":
	if len(sys.argv) < 4:
		print("Usage: python "+sys.argv[0]+" <in_bam> <out_dir> <threads>")
	else:
		in_bam, out_dir, threads = sys.argv[1:]
		filter_reads(in_bam, out_dir, int(threads))

