function y = Qbar2_test_3D(Q,theta)
%Qbar This function returns the transformed reduced
% stiffness matrix "Qbar" given the reduced stiffness matrix Q
% and the orientation angle "theta"
% There are two arguments representing Q and "theta"
% The size of the matrix is 3 x 3.
% The angle "theta" must be given in degrees.
m = cos(theta*pi/180);
n = sin(theta*pi/180);
AA = [m^4 2*m^2*n^2 0 0 n^4 0 0 0 0 4*m^2*n^2;
      m^2*n^2 m^4+n^4 0 m^2*n^2 0 0 0 0 -4*m^2*n^2;
      0 0 m^2 0 n^2 0 0 0;
      m^3*n -m*n*(m^2-n^2) 0 -m*n^3 0 0 0 -2*m*n*(m^2-n^2);
      n^4 2*m^2*n^2 0 m^4 0 0 0 4*m^2*n^2;
      0 n^2 m^2 0 0 0 0;
      m*n^3 m*n*(m^2-n^2) 0 -m^3*n 0 0 0 2*m*n*(m^2-n^2);
      0 0 0 0 0 1 0 0;
      0 0 m*n 0 -m*n 0 0;
      0 0 0 0 0 0 m^2 n^2 0;
      0 0 0 0 0 -m*n m*n 0;
      0 0 0 0 0 n^2 m^2 0;
      m^2*n^2 -2*m^2*n^2 0 m^2*n^2 0 0 0 (m^2-n^2)^2];
QQ = AA * [Q(1,1); Q(1,2); Q(1,3); Q(2,2); Q(2,3); Q(3,3); Q(4,4); Q(5,5); Q(6,6)];
y = [QQ(1) QQ(2) QQ(3) 0 0 QQ(4);
     QQ(2) QQ(5) QQ(6) 0 0 QQ(7);
     QQ(3) QQ(6) QQ(8) 0 0 QQ(9);
     0 0 0 QQ(10) QQ(11) 0;
     0 0 0 QQ(11) QQ(12) 0;
     QQ(4) QQ(7) QQ(9) 0 0 QQ(13)];