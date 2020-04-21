% demonstrates mono visual odometry on an image sequence
disp('===========================');
clear all; close all; %dbstop error;

% parameter settings (for an example, please download
img_dir      = '../../dataset/sequences/00/image_0/';
gt_dir       = '../../dataset/poses/00.txt';
calibFile    = '../../dataset/sequences/00/calib.txt';
border       = 50;
gap          = 15;

% Load the camera calibration information 
fid = fopen(calibFile, 'r');
calibInfo = fscanf(fid, '%s %f %f %f %f %f %f %f %f %f %f %f %f');
calibInfo = calibInfo(4:15);
param.f      = calibInfo(1);
param.cu     = calibInfo(3);
param.cv     = calibInfo(7);

% Load the ground-truth depth and rotation
fid = fopen(gt_dir, 'r');
gtTr = fscanf(fid, '%f');
gtTr = reshape(gtTr, [4, 3, length(gtTr) / 12] );
gtTr = permute(gtTr, [3, 2, 1] );
param.height = 1.6;
param.pitch  = -0.08;
param.match.pre_step_size = 64;
first_frame  = 0;
last_frame   = 300;

% init visual odometry
visualOdometryMonoMex('init',param);

% init transformation matrix array
Tr_total{1} = eye(4);

% create figure
figure('Color',[1 1 1]);
ha1 = axes('Position',[0.05,0.7,0.9,0.25]);
axis off;
ha2 = axes('Position',[0.05,0.05,0.9,0.6]);
set(gca,'XTick',-500:10:500);
set(gca,'YTick',-500:10:500);
axis equal, grid on, hold on;

% for all frames do
replace = 0;
errorTransSum = 0; 
errorRotSum = 0;
errorRotArr = zeros(1, last_frame-first_frame - 1);
errorTransArr = zeros(1, last_frame-first_frame-1);
for frame=first_frame:last_frame-1
  
  % 1-based index
  k = frame-first_frame+1;
  
  % read current images
  I = imread([img_dir '/' num2str(frame,'%06d') '.png']);

  % compute egomotion
  Tr = visualOdometryMonoMex('process',I,replace);
  
  % accumulate egomotion, starting with second frame
  if k>1
    
    % if motion estimate failed: set replace "current frame" to "yes"
    % this will cause the "last frame" in the ring buffer unchanged
    if isempty(Tr)
      replace = 1;
      Tr_total{k} = Tr_total{k-1};
      
    % on success: update total motion (=pose)
    else
      replace = 0;
      Tr_total{k} = Tr_total{k-1}*inv(Tr);
    end
  end
  
  % output statistics
  num_matches = visualOdometryMonoMex('num_matches');
  num_inliers = visualOdometryMonoMex('num_inliers');
  matches = visualOdometryMonoMex('get_matches');

  % update image
  axes(ha1); cla;
  imagesc(I); colormap(gray);
   if size(matches, 2) ~= 0
      for n = 1 : size(matches, 2)
        line([matches(1, n)', matches(3, n)'], [matches(2, n)', matches(4, n)']);
      end
  end
  axis off;
  
  % update trajectory
  axes(ha2);
  if k>1
   plot([Tr_total{k-1}(1,4) Tr_total{k}(1,4)], ...
         [Tr_total{k-1}(3,4) Tr_total{k}(3,4)],'-xb','LineWidth',1);
    plot([gtTr(k-1, 1, 4) gtTr(k, 1, 4)], ...
        [gtTr(k-1, 3, 4), gtTr(k, 3, 4)], '-xr', 'LineWidth', 1);
    % Compute rotation
    Rpred_p = Tr_total{k-1}(1:3, 1:3);
    Rpred_c = Tr_total{k}(1:3, 1:3);
    Rpred = (Rpred_c)' * Rpred_p; 
    Rgt_p = squeeze(gtTr(k-1, 1:3, 1:3));
    Rgt_c = squeeze(gtTr(k, 1:3, 1:3) );
    Rgt = (Rgt_c)' * Rgt_p;
    % Compute translation 
    Tpred_p = Tr_total{k-1}(1:3, 4);
    Tpred_c = Tr_total{k}(1:3, 4);
    Tpred = Tpred_c - Tpred_p;
    Tgt_p = gtTr(k-1, 1:3, 4);
    Tgt_c = gtTr(k, 1:3, 4);
    Tgt = Tgt_c - Tgt_p;
    
    [errorRot, errorTrans] = errorMetric(Rpred, Rgt, Tpred, Tgt);
    errorRotSum = errorRotSum + errorRot;
    errorTransSum = errorTransSum + errorTrans;
    errorRotArr(k-1) = errorRot;
    errorTransArr(k-1) = errorTrans;
    fprintf('Mean Error Rotation: %.5f\n' , errorRotSum / (k-1) );
    fprintf('Mean Error Translation: %.5f\n',  errorTransSum / (k-1) );
  end
  pause(0.05); refresh;
  

  disp(['Frame: ' num2str(frame) ...
        ', Matches: ' num2str(num_matches) ...
        ', Inliers: ' num2str(100*num_inliers/num_matches,'%.1f') ,' %']);
end

% release visual odometry
visualOdometryMonoMex('close');
