import MyPillow as pillow
import os, sys


def main():
    here = sys.path[0]

    im1 = pillow.Image.open('A.png')
    im2 = pillow.Image.open('B.png')
    im1, im2 = pillow.normalize(im1, im2)

    print(pillow.getImageMatchScore(im1, im2))

    changed = pillow.getChangedImage(im1, im2)
    changed.save(os.path.join(here, 'changed.png'))

    same = pillow.getSameImage(im1, im2)
    same.save(os.path.join(here, 'same.png'))

    added = pillow.getAdditionsImage(im1, im2)
    added.save(os.path.join(here, 'added.png'))

    subtracted = pillow.getSubtractionsImage(im1, im2)
    subtracted.save(os.path.join(here, 'subtracted.png'))


if __name__ == "__main__":
    main()
