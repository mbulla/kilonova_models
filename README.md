# kilonova_models
Kilonova models computed using POSSIS (see Bulla 2019, MNRAS, 489, 5037 for an outline of the code).

Feel free to use these models and cite the relevant papers (see citations.bib in each model directory)

The make_lcs.py script creates bolometric and broad-band light curves for a selected grid of models. Example command line:
python make_lcs.py --doAB --doLbol --modeldir model/ --lcdir lcs/