import MyPillow as Pillow
from PIL import Image, ImageChops as Chops
import Transform as Trans
import os
import sys


def main():
	here = sys.path[0]

	imA = Image.open('A.png')
	imB = Image.open('B.png')
	imC = Image.open('C.png')
	im1 = Image.open('1.png')
	im2 = Image.open('2.png')
	im3 = Image.open('3.png')
	im4 = Image.open('4.png')
	im5 = Image.open('5.png')
	im6 = Image.open('6.png')
	imA, imB, imC, im1, im2, im3, im4, im5, im6 = Pillow.normalize(imA, imB, imC, im1, im2, im3, im4, im5, im6)

	ans_im = im5

	changed_hor = Pillow.getChangedImage(imA, imB)
	changed_hor.save(os.path.join(here, 'changed_hor.png'))

	changed_vert = Pillow.getChangedImage(imA, imC)
	changed_vert.save(os.path.join(here, 'changed_vert.png'))

	changed_B_ans = Pillow.getChangedImage(imB, ans_im)
	changed_B_ans.save(os.path.join(here, 'changed_B_ans.png'))

	changed_C_ans = Pillow.getChangedImage(imC, ans_im)
	changed_C_ans.save(os.path.join(here, 'changed_C_ans.png'))

	print('Best Horizontal Socre:', Pillow.getImageMatchScore(changed_hor, changed_C_ans))
	print('Best Vertical Socre:', Pillow.getImageMatchScore(changed_vert, changed_B_ans))

if __name__ == "__main__":
	main()