% Loop for generating angle-value curve
EXall = []; EYall = [];
theta = 0;
angle = [theta theta];

% Ply orientation sequence
% theta = 0;
% angle = [theta, -theta, -theta, theta];
len = length(angle);

% Thickness
h = 1;
H = h * len;

%
z = zeros(len+1,1);
for i = 1:(len+1)
    z(i) = h*(i-1) - H/2;
end

% Calculate the Reduced Compliance and stiffness matrix
% Local compliance matrix
S = OrthotropicCompliance3D(E1, E2, E3, Nu12, Nu23, Nu13, G12, G23, G13);
% Local stiffness matrix
Q2 = OrthotropicStiffness3D(E1, E2, E3, Nu12, Nu23, Nu13, G12, G23, G13);
Q = inv(S);
% disp(Q2-Q)

% Transform into global coordinate system
Qbar_all = {};