# Image Merge

<p class='summary'>
ImageMerge is a python3 tool for computing the average of an unlimited number of images. 
ImageMerge (ideally) do not load in memory all the images so it can work with a very big numbers of images. It is useful for creating a daylight very long exposure photography.
</p>

<h2>Features</h2>
<ul>
    <li>Average of an unlimited number of images</li>
    <li>Remove extraneous elements given a collection of images</li>
</ul>

<h2>How to</h2>
Take your photo-camera, a good quality tripod and, if necessary, a ND filter, and shot a lot of images of the same subject.
After this you should use ImageMerge for combining the images and obtaining the effect of a super long exposure; also in full day light.

<h2>Advantages of ImageMerge respect to the classical ND filters:</h2>
1. Improve the DR of your images.
2. Day light extremely long exposure.
3. Better flexibilty in setting the aperture and exposure time of your camera.
4. Better capacity in controlling the situations with a difficult light. 

<h2>Advantages of ImageMerge respect to others software [like photoshop or imagemagik]</h2>
Photoshop and Imagemagik load in to memory all the images before computing the average, so the maximal number of images is limited by your installed RAM.
With ImageMerge you can virtually process an unlimited number of images.  

<h2>Example</h2>
Here's some usage examples of how to use ImageMerge

Observation: The images that don't fit in size and color depth of the first image in the directory will be discarded during the process.  

0. Compute the average of the images in the directory "/myimagecollection/serial/" and save the result in the default file: "/tmp/out_merge.jpg"
<pre>
> ./image_merge -d /myimagecollection/serial/
</pre>

1. Compute the average of the images in the directory "/myimagecollection/serial/" and save the result in "/tmp/r.tif" 
if the imput images are in RAW the resulting r.tif will be written in 16bit.
<pre>
> ./image_merge -d /myimagecollection/serial/ -o /tmp/r.tif -ocd auto
</pre>

2. Force the output tif to 16bit:
<pre>
> ./image_merge -d /myimagecollection/serial/ -o /tmp/r.tif -ocd auto
</pre>

2. Remove extraneous elements (slow at the moment; max 3 or 4 images)
<pre>
> ./image_merge -d /myimagecollection/serial/ -o /tmp/r.jpg -a re
</pre>


<h2> optional arguments </h2>

usage: image_merge [-h] [-d DIR_IN] [-o OUT_IMAGE] [-ocd {8,16,auto}]
                   [-a {avg,average,re,remove_extraneous}]

optional arguments:
  -h, --help            
  show this help message and exit
  
  -d DIR_IN, --dir_in DIR_IN   
  set the input directory
  
  -o OUT_IMAGE, --out_image OUT_IMAGE  
  set the output file (default: /tmp/out_merge.jpg )
  
  -ocd {8,16,auto}, --out_color_depth {8,16,auto}  
  set the output colordepth [dafault: auto]
  
  -a {avg,average,re,remove_extraneous}, --algorithm {avg,average,re,remove_extraneous}  
  select the algorithm: 
  avg|average: compute the average.
  re|remove_extraneous: remove extraneous elements

