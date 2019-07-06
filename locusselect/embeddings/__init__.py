from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pdb 
#numpy & i/o
import warnings
import numpy as np
import argparse
import pysam
import pandas as pd

#import keras functions
import keras 
from keras import callbacks as cbks
from keras.losses import *
from keras.models import Model 

#import dependencies from locusselect 
from locusselect.generators import *
from locusselect.custom_losses import *
from locusselect.metrics import recall, specificity, fpr, fnr, precision, f1
from locusselect.config import args_object_from_args_dict

def parse_args():
    parser=argparse.ArgumentParser(description='Provide a model yaml & weights files & a dataset, get model predictions and accuracy metrics')
    parser.add_argument("--threads",type=int,default=1)
    parser.add_argument("--max_queue_size",type=int,default=100)
    parser.add_argument('--model_hdf5',help='hdf5 file that stores the model')
    parser.add_argument('--weights',help='weights file for the model')
    parser.add_argument('--yaml',help='yaml file for the model')
    parser.add_argument('--json',help='json file for the model')
    parser.add_argument("--embedding_layer",type=int,help="model layer for which to calculate embedding") 
    parser.add_argument('--input_bed_file',required=True,help='bed file with peaks to generate embedding')
    parser.add_argument('--batch_size',type=int,help='batch size to use to compute embeddings',default=1000)
    parser.add_argument('--ref_fasta')
    parser.add_argument('--flank',default=500,type=int)
    parser.add_argument('--center_on_summit',default=False,action='store_true',help="if this is set to true, the peak will be centered at the summit (must be last entry in bed file) and expanded args.flank to the left and right")
    parser.add_argument("--output_npz_file",default=None,help="name of output file to store embeddings. The npz file will have fields \"bed_entries\" and \"embeddings\"")
    parser.add_argument("--expand_dims",default=False,action="store_true",help="set to True if using 2D convolutions, Fales if 1D convolutions (default)") 
    return parser.parse_args()


def get_embeddings(args,model):
    data_generator=DataGenerator(args.input_bed_file,
                                 args.ref_fasta,
                                 batch_size=args.batch_size,
                                 center_on_summit=args.center_on_summit,
                                 flank=args.flank,
                                 expand_dims=args.expand_dims)
    print("created data generator") 
    embeddings=model.predict_generator(data_generator,
                                  max_queue_size=args.max_queue_size,
                                  workers=args.threads,
                                  use_multiprocessing=True,
                                  verbose=1)
    print("got embeddings")
    bed_entries=data_generator.data_index
    print("got region labels") 
    return np.asarray(bed_entries), embeddings
    
def get_embedding_layer_model(model,embedding_layer):
    return Model(inputs=model.input,
                 outputs=model.layers[embedding_layer].output)

def get_model(args):    
    custom_objects={"recall":recall,
                    "sensitivity":recall,
                    "specificity":specificity,
                    "fpr":fpr,
                    "fnr":fnr,
                    "precision":precision,
                    "f1":f1,
                    "ambig_binary_crossentropy":ambig_binary_crossentropy,
                    "ambig_mean_squared_error":ambig_mean_squared_error}
    if args.yaml!=None:
        from keras.models import model_from_yaml
        #load the model architecture from yaml
        yaml_string=open(args.yaml,'r').read()
        model=model_from_yaml(yaml_string,custom_objects=custom_objects) 
        #load the model weights
        model.load_weights(args.weights)
        
    elif args.json!=None:
        from keras.models import model_from_json
        #load the model architecture from json
        json_string=open(args.json,'r').read()
        model=model_from_json(json_string,custom_objects=custom_objects)
        model.load_weights(args.weights)
        
    elif args.model_hdf5!=None: 
        #load from the hdf5
        from keras.models import load_model
        model=load_model(args.model_hdf5,custom_objects=custom_objects)
    print("got model architecture")
    print("loaded model weights")        
    return model


def compute_embeddings(args):
    if type(args)==type({}):
        args=args_object_from_args_dict(args) 
    
    #get the original model supplied by user
    model=get_model(args)
    print("loaded model") 
    #get the model that returns embedding at user-specified layer
    embedding_layer_model=get_embedding_layer_model(model,args.embedding_layer)
    print("obtained embedding layer model") 
    #get the embeddings of the input narrowPeak file peaks 
    bed_entries,embeddings=get_embeddings(args,embedding_layer_model)
    if args.output_npz_file is not None:
        print("writing output file")
        np.savez_compressed(args.output_npz_file,bed_entries=bed_entries,embeddings=embeddings)
    return bed_entries,embeddings

    
def main():
    args=parse_args()
    compute_embeddings(args) 

    

if __name__=="__main__":
    main()
    
