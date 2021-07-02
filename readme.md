# Will Fitch Final Year Project

This is a repository for my final year project at Brunel University London, implementing a neural regression of greenhouse gas data using fastai and transfer learning. If you're interested in the dissertation itself, email me at WRFitch@outlook.co.uk.

## TODO
- Move model training logic to GEE so the entire import pipeline becomes unnecessary. TFlow implementation available in GEE.
- Train model on a planetary scale. Super normal stuff.
  - Probably worth starting on London, then the southern UK, then the rest of the UK, then based on individual countries. 
- Export model from GEE.
- Write a basic Django REST server that uses the exported GEE model to predict coordinates.
- Write a frontend webpage to display the functionality offered by the Django server.
