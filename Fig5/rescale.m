function [x,w] = rescale(x0, w0, a, b)
x = 0.5*(b-a)*x0 + 0.5*(b+a);
w = 0.5*(b-a)*w0;
end
