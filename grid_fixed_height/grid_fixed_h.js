var Grid = (function() {
    var my = {};

    my.INITIAL_HEIGHT = 300;
    my.GRID_WIDTH = 960;
    my.MIN_ROW_HEIGHT = 200;
    my.MIN_IMAGE_WIDTH = 200;
    my.IMAGE_MARGIN = 4;
    my.TALL_IMAGE_RATIO = 2.5;
    my.PAGINATION = false;

    my.new_row = function(){
        return {'images':[],    
                'height':0};
    }

    my.calc_image_display_dims = function(image){
        //Assumes we know the width and height of each image
        var image_w = image.width;
        var image_h = image.height;

        //Special case: handle disproprotionately tall images that look bad resized.
        if (parseFloat(image_h) / parseFloat(image_w) > my.TALL_IMAGE_RATIO) {
            image_h = my.INITIAL_HEIGHT; //unset the height
            image.tall = true;
            //CSS will resize width only and crop height.
        }

        image.display_height = my.INITIAL_HEIGHT;
        //shrink image to row's height, maintain aspect ratio
        image.display_width = Math.round((parseFloat(image_w) * parseFloat(my.INITIAL_HEIGHT)) / parseFloat(image_h));
        image.display_padded_width = image.display_width + (my.IMAGE_MARGIN * 2);
        return;
    }   

    my.calc_row_height = function(row_width, row, image){
        var num_row_images = row.images.length;

        var row_has_room = true;
        var num_row_images_inclusive = num_row_images + 1;
        var overflow = (row_width + image.display_padded_width) - my.GRID_WIDTH;
        
        // Margin does not stretch, so use total width excluding margin to scale images
        var unpadded_row_width = my.GRID_WIDTH - my.IMAGE_MARGIN * 2 * num_row_images_inclusive;
        // Calculate what row height would need to be to include the new image
        necessary_height = Math.round(parseFloat(unpadded_row_width * my.INITIAL_HEIGHT) / parseFloat(unpadded_row_width + overflow));

        //if necessary height is too short to fit the new image, increase the row height so extisting images fill the leftover space.
        if (necessary_height < my.MIN_ROW_HEIGHT && num_row_images) {
            var row_has_room = false;
            overflow = my.GRID_WIDTH - row_width;
            unpadded_width = my.GRID_WIDTH - my.IMAGE_MARGIN * 2 * num_row_images;
            necessary_height = Math.round(parseFloat(unpadded_width * my.INITIAL_HEIGHT) / parseFloat(unpadded_width - overflow));
        }   

        row.height = necessary_height;
        return row_has_room;
    }
    
    my.finalize_row = function(row) {
        //sets final image display dimensions to match final row height.
        var final_row_height = row.height;
        var total_width = 0;

        var image;
        for (var i=0; i < row.images.length; i++) {
            image = row.images[i];
            image.display_width = Math.round(parseFloat(final_row_height * image.display_width) / parseFloat(image.display_height));
            image.display_height = final_row_height;
            total_width += image.display_width + my.IMAGE_MARGIN * 2;

            delete image.display_padded_width;  // No longer needed
        }

        // Due to rounding error, we might be off by a few pixels
        // Distribute the extra N pixels (or steal the overflow pixels) from the first N images in the row
        var overflow = parseInt(total_width - my.GRID_WIDTH);
        if (overflow) {
            var polarity = (overflow < 0) ? 1 : -1;
        
            for (var i=0; i < Math.min(Math.abs(overflow), row.images.length); i++) {
                row.images[i].display_width += polarity;
            }
        }
    }
    
    my.build_grid_rows = function(images) {
        var rows = [];
        var row = my.new_row();
        var row_width = 0;

        var image;
        for (var i=0; i < images.length; i++) {
            image = images[i];
            my.calc_image_display_dims(image);

            //check if this image will overflow the row's width at current row height
            if (row_width + image.display_padded_width < my.GRID_WIDTH) {
                row.images.push(image);
                row_width += image.display_padded_width;
            } else {
                //try adjusting row height to accomodate this image.
                row_has_room = my.calc_row_height(row_width, row, image);
                if (row_has_room) {
                    //shrink the row height to include this image
                    row.images.push(image);
                    my.finalize_row(row);
                    rows.push(row);
                    row = my.new_row();
                    row_width = 0;
                } else {
                    // end the current row as is, and start a new row with this image
                    my.finalize_row(row);
                    rows.push(row);
                    row = new_row();
                    row.images = [image];
                    row_width = image.display_padded_width;
                }
            }
        }   
        
        /* Say there's still room in current row, but we are out of images in this page to fill it.
        * If we are paginating, save them for the next page by passing back an offset.
        * If we aren't paginating or if there's no finalized rows yet, then it's the last page, and we should finalize the leftovers.
        */
        var leftout_image_count = row.images.length;
        if (leftout_image_count && (!my.PAGINATION || !rows.length)) {
            row.height = my.INITIAL_HEIGHT; //this case doesn't fill the full grid width to preserve image quality.
            my.finalize_row(row);
            rows.push(row);
            leftout_image_count = 0;
        }

        //TIP: if paginating, hold onto leftout_image_count so you can offset your next batch of images by that amount.
        var grid_data = {"image_rows": rows, "leftout_image_count": leftout_image_count};
        return grid_data;
    }   

    return my;
}());
    
    
    