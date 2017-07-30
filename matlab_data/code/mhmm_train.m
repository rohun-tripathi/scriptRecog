T = 50;
nex = 50;
data = randn(T,nex);

M = 2;
Q = 2;
left_right = 0;

prior0 = normalise(rand(Q,1));
transmat0 = mk_stochastic(rand(Q,Q));

cov_type="full"
[mu0, Sigma0] = mixgauss_init(Q*M, data, cov_type);
mu0 = reshape(mu0, [Q M]);
Sigma0 = reshape(Sigma0, [Q M]);
mixmat0 = mk_stochastic(rand(Q,M));


[LL, prior1, transmat1, mu1, Sigma1, mixmat1] = ...
    mhmm_em(data, prior0, transmat0, mu0, Sigma0, mixmat0, 'max_iter', 2);
