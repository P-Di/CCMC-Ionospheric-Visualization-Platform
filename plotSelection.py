def plot_selection_format(plot,options, graphs):

    chl = [None, None, None, None, None, None, None, None]
    #options = ['DK_F', 'MS_F', 'SN_F', 'RCC']
    for p, j in enumerate(plot):
        for i, k in enumerate(options):
            if k == j:
                chl[p] = graphs[i]
    return chl