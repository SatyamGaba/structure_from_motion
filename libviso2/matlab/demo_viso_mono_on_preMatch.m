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
param.pre_step_size = 258; % The length of the precomputed feature  + 2 (location on the image)
first_frame  = 0;
assert(first_frame == 0);
last_frame   = 300;

% init visual odometry
visualOdometryMonoPreMatchMex('init',param);

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
for frame=first_frame:last_frame-1
  
  % 1-based index
  k = frame-first_frame+1;
  
  % read current images
  I = imread([img_dir '/', num2str(frame,'%06d') '.png']);
  
  if k > 1
    flow = load([img_dir, '/', num2str(frame, '%06d'), '_flow.mat'] );
    flow = flow.flow;
  
    height = size(I, 1); width = size(I, 2);
    [u1, v1] = meshgrid(1:width, 1:height);
    u2 = u1 + flow(:, :, 1);
    v2 = v1 + flow(:, :, 2);
    u1 = u1(border+1:end-border, border+1:end-border);
    v1 = v1(border+1:end-border, border+1:end-border);
    u2 = u2(border+1:end-border, border+1:end-border);
    v2 = v2(border+1:end-border, border+1:end-border);
  
    u1 = u1(1:gap:end, 1:gap:end);
    v1 = v1(1:gap:end, 1:gap:end);
    u2 = u2(1:gap:end, 1:gap:end);
    v2 = v2(1:gap:end, 1:gap:end);
    u1 = u1(:); v1 = v1(:); u2 = u2(:); v2 = v2(:);
    preMatches = [u1'; v1'; u2'; v2'];
    Tr = visualOdometryMonoPreMatchMex('process', preMatches);
  else
    Tr = [];
  end

  % compute egomotion

  
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
  num_matches = visualOdometryMonoPreMatchMex('num_matches');
  num_inliers = visualOdometryMonoPreMatchMex('num_inliers');
  matches = visualOdometryMonoPreMatchMex('get_matches');

  % update image
  axes(ha1); cla;
  imagesc(I); colormap(gray);
  if k > 1
    for n = 1 : length(u1)
        line([u1(n), u2(n)], [v1(n), v2(n)]);
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
    fprintf('Mean Error Rotation: %.5f\n' , errorRotSum / (k-1) );
    fprintf('Mean Error Translation: %.5f\n',  errorTransSum / (k-1) );
  end
  pause(0.05); refresh;


  disp(['Frame: ' num2str(frame) ...
        ', Matches: ' num2str(num_matches) ...
        ', Inliers: ' num2str(100*num_inliers/num_matches,'%.1f') ,' %']);
end

% release visual odometry
visualOdometryMonoPreFeatureMex('close');
