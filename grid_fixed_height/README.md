JS helper to get dimensions for a pretty image grid where each row has a specific height that allows for the images in that row to fill the complete width of the grid without cropping (except for extremely tall images).

Run it:
From this directory view example.html in browser

Details:
Accepts a list of image objects with height and width, and returns a set of rows containing images with display height and width calculated. Extremely tall images are flagged "tall" and treated as if they are cropped at a default height to avoid extremely thin images in the end result grid. 

For the sake of viewing an example, I implemented a basic grid with sample image data, and basic inline css, mustache template, and js.

