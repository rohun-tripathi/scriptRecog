%data = csvread('script_recognition/repository/matlab_data/english_train_char_original.csv');

O = 2;
T = 50;
nex = 50;
data = randn(O,T,nex);

O = 3;
Q = 80;

prior1 = normalise(rand(Q,1));
transmat1 = mk_stochastic(rand(Q,Q));
obsmat1 = mk_stochastic(rand(Q,O));

[LL, prior2, transmat2, obsmat2] = dhmm_em(data, prior1, transmat1, obsmat1, 'max_iter', 500);

loglik = dhmm_logprob(data, prior2, transmat2, obsmat2)

