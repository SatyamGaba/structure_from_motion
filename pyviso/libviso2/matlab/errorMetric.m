function [errorRot, errorTrans] = errorMetric(RPred, RGt, TPred, TGt)
diffRot = (RPred - RGt);
diffTrans = (TPred - TGt);
errorRot = sqrt(sum(diffRot(:) .* diffRot(:) ) );
errorTrans = sqrt(sum(diffTrans(:) .* diffTrans(:)) );

end