from optimizer.assets.i_optimizable_container import IOptimizableContainer
from pathlib import Path

import os
import re
import shutil

class ImageContainer(IOptimizableContainer):
	"""
	Represent an asset container of CoD4 image IWI files.
	"""

	def __init__(self, inp, outp):
		"""
		Initialize a new ImageContainer object.

		inp: input image folder path.
		outp: output image folder path.
		"""
		self.csv_images_line = []
		self.in_path = inp
		self.out_path = outp


	def loadAssets(self):
		"""
		Load all images from the CSV Hint file.
		"""
		if os.path.exists(Path(self.out_path) / "images_list.txt"):
			with open(Path(self.out_path) / "images_list.txt") as c:
				self.csv_images_line = c.readlines()


	def move(self, path):
		"""
		Move all images to a specified path.
		"""
		self.out_path = path

		for root, _, files in os.walk(Path(self.in_path) / "images", topdown = False):
			for name in files:

				if name + "\n" in self.csv_images_line:
					f = Path(root) / name
					print(name)
					shutil.copyfile(f, Path(self.out_path) / Path("images/" + name))


	def optimize(self):
		"""
		Optimize all images.
		"""
		pass


	def delete(self):
		"""
		Delete all images.
		"""
		for root, _, files in os.walk(Path(self.out_path) / "images", topdown = False):
			for name in files:
				f = Path(root) / name
				delete(f)


def delete(path):
	"""
	Delete a file from a specified path.
	"""
	if os.path.exists(path):
		os.remove(path)
