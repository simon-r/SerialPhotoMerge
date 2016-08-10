# Serial Photo Merge

<p class='summary'>
Serial Photo Merge is a python3 tool for computing the average of an unlimited number of images. 
Serial Photo Merge (ideally) do not load in memory all the images so it can work with a very big numbers of images. It is useful for creating a daylight very long exposure photography.
</p>

<h3>Features</h3>
<ul>
    <li>Average of an unlimited number of images</li>
    <li>Remove extraneous elements given a collection of images</li>
    <li>RAW support</li>
    <li>Supprt for 16bit color depth (otput 16bit tiff)</li>
</ul>

<h3>How to</h3>
Take your photo-camera, a good quality tripod and, if necessary, an ND filter, mount the camera on the tripod and shot a lot of images of the same subject.
After this you should use Serial Photo Merge for combining the images and obtaining the effect of a super long exposure; also in a full day light.

<h3>Advantages of Serial Photo Merge respect to the classical ND filters:</h3>
1. Improve the DR of your images.
2. Day light extreme long exposure.
3. Better flexibilty in settings the aperture and exposure time of your camera.
4. Better capacity in controlling situations with a difficult light. 

<h3>Advantages of Serial Photo Merge respect to others software [like photoshop or imagemagik]</h3>
Photoshop and Imagemagik load into memory all the images before computing the average, so the maximal number of images is limited by your installed RAM.
With Serial Photo Merge you can virtually process an unlimited number of images.  

<h3>Example</h3>
Here's some usage examples of how to use Serial Photo Merge

Observation: The images that don't fit in size and color depth of the first image in the directory will be discarded during the process.  

0. Compute the average of the images in the directory "/myimagecollection/serial/" and save the result in the default file: "/tmp/out_merge.jpg"
<pre>
> ./serial_photo_merge -d /myimagecollection/serial/
</pre>

1. Compute the average of the images in the directory "/myimagecollection/serial/" and save the result in "/tmp/r.tif" 
if the imput images are in RAW the resulting r.tif will be written in 16bit.
<pre>
> ./serial_photo_merge -d /myimagecollection/serial/ -o /tmp/r.tif -ocd auto
</pre>

2. Force the output tif to 16bit:
<pre>
> ./serial_photo_merge -d /myimagecollection/serial/ -o /tmp/r.tif -ocd 16
</pre>

2. Remove extraneous elements (slow at the moment; max 3 or 4 images)
<pre>
> ./serial_photo_merge -d /myimagecollection/serial/ -o /tmp/r.jpg -a re
</pre>

<h3>Requirements</h3>
Python 3 <br>
numpy: http://www.numpy.org/<br>
scipy: https://www.scipy.org/<br>
matplotlib: http://matplotlib.org/<br>
rawpy: https://github.com/neothemachine/rawpy (optional)<br>
imageio: https://github.com/imageio/imageio (optional)<br>

<h3>Optional arguments </h3>
<br>
usage: serial_photo_merge [-h] [-d DIR_IN] [-o OUT_IMAGE] [-ocd {8,16,auto}]<br>
                   [-a {avg,average,re,remove_extraneous}]<br>
<br>
optional arguments:<br>
  -h, --help        <br> 
  show this help message and exit<br>
  <br>
  -d DIR_IN, --dir_in DIR_IN <br>
  set the input directory <br>
  <br>
  -o OUT_IMAGE, --out_image OUT_IMAGE <br>
  set the output file (default: /tmp/out_merge.jpg ) <br>
  <br>
  -ocd {8,16,auto}, --out_color_depth {8,16,auto}  <br>
  set the output colordepth [dafault: auto] <br>
  <br>
  -a {avg,average,re,remove_extraneous}, --algorithm {avg,average,re,remove_extraneous} <br>
  select the algorithm: <br>
  avg|average: compute the average. <br>
  re|remove_extraneous: remove extraneous elements <br>
<br>
<h2>Image Example</h2>
The following image has been produced by combining more than 100 images and about 350 seconds of total exposure.
<img src="http://i.imgur.com/Sr59TfL.jpg" >
