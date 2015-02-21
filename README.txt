This iteration attempts to implement the eraser behavior using nearest_point_query_nearest(). It runs on OSX but fails on iOS because that method is not available for some reason when running cymunk on iOS.

FIXED: This now works. The version of cymunk I was using didn't fully implement the cymunk module. Once I built the extension from a complete version, it worked.
