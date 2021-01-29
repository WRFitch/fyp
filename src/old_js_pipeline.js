// cheeky script to get data and store it in google drive. 
// Dataset must be imported in chunks to ensure the whole dataset can be worked through given limited storage

var british_isles = /* color: #d63000 */ee.Geometry.Polygon(
    [[[-1.836112801004015, 59.808076330562756],
      [-8.779472176004015, 58.82140293049428],
      [-7.988456551004015, 55.71069203454839],
      [-11.196464363504015, 54.42753859549109],
      [-11.328300301004015, 50.967746003015044],
      [-9.526542488504015, 50.77361752815123],
      [-6.274589363504015, 51.81776248652293],
      [-5.395683113504015, 51.21615275310099],
      [-6.582206551004015, 49.56332371186494],
      [-3.110526863504015, 49.904165426606255],
      [1.240059073995985, 50.80139967619036],
      [2.426582511495985, 52.33095407387208],
      [1.767402823995985, 53.4183511305661],
      [0.5369340739959849, 53.44453305344514],
      [-1.616386238504015, 56.32474216074427],
      [-0.7814253010040151, 57.805828290000164]]]),
test_bounds = /* color: #98ff00 */ee.Geometry.Polygon(
    [[[-1.0666833726431624, 51.89360084338857],
      [-0.9321008531119124, 51.38908166135181],
      [-0.18503054061191238, 51.08470683562287],
      [0.4741491468881076, 51.193274483099074],
      [0.9822668226693576, 51.60282356474035],
      [0.2269567640756076, 52.071221592742454]]]);

// Import satellite photography dataset 
function maskS2clouds(image) {
    var qa = image.select('QA60');
  
    // Bits 10 and 11 are clouds and cirrus, respectively.
    var cloudBitMask = 1 << 10;
    var cirrusBitMask = 1 << 11;
  
    // Both flags should be set to zero, indicating clear conditions.
    var mask = qa.bitwiseAnd(cloudBitMask).eq(0) 
        .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
  
    return image.updateMask(mask).divide(10000);
  }
  
  //this function is client-side, so we have to import pictures here, then export them elsewhere. Best engineers in the world...
  function exportImg(image){
      Export.image.toDrive({
        image: image,
        description: 'img2drive',
        scale: 30,
        region: test_bounds
      });
      print(image);
      return image;
  }
  
  // given a polygon, download all the images defined in its range and export them to google drive. 
  function exportImgsFromPolygon(bounds){
    print("getting images from ee");
  
    // Pre-filter to get less cloudy granules.
    var dataset = ee.ImageCollection('COPERNICUS/S2_SR') 
                    .filterDate('2020-01-01', '2020-01-30') 
                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) 
                    .filterBounds(bounds) 
                    .map(maskS2clouds);
    
    //update to import each image to this runner, then export them. 
    var dataset2 = dataset;
    ExportCol(dataset, "img_test", bounds);
    
    return dataset;
  }
  
  var ExportCol = function(col, folder, scale, type,
                           nimg, maxPixels, region) {
      type = type || "float";
      nimg = nimg || 500;
      scale = scale || 1000;
      maxPixels = maxPixels || 1e10;
  
      var colList = col.toList(nimg);
      var n = colList.size().getInfo();
  
      for (var i = 0; i < n; i++) {
        var img = ee.Image(colList.get(i));
        var id = img.id().getInfo();
        //region = region || img.geometry().bounds().getInfo()["coordinates"];
  
        var imgtype = {"float":img.toFloat(), 
                       "byte":img.toByte(), 
                       "int":img.toInt(),
                       "double":img.toDouble()
                      };
  
        Export.image.toDrive({
          image:imgtype[type],
          description: id,
          folder: folder,
          fileNamePrefix: id,
          region: test_bounds,
          scale: scale,
          maxPixels: maxPixels});
      }
    };
  
  exportImgsFromPolygon(test_bounds);