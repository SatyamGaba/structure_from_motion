%module viso2

%{
#define SWIG_FILE_WITH_INIT
#include "viso_mono.h"
#include "viso_stereo.h"
#include "reconstruction.h"
%}

// enable the flattened nested class structure
%feature("flatnested");
%feature("autodoc", "0");

// handle numpy
%include numpy.i
%init %{
  import_array();
%}

%include "std_vector.i"
%include "std_string.i"

// rename the crazy nested class parameter scheme
%rename (VO_parameters) VisualOdometry::parameters;
%rename (Matcher_parameters) Matcher::parameters;
%rename (Mono_parameters) VisualOdometryMono::parameters;
%rename (Stereo_parameters) VisualOdometryStereo::parameters;

%rename (p_match) Matcher::p_match;
%rename (point3d) Reconstruction::point3d;
%rename (point2d) Reconstruction::point2d;
%rename (track) Reconstruction::track;

// make sure the static eye function is exposed
%rename(identity) Matrix::eye();
%rename(setInverse) Matrix::inv();

%rename(assign) Matrix::operator=;

// no need for iostream operators
%ignore operator<<;
typedef int int32_t;

%apply (unsigned char* IN_ARRAY2, int DIM1, int DIM2 ) {(unsigned char* image1, int rows1, int cols1),
     (unsigned char* image2, int rows2, int cols2)}
%apply (double* INPLACE_ARRAY2, int DIM1, int DIM2) { (double* mat, int rows, int cols) }
%apply (float* INPLACE_ARRAY2, int DIM1, int DIM2) { (float* feature, int num, int featureSize) }
%apply (float* INPLACE_ARRAY2, int DIM1, int DIM2) { (float* match, int num, int featureSize) }



// what interfaces to SWIG?
%include "viso.h"
%include "viso_mono.h"
%include "viso_stereo.h"
%include "matrix.h"
%include "matcher.h"
%include "reconstruction.h"

namespace std {
  %template(MatchVector) vector<Matcher::p_match>;
  %template(Point3dVector) vector<Reconstruction::point3d>;
  %template(TrackVector) vector<Reconstruction::track>;
 }

// apply the numpy typemap to enable a more comforable call with 2D images
%extend VisualOdometryMono {
  bool process_frame(unsigned char* image1, int rows1, int cols1, bool replace=false)
  {
    int dims[] = {cols1, rows1, cols1};
    return $self->process(image1, dims, replace);
  }
  bool process_frame_preFeat(unsigned char* image1, int rows1, int cols1, float* feature, int num, int featureSize, bool replace=false)
  {
    int dims[] = {cols1, rows1, cols1};
    int feature_dims[] = {num, featureSize};
    return $self->process(image1, dims, feature, feature_dims, replace);
  }
  bool process_frame_preMatch(float* match, int num, int featureSize )
  {
    int dims[] = {num};
    return $self->process(match, dims);
  }
}

%extend VisualOdometryStereo {
  bool process_frame(unsigned char* image1, int rows1, int cols1, unsigned char* image2, int rows2, int cols2, bool replace=false)
  {
    int dims[] = {cols1, rows1, cols1};
    return $self->process(image1, image2, dims, replace);
  }
}

%extend Matcher {
  void pushBack(unsigned char* image1, int rows1, int cols1, unsigned char* image2, int rows2, int cols2, bool replace=false)
  {
    int dims[] = {cols1, rows1, cols1};
    return $self->pushBack(image1, image2, dims, replace);
  }
  void pushBack(unsigned char* image1, int rows1, int cols1, bool replace=false)
  {
    int dims[] = {cols1, rows1, cols1};
    return $self->pushBack(image1, dims, replace);
  }
}

// enable string representation for the matrix object
%feature("python:slot", "tp_str", functype="reprfunc") Matrix::__str__();
%extend Matrix {
  std::string __str__() {
    std::stringstream out;
    out << *$self;
    return out.str();
    /* std::string s = out.str(); */
    /* char* returned = (char*)malloc(s.length() * sizeof(char)); */
    /* strcpy(returned, s.c_str()); */
    /* return returned; // will this work? */
  }
}

%extend Matrix {
  // support typemap for numpy extraction
  void toNumpy(double* mat, int rows, int cols) {
    // TODO: bounds checking
    return $self->getData(mat, 0, 0, rows-1, cols-1);
  }
}
