from optimizer.assets.iconvertableasset import IConvertableAsset
from pathlib import Path

import os
import re
import shutil
import codecs

class XmodelAsset(IConvertableAsset):

	def __init__(self, inp, outp):

		self.csv_xmodel_line = []
		self.in_path = inp
		self.out_path = outp


	def cleanAssetList(self):

		if os.path.exists(Path(self.out_path) / "csv/csv_material_all.txt"):
			with open(Path(self.out_path) / "csv/csv_material_all.txt") as c:
				csv_material_all_line = c.readlines()

		outfile = []
		with open(Path(self.out_path) / "xmodel_material_list.txt", "r+") as f:
			for line in f:
				if not line.strip():
					continue
				if line in csv_material_all_line and line not in outfile:
					outfile.append(line)
			f.seek(0)
			f.writelines(outfile)
			f.truncate()


	def loadAssets(self):

		if os.path.exists(Path(self.out_path) / "csv/csv_xmodel.txt"):
			with open(Path(self.out_path) / "csv/csv_xmodel.txt") as c:
				self.csv_xmodel_line = c.readlines()


	def findXmodels(self, path, name):

		result = ""
		chars = r"A-Za-z0-9\-.,~_&$% "
		shortest_run = 1

		regexp = '[%s]{%d,}' % (chars, shortest_run)
		pattern = re.compile(regexp)

		with open(path, "rb") as binary_file:
			data = binary_file.read().decode("ansi")
			for _str in pattern.findall(data):
				result += _str + "\n"

		if not os.path.exists(Path(self.out_path) / "xmodel_material_list.txt"):
			with open(Path(self.out_path) / "xmodel_material_list.txt", "w"): 
				pass

		if os.path.exists(Path(self.out_path) / "xmodel_material_list.txt"):
			with open(Path(self.out_path) / "xmodel_material_list.txt", "a") as c:
				c.write(result)
	

	def move(self, path):

		self.out_path = path

		for root, _, files in os.walk(Path(self.in_path) / "xmodel", topdown = False):
			for name in files:

				if name + "\n" in self.csv_xmodel_line:
					f = Path(root) / name
					print(name)
					shutil.copyfile(f, Path(self.out_path) / Path("xmodel/" + name))


	def convert(self):

		for root, _, files in os.walk(Path(self.out_path) / "xmodel", topdown = False):
			for name in files:
				f = Path(root) / name
				self.findXmodels(f, name)

		self.cleanAssetList()

	
	def delete(self):

		for root, _, files in os.walk(Path(self.out_path) / "xmodel", topdown = False):
			for name in files:
				f = Path(root) / name
				delete(f)


def delete(path):

	if os.path.exists(path):
		os.remove(path)
