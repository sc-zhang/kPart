#!/usr/bin/env python
import sys
from utils import time_print


def classify_result(in_csv, out_csv):
	time_print("Starting classify")
	with open(in_csv, 'r') as fin:
		with open(out_csv, 'w') as fout:
			for line in fin:
				data = line.strip().split(',')
				if data[0] == 'ContigName':
					sample_list = []
					for info in data[-2:]:
						sample_list.append(info.split()[-1])
					data.append("Classification")
					fout.write("%s\n"%(','.join(data)))
				else:
					ctg = data[0]
					vals = list(map(int, data[3:]))
					for i in range(0, len(vals)):
						if vals[i] == 0:
							vals[i] = 1
					if vals[0]*1.0/vals[1] > 2.0:
						data.append(sample_list[0])
					elif vals[1]*1.0/vals[0] > 2.0:
						data.append(sample_list[1])
					else:
						data.append('Undetermined')
					fout.write("%s\n"%(','.join(data)))
	time_print("Finished")


if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Usage: python %s <in_csv> <out_csv>"%sys.argv[0])
	else:
		in_csv, out_csv = sys.argv[1:]
		classify_result(in_csv, out_csv)

