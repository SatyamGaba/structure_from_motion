#pragma once

#include "viso_stereo.h" 

class Stereo
{
};

class Calibration
{
    double f;  // focal length (in pixels)
    double cu; // principal point (u-coordinate)
    double cv; // principal point (v-coordinate)
};

class Matching
{
    int32_t nms_n;                  // non-max-suppression: min. distance between maxima (in pixels)
    int32_t nms_tau;                // non-max-suppression: interest point peakiness threshold
    int32_t match_binsize;          // matching bin width/height (affects efficiency only)
    int32_t match_radius;           // matching radius (du/dv in pixels)
    int32_t match_disp_tolerance;   // dv tolerance for stereo matches (in pixels)
    int32_t outlier_disp_tolerance; // outlier removal: disparity tolerance (in pixels)
    int32_t outlier_flow_tolerance; // outlier removal: flow tolerance (in pixels)
    int32_t multi_stage;            // 0=disabled,1=multistage matching (denser and faster)
    int32_t half_resolution;        // 0=disabled,1=match at half resolution, refine at full resolution
    int32_t refinement;             // refinement (0=none,1=pixel,2=subpixel)
    int pre_step_size;              // the size of precomputed feature

};

class Bucket
{
    int32_t max_features;  // maximal number of features per bucket 
    double  bucket_width;  // width of bucket
    double  bucket_height; // height of bucket
};

class Parameters
{
private:
  VisualOdometryStereo::parameters params;
  
public:
  Parameters();
  ~Parameters();

  double  base() { return params.base; }             // baseline (meters)
  void    base(double b) { params.base = b; }

  int32_t ransac_iters;     // number of RANSAC iterations
  double  inlier_threshold; // fundamental matrix inlier threshold
  bool    reweighting;      // lower border weights (more robust to calibration errors)    
  
  
};

class StereoVO
{
private:
  VisualOdometryStereo* vo_;
public:
  StereoVO(Parameters* params);
  ~StereoVO();
  
  // process a new images, push the images back to an internal ring buffer.
  // valid motion estimates are available after calling process for two times.
  // inputs: I1 ........ pointer to rectified left image (uint8, row-aligned)
  //         I2 ........ pointer to rectified right image (uint8, row-aligned)
  //         dims[0] ... width of I1 and I2 (both must be of same size)
  //         dims[1] ... height of I1 and I2 (both must be of same size)
  //         dims[2] ... bytes per line (often equal to width)
  //         replace ... replace current images with I1 and I2, without copying last current
  //                     images to previous images internally. this option can be used
  //                     when small/no motions are observed to obtain Tr_delta wrt
  //                     an older coordinate system / time step than the previous one.
  // output: returns false if an error occured
  bool process (uint8_t *I1, uint8_t *I2, int32_t* dims, bool replace=false);  

  bool process (uint8_t *I1, int32_t* dims, float* feature, bool replace=false);  
  
  // call this function instead of the specialized ones, if you already have
  // feature matches, and simply want to compute visual odometry from them, without
  // using the internal matching functions.
  bool process (std::vector<Matcher::p_match> p_matched_);

  // returns transformation from previous to current coordinates as a 4x4
  // homogeneous transformation matrix Tr_delta, with the following semantics:
  // p_t = Tr_delta * p_ {t-1} takes a point in the camera coordinate system
  // at time t_1 and maps it to the camera coordinate system at time t.
  // note: getMotion() returns the last transformation even when process()
  // has failed. this is useful if you wish to linearly extrapolate occasional
  // frames for which no correspondences have been found
  Matrix getMotion ();

  // returns previous to current feature matches from internal matcher
  std::vector<Matcher::p_match> getMatches ();

  // returns the number of successfully matched points, after bucketing
  int32_t getNumberOfMatches ();
  
  // returns the number of inliers: num_inliers <= num_matched
  int32_t getNumberOfInliers ();

  // returns the indices of all inliers
  std::vector<int32_t> getInlierIndices ();
  
  // given a vector of inliers computes gain factor between the current and
  // the previous frame. this function is useful if you want to reconstruct 3d
  // and you want to cancel the change of (unknown) camera gain.
  float getGain (std::vector<int32_t> inliers_);

};
