import time


def time_print(info):
    print("\033[32m%s\033[0m %s" % (time.strftime('[%H:%M:%S]', time.localtime(time.time())), info))


def reverse_kmer(kmer):
    rev_kmer = []
    base_db = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    for base in kmer[::-1]:
        if base in base_db:
            rev_kmer.append(base_db[base])
        else:
            rev_kmer.append(base)
    return ''.join(rev_kmer)


def get_kmer(kmer_db, seq, ks):
    seq = seq.upper()
    for i in range(0, len(seq) - ks + 1):
        kmer = seq[i: i + ks]
        rev_kmer = reverse_kmer(kmer)
        if kmer not in kmer_db:
            kmer_db[kmer] = 0
        if rev_kmer not in kmer_db:
            kmer_db[rev_kmer] = 0
        kmer_db[kmer] += 1
        kmer_db[rev_kmer] += 1
