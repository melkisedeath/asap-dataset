import partitura
import numpy as numpy
import os
import pandas as pd



def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string


def produce_match(mfn, sfn, alignment_fn, match_name):
	"""
	Produce and Save Match.

	Parameters
	----------
	mfn : str
		Performance Midi File Path
	sfn : str
		Score musicxml File Path
	alignment : str
		Alignment ".txt" file path
	match_name : str
		Path and Save Name.


	"""

	data = pd.read_csv(alignment_fn, sep="\t")

	alignment = list()
	for x in data[["xml_id", "midi_id"]].to_numpy():
		if x[1] == "deletion":
			dd = dict(label="deletion", score_id=x[0])
		elif x[0] == "insertion":
			dd = dict(label="insertion", performance_id="n"+str(x[1]))
		else:
			dd = dict(label="match", score_id=x[0] , performance_id= "n"+str(x[1]))
		alignment.append(dd)
	ppart = partitura.load_performance_midi(mfn)
	spart = partitura.load_musicxml(sfn) 
	match = partitura.save_match(alignment, ppart, spart, match_name)



def rec_fn_search(outlist, dirname):
	"""
	Recursive Alignment File Search.


	Parameters
	----------
	outlist : list
		Argument that grows with every recursive call.

	dirname : path
		Parent Directory to look for specified files.		
	"""
	for fn in os.listdir(dirname):
		path = os.path.join(dirname, fn)
		if os.path.isdir(path):
			outlist = rec_fn_search(outlist, path)
		if os.path.isfile(path) and path.endswith("note_alignment.txt"):
			base_name = remove_suffix(os.path.basename(dirname), "_note_alignments")
			pardir = os.path.abspath(os.path.join(dirname, os.pardir))
			midi_name = os.path.join(pardir, base_name + ".mid")
			match_name = os.path.join(pardir, base_name + ".match")
			score = os.path.join(pardir, "xml_score.musicxml")
			alignment = path
			produce_match(midi_name, score, alignment, match_name)
			outlist.append(match_name)
	return outlist


def main():
	dirname = os.path.dirname(__file__)
	match_files = rec_fn_search([], dirname)








if __name__ == "__main__":
	
	main()