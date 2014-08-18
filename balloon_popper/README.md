A JS balloon popper for the "EASY" exhibit on Konversation.

Challenge: artist sent me a multiple large .gifs of a balloon popping at different intervals, and requested that balloons be placed around his art work, and that they pop in a specific order.

Solution: Avoid loading multiple gifs of the same baloon popping after different intervals, and have each gif only run once by using js, pre- and post- popped balloon images, and one gif.

To View: Download folder and open index.html in browser.

Description: 
I placed copies of a static image across the page. 
In the background, I load one gif of a balloon popping. 
When the page is loaded, I start with the first balloon, replacing the src with the gif, waiting 1 lifecycle of the gif, and then replacing the src with a static image of the popped balloon.
I repeat this process on the next balloon, until all of the balloons are popped.



