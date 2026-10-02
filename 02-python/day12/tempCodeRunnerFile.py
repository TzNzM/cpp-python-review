    logits_max = logits.max(axis=1, keepdims=True)

    shifted = logits - logits_max

    exp_values = np.exp(shifted)

    return exp_values / exp_values.sum(axis=1, keepdims=True)