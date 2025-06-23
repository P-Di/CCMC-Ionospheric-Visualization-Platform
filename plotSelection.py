def plot_selection_format(plot,options, graphs):

    chl = [None, None, None, None, None, None, None, None]
    style_sel = []
    for p, j in enumerate(plot):
        for i, k in enumerate(options):
            if k == j:
                chl[p] = graphs[i]
    for i in chl:
        if i == None:
            style_sel.append(9)
        else:
            style_sel.append(8)
    return chl, style_sel