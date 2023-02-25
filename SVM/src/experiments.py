EXPERIMENTS = [
    {
        'C': 0.1,
        'kernel': 'linear',
        'kernel_param': None,
        'model_name': 'linear_01'
    },
    {
        'C': 10.0,
        'kernel': 'linear',
        'kernel_param': None,
        'model_name': 'linear_10'
    },
    {
        'C': 1000,
        'kernel': 'linear',
        'kernel_param': None,
        'model_name': 'linear_001'
    },
    {
        'C': 0.01,
        'kernel': 'rbf',
        'kernel_param': 0.01,
        'model_name': 'rbf_001_001'
    },
    {
        'C': 1.0,
        'kernel': 'rbf',
        'kernel_param': 0.01,
        'model_name': 'rbf_1_001'
    },
    {
        'C': float("inf"),
        'kernel': 'rbf',
        'kernel_param': 0.01,
        'model_name': 'rbf_inf_001'
    },
    {
        'C': 0.01,
        'kernel': 'rbf',
        'kernel_param': 0.001,
        'model_name': 'rbf_001_0001'
    },
    {
        'C': float("inf"),
        'kernel': 'rbf',
        'kernel_param': 1,
        'model_name': 'rbf_inf_1'
    },
]