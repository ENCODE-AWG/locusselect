import argparse
import pdb 
def args_object_from_args_dict(args_dict):
    #create an argparse.Namespace from the dictionary of inputs
    args_object=argparse.Namespace()
    #set the defaults for training/prediction/interpretation/cross-validation
    #training
    vars(args_object)['batch_size']=1000
    #prediction
    vars(args_object)['threads']=1
    vars(args_object)['max_queue_size']=100
    vars(args_object)['tasks']=None
    vars(args_object)['batch_size']=1000
    vars(args_object)['flank']=500
    vars(args_object)['center_on_summit']=False
    vars(args_object)['center_on_bed_interval']=False
    vars(args_object)['yaml']=None
    vars(args_object)['json']=None
    vars(args_object)['output_npz_file']=None
    vars(args_object)['sequential']=True
    vars(args_object)['global_pool_on_position']=False
    vars(args_object)['non_global_pool_on_position_size']=None
    vars(args_object)['non_global_pool_on_positin_stride']=None
    vars(args_object)['alphabet_size']=4
    vars(args_object)['outf']=None
    vars(args_object)['num_rows']=1000
    vars(args_object)['input_grad']=False
    vars(args_object)['embedding_layer_number']=None
    vars(args_object)['embedding_layer_name']=None
    vars(args_object)['embedding_input_number']=None
    vars(args_object)['embedding_input_name']=None
        
    for key in args_dict:
        vars(args_object)[key]=args_dict[key]
    args=args_object
    return args

    
    
