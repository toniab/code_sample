# DEMONSTRATE GRID_FIXED_H DATA
import grid_fixed_h

# SAMPLE THUMBNAILED IMAGE DATA
images = [
       {"url":"http://s.likes-media.com/img/dab39c79b6bae635cdf1b92892bf9a44.600x.jpg", "width":250, "height":210},
       {"url":"http://s.likes-media.com/img/dd8343a787506c91d3eeff50b12ee63b.600x.jpg", "width":600, "height":600},
       {"url":"http://s.likes-media.com/img/32b71edb2d59e76aedd476017fe68ea4.600x.jpg", "width":600, "height":300},
       {"url":"http://s.likes-media.com/img/97e97aea3e72908ac18b8150c8abff6e.600x.jpg", "width":599, "height":610},
       {"url":"http://s.likes-media.com/img/02ec9ab5c7a572c186d1fdd8e51e8093.600x.jpg", "width":599, "height":447},
       {"url":"http://s.likes-media.com/img/fcb21bc7d1a7168e684742a5dd6d8d83.600x.jpg", "width":500, "height":509},
       {"url":"http://d2tq98mqfjyz2l.cloudfront.net/image_cache/139176938718545_tall.jpg", "width":500, "height":5615},
       {"url":"http://s.likes-media.com/img/6db957725d8d3731d17dd68764c11776.600x.jpg", "width":500, "height":667},
       {"url":"http://s.likes-media.com/img/f4f8afeeab872f2fa444113f8c814876.600x.jpg", "width":600, "height":450},
       {"url":"http://s.likes-media.com/img/69992cd2bfe1d406b52677fb1f4d8ccc.600x.jpg", "width":500, "height":684},
       {"url":"http://s.likes-media.com/img/9a65b65b1eb8bc7cdedbc063d1633d2a.600x.jpg", "width":599, "height":412},
       {"url":"http://d2tq98mqfjyz2l.cloudfront.net/image_cache/1392123123914130_tall.jpg", "width":500, "height":8735},
       {"url":"http://s.likes-media.com/img/e6db8b27eb18dbd58f69cf37d48bdae8.600x.gif", "width":296, "height":406},
       {"url":"http://s.likes-media.com/img/1515c6c7e4793217bba22cebef71c8d4.600x.jpg", "width":600, "height":600},
       {"url":"http://s.likes-media.com/img/099530d5629e8813bec1f3632f011ac3.600x.jpg", "width":500, "height":375},
       {"url":"http://s.likes-media.com/img/8e9db23caad7c99b789b2d0c6a60cf47.600x.gif", "width":500, "height":500},
       {"url":"http://s.likes-media.com/img/8d25d66ba36b8f5463af7f8e742e3880.600x.jpg", "width":500, "height":750},
       {"url":"http://s.likes-media.com/img/37d0e039e750ea06e0454ec5e6763af8.600x.jpg", "width":359, "height":574},
       {"url":"http://s.likes-media.com/img/fb134dcefde711378a93e96afe266597.600x.jpg", "width":500, "height":500},
]

grid_data = grid_fixed_h.build_grid_rows(images)

print ""
print "Creating grid with %s images" % len(images)
print "Grid is %s rows total" % len(grid_data['image_rows'])
print ""
for index, row in enumerate(grid_data['image_rows']):
    print "Row #%s - %spx tall" % (index + 1, row['height'])

    for image_index, image in enumerate(row['images']):
        print ""
        print "Row %s Image %s: %s" % (index +1, image_index + 1, image['url'])
        print "Natural dims %s x %s" % (image['width'], image['height'])
        print "Display dims %s x %s" % (image['display_width'], image['display_height'])
        if image.get('tall'):
           print "*NOTE: TALL IMAGE, cropped to default height"

    print ""
    print ""
    print ""

print "No more rows."
