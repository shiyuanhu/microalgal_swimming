% This code simulates the dynamics of a two-filament scallop using a 
% nonlocal slender body theory
%
% Written by Shiyuan Hu <shiyuanhu@buaa.edu.cn>, Oct. 2025.

N = 101;
npts = N+1;
a = 1e-2; % filament radius
c = abs(log(a^2) + 1); % slenderness parameter
delta = 4*a; % regularization parameter for nonlocal integral

% form Clenshaw-Curtis quadrature
[s0, w0] = clencurt(N);
[s, w] = rescale(s0, w0, -1./2, 1./2);
w_rep = zeros(1, 2*npts);
w_rep(1:2:end) = w;
w_rep(2:2:end) = w;

ii = 1:2*npts;
ndim = 2*npts+1;

thetaA = 1.0; % amplitude
theta0 = 1.0; % tilt angle

% initial position of the hinged point
x0 = 0.;

% vertical separation at the hinged point
sep = 5*a;

t = 0.;
t_total = 1.0; % total simulation duration
dt = 2e-3; % time step
ifirst = 1;

Us = [];
ts = [];

datapath = pwd;
filename = fullfile(datapath, 'U_nonlocal.txt');
fileobj = fopen(filename, 'w');

while t < t_total
    % filament orientation
    theta = thetaA*sin(2*pi*t) + theta0;
    theta_dot = 2*pi*thetaA*cos(2*pi*t);
    
    % position of the two filaments
    r1_x = (s + 1./2)*cos(theta);
    r1_y = (s + 1./2)*sin(theta) + sep;
    
    r2_x = r1_x;
    r2_y = -r1_y;

    I_p_pp = [1.0+cos(theta)^2.0, cos(theta)*sin(theta); ...
              cos(theta)*sin(theta), 1.0+sin(theta)^2.0];
    I_m_pp = [1.0-cos(theta)^2.0, -cos(theta)*sin(theta); ...
              -cos(theta)*sin(theta), 1.0-sin(theta)^2.0];
    
    s_reg = ((s'-s).^2.0 + delta^2.0).^(1/2);
    s_inv = 1./s_reg;
    
    % nonlocal integral
    K1 = zeros(ndim, ndim);
    K1(ii,ii) = kron(s_inv, I_p_pp);
    K1(ii,ii) = w_rep.*K1(ii,ii);
    
    K2 = zeros(ndim, ndim);
    diags = diag(-sum(w.*s_inv, 2));
    K2(ii,ii) = kron(diags, I_p_pp);

    % local drag coefficient
    K3 = zeros(ndim, ndim);
    local_D = c*I_p_pp + 2.0*I_m_pp;
    K3(ii,ii) = kron(eye(npts,npts), local_D);
    
    % translational velocity
    K4 = sparse(1:2:2*npts, ndim*ones(1,npts), -8*pi, ndim, ndim);

    % force-free condition
    K5 = sparse(ndim*ones(1,npts), 1:2:2*npts, w, ndim, ndim);
    
    % interactions between two filaments
    R = ((r1_x'-r2_x).^2.0 + (r1_y'-r2_y).^2.0).^(1./2);
    
    Rhat_x = (r1_x'-r2_x)./R;
    Rhat_y = (r1_y'-r2_y)./R;

    K6 = zeros(ndim, ndim);
    K6(1:2:2*npts, 1:2:2*npts) = (1 + (Rhat_x.*Rhat_x))./R;
    K6(1:2:2*npts, 2:2:2*npts) = -(Rhat_x.*Rhat_y)./R;
    K6(2:2:2*npts, 1:2:2*npts) = (Rhat_y.*Rhat_x)./R;
    K6(2:2:2*npts, 2:2:2*npts) = -(1 + (Rhat_y.*Rhat_y))./R;
    K6(ii,ii) = w_rep.*K6(ii,ii);

    % lhs matrix
    lhs = K1+K2+K3+K4+K5+K6;
    
    % rhs array
    rhs = zeros(1, ndim);
    rhs(1:2:2*npts) = 8*pi*(s+1/2)*theta_dot*(-sin(theta));
    rhs(2:2:2*npts) = 8*pi*(s+1/2)*theta_dot*cos(theta);
    
    % solve the linear system
    result = (lhs\rhs')';

    U = result(end);
    if ifirst == 1
        Up = U;
    end

    x0 = x0 + 0.5*dt*(3.0*U - Up);
 
    fprintf(fileobj, "%.5f %.10f %.10f\n", [t, U, x0]);
    
    Up = U;
    Us = [Us, U];
    ts = [ts t];
    t = t+dt;
end

fclose('all');

plot(Us, 'DisplayName', "nonlocal slender body");

legend