#!/bin/sh
# python genPostProcessing.py --targetDir v2 --overwrite --addReweights --logLevel INFO --interpolationOrder 2 --delphesEra RunII --sample TTTT_MS #SPLIT493
# python genPostProcessing.py --targetDir v2 --overwrite --addReweights --logLevel INFO --interpolationOrder 2 --delphesEra RunII --sample TTbb_MS #SPLIT497
python genPostProcessing.py --targetDir v4 --overwrite --addReweights --logLevel INFO --interpolationOrder 2 --delphesEra RunII --sample TTTT_MS #SPLIT493
python genPostProcessing.py --targetDir v4 --overwrite --addReweights --logLevel INFO --interpolationOrder 2 --delphesEra RunII --sample TTbb_MS #SPLIT497
