###############################################################################
##  Vision Research Laboratory and                                           ##
##  Center for Multimodal Big Data Science and Healthcare                    ##
##  University of California at Santa Barbara                                ##
## ------------------------------------------------------------------------- ##
##                                                                           ##
##     Copyright (c) 2019                                                    ##
##     by the Regents of the University of California                        ##
##                            All rights reserved                            ##
##                                                                           ##
## Redistribution and use in source and binary forms, with or without        ##
## modification, are permitted provided that the following conditions are    ##
## met:                                                                      ##
##                                                                           ##
##     1. Redistributions of source code must retain the above copyright     ##
##        notice, this list of conditions, and the following disclaimer.     ##
##                                                                           ##
##     2. Redistributions in binary form must reproduce the above copyright  ##
##        notice, this list of conditions, and the following disclaimer in   ##
##        the documentation and/or other materials provided with the         ##
##        distribution.                                                      ##
##                                                                           ##
##                                                                           ##
## THIS SOFTWARE IS PROVIDED BY <COPYRIGHT HOLDER> "AS IS" AND ANY           ##
## EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE         ##
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR        ##
## PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> OR           ##
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,     ##
## EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,       ##
## PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR        ##
## PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF    ##
## LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING      ##
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS        ##
## SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.              ##
##                                                                           ##
## The views and conclusions contained in the software and documentation     ##
## are those of the authors and should not be interpreted as representing    ##
## official policies, either expressed or implied, of <copyright holder>.    ##
###############################################################################

import sys
import argparse
import os
from imUtils import *
from segUtils import *
from postUtils import *
from unetSeg import *


def main(base, parallel, seg_model, gpu, save_last, clear_cache):
	if clear_cache:
		from subprocess import call
		call(['rm', '-r', os.path.join(base, 'Thresholds')])
		call(['rm', '-r', os.path.join(base, 'UNet_Outputs')])
		call(['rm', '-r', os.path.join(base, 'MNI152')])
		call(['rm', '-r', os.path.join(base, 'Predictions')])
		call(['rm', '-r', os.path.join(base, 'Final_Predictions')])
		call(['rm', '-r', os.path.join(base, 'imname_list.pkl')])
		call(['rm', '-r', os.path.join(base, 'imname_list1.pkl')])

	else:
		if seg_model == 'unet':
			threshold(base, 'Scans', parallel)
			unetPredict(base, gpu)
		else:
			affine_transform(base)
			snake_seg(base, parallel, 'v')
			snake_seg(base, parallel, 'c')
			combine_segs(base)
		subarachnoid_seg(base, seg_model, parallel)
		get_volumes(base, seg_model, save_last)
		make_prediction(base, seg_model)
		clean_up(base)
	
  
if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--directory', default='')
	parser.add_argument('--seg_model', default='unet', help='unet or mcv')
	parser.add_argument('--parallel', action='store_true', default=False)
	parser.add_argument('--gpu', action='store_true', default=False)
	parser.add_argument('--save_last', action='store_true', default=False, help='include this to append to previous csv analysis files')
	parser.add_argument('--clear_cache', action='store_true', default=False, help='this will delete previous calculations')
	args = parser.parse_args()
	main(args.directory, args.parallel, args.seg_model, args.gpu, args.save_last, args.clear_cache)


