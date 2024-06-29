# **`make_fsf`**

## Background
The FSL FEAT GUI  has always taken a very long time to load for me when I have more than a few EVs, inputs, or contrasts. However, manually editing this part of the .fsf document can be annoying and error prone. It's struck me as odd that this process isn't more streamlined. I thought that someone surely must have created a more modern solution in Python or R by now, but after searching off and on for a couple weeks, I didn't find one, so I made my own and thought I could share it.

## Description
`make_fsf` is simply a convenient means of automating the generation of low and high level .fsf files for FSL's FEAT. This does not add new options to FSL. It is just an alternative means of developing .fsf's to either using the FEAT GUI or manually editing a pre-existing document.

## Plans
I plan to do a few things with this project:
+ Thus far, I've only developed the functions for my own personal use. There may be use cases that this does not work for, so I will try to explore those to make it as robust as I can. 
+ I then plan to publish it to PyPI so that users can conveniently access it just as you might any other python library. Part of me wondered if this is overkill, given it's effectively just a wrapper and extremely niche, but I think the convenience is worth it.
+ I've been developing these functions in parallel both in Python and in R. If the Python library works, I will try to do the same in CRAN.

## Note
If the lack of professionalism in this README hasn't made it abundantly clear yet, I am in no way affiliated with the development of FSL. I also have not contacted anyone from FSL about this. I am just an occasional FSL user who strongly believes in the spirit of open-source, open-science, and cooperation and thought others might like this thing I made.

## Contact
If anyone has any questions, concerns, or would like to contact me, feel free to reach out at [billy.mitchell@temple.edu](mailto:billy.mitchell@temple.edu). If you have a suggestion or spot an error, please use the github issues function so that I can keep them organized and address them promptly.
