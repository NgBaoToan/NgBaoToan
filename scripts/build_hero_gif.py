#!/usr/bin/env python3
"""Build the 7.2-second illustrated banner. Requires Pillow and Inkscape."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import tempfile
from PIL import Image
from build_assets import hero, ROOT


def main():
    with tempfile.TemporaryDirectory(prefix='toan-banner-') as temp:
        folder=Path(temp)
        def frame(index):
            # Start with a readable complete scene, then loop into typing.
            elapsed=(5.8+index/10)%7.2
            source=folder/f'{index:03}.svg'
            target=folder/f'{index:03}.png'
            source.write_text(hero(elapsed=elapsed),encoding='utf-8')
            result=subprocess.run(['inkscape',str(source),'--export-type=png','--export-filename='+str(target)],capture_output=True)
            if result.returncode:
                raise RuntimeError(result.stderr.decode(errors='replace'))
            with Image.open(target) as image:
                return image.convert('RGB')
        with ThreadPoolExecutor(max_workers=4) as pool:
            images=list(pool.map(frame,range(72)))
        palette=images[0].quantize(colors=256)
        frames=[image.quantize(palette=palette,dither=Image.Dither.NONE) for image in images]
        destination=ROOT/'assets'/'hero.gif'
        frames[0].save(destination,save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True,disposal=1)
        print(f'Created {destination.name}: 72 frames, 7.2 seconds, {destination.stat().st_size} bytes')


if __name__=='__main__': main()
