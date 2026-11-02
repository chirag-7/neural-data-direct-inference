# J08: direct microscopy segmentation

Both complete retained fields are supplied as images, with only input-defined padding cropped and an explicit8bit conversion. Models return actual instance boundary polygons. A fixed geometry decoder rasterizes those polygons without learning or detecting anything. The unchanged native object-F1 scorer compares against each of five experts, then averages image/rater scores. See [manifest](input-manifest.json) for the exact transform and image hashes. All test annotations remain scorer-only.
