INITIAL_HEIGHT = 300
GRID_WIDTH = 959
MIN_ROW_HEIGHT = 200
MARGIN = 4
MIN_IMAGE_WIDTH = 200
TALL_IMAGE_RATIO = 2.5
PAGINATION = False

def new_row():
    return {'images':[],
            'height':0}

def calc_image_display_dims(image):
    #Assumes we know the width and height of each image
    image_w = image['width']
    image_h = image['height']

    #Special case: handle disproprotionately tall images that look bad resized.
    if float(image_h) / float(image_w) > TALL_IMAGE_RATIO:
        image_h = INITIAL_HEIGHT #unset the height
        image['tall'] = True
        #CSS will resize width only and crop height.

    image['display_height'] = INITIAL_HEIGHT
    #if we shrink image to grid row's height, decide how much width the image will take up.
    image['display_width'] = int(round((float(image_w) * float(INITIAL_HEIGHT)) / float(image_h)))
    image['display_padded_width'] = image['display_width'] + (MARGIN * 2)
    return

def calc_row_height(row_width, row, image):
    num_row_images = len(row['images'])

    row_has_room = True
    num_row_images_inclusive = num_row_images + 1
    overflow = (row_width + image['display_padded_width']) - GRID_WIDTH

    # Margin does not stretch, so use total width excluding margin to scale images
    unpadded_row_width = GRID_WIDTH - MARGIN * 2 * num_row_images_inclusive
    # Calculate what row height would need to be to include the new image
    necessary_height = int(round(float(unpadded_row_width * INITIAL_HEIGHT) / float(unpadded_row_width + overflow)))

    #if necessary height is too short to fit the new image, increase the row height so extisting images fill the leftover space.
    if necessary_height < MIN_ROW_HEIGHT and num_row_images:
        row_has_room = False
        overflow = GRID_WIDTH - row_width
        unpadded_width = GRID_WIDTH - MARGIN * 2 * num_row_images
        necessary_height = int(round(float(unpadded_width * INITIAL_HEIGHT) / float(unpadded_width - overflow)))

    row['height'] = necessary_height
    return row_has_room

def finalize_row(row):
    #sets final image display dimensions to match final row height.
    final_row_height = row['height']
    total_width = 0

    for image in row['images']:
        image['display_width'] = int(round(float(final_row_height * image['display_width']) / float(image['display_height'])))
        image['display_height'] = final_row_height
        total_width += image.get('display_width') + MARGIN * 2

        del image['display_padded_width']  # No longer needed

    # Due to rounding error, we might be off by a few pixels
    # Distribute the extra N pixels (or steal the overflow pixels) from the first N images in the row
    overflow = int(total_width - GRID_WIDTH)
    if overflow:
        polarity = 1 if overflow < 0 else -1
        for row_image in row['images'][:abs(overflow)]:
            row_image['display_width'] += polarity

def build_grid_rows(images):
    rows = []
    row = new_row()
    row_width = 0

    for image in images:

        calc_image_display_dims(image)

        #check if this image will overflow the row's width at current row height
        if row_width + image['display_padded_width'] < GRID_WIDTH:
            row['images'].append(image)
            row_width += image['display_padded_width']
        else:
            #try adjusting row height to accomodate this image.
            row_has_room = calc_row_height(row_width, row, image)
            if row_has_room:
                #shrink the row height to include this image
                row['images'].append(image)
                finalize_row(row)
                rows.append(row)
                row = new_row()
                row_width = 0
            else:
                #end the current row as is, and start a new row with this image
                finalize_row(row)
                rows.append(row)
                row = new_row()
                row['images'] = [image]
                row_width = image['display_padded_width']

    #Say there's still room in current row, but we are out of images in this page to fill it.
    # If we are paginating, save them for the next page by passing back an offset.
    leftout_image_count = len(row['images'])

    #if we aren't paginating or if there's no finalized rows yet it is the last page, and we should finalize the leftovers.
    if leftout_image_count and (not PAGINATION or not len(rows)):
        row['height'] = INITIAL_HEIGHT; #this case doesn't fill the full grid width to preserve image quality.
        finalize_row(row)
        rows.append(row)
        leftout_image_count = 0

    #TIP: if paginating, hold onto leftout_image_count so you can offset your next batch of images by that amount.

    grid_data = {"image_rows": rows, "leftout_image_count": leftout_image_count}
    return grid_data

