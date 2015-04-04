%module viso2

%{
#define SWIG_FILE_WITH_INIT
#include "viso_stereo.h"
%}

// enable the flattened nested class structure
%feature("flatnested");
%feature("autodoc", "0");

// handle numpy
%include numpy.i
%init %{
  import_array();
%}


// rename the crazy nested class parameter scheme
%rename (VO_parameters) VisualOdometry::parameters;
%rename (Matcher_parameters) Matcher::parameters;
%rename (Stereo_parameters) VisualOdometryStereo::parameters;

// make sure the static eye function is exposed
%rename(identity) Matrix::eye();
%rename(setInverse) Matrix::inv();

// no need for iostream operators
%ignore operator<<;
typedef int int32_t;

%apply (unsigned char* IN_ARRAY2, int DIM1, int DIM2 ) {(unsigned char* image1, int rows1, int cols1),
     (unsigned char* image2, int rows2, int cols2)} 

// what interfaces to SWIG?
%include "viso.h"
%include "viso_stereo.h"
%include "matrix.h"
%include "matcher.h"

// apply the numpy typemap to enable a more comforable call with 2D images
%extend VisualOdometryStereo {
  bool process_frame(unsigned char* image1, int rows1, int cols1, unsigned char* image2, int rows2, int cols2, bool replace=false)
  {
    int dims[] = {cols1, rows1, cols1};
    return $self->process(image1, image2, dims, replace);
  }
}

// enable string representation for the matrix object
%feature("python:slot", "tp_str", functype="reprfunc") Matrix::__str__();
%extend Matrix {
  const char* __str__() {
    std::stringstream out;
    out << *$self;
    return out.str().c_str(); // will this work?
  }
}
