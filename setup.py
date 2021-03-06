from setuptools import setup,find_packages

config = {
    'include_package_data': True,
    'description': 'Compute deep learning embeddings for narrowPeak files; compute pairwise distance between embeddings and cluster with tSNE',
    'download_url': 'https://github.com/kundajelab/locusselect',
    'version': '0.3',
    'packages': ['locusselect'],
    'setup_requires': [],
    'install_requires': ['numpy>=1.9', 'keras>=2.2', 'h5py', 'pandas','deeplift'],
    'scripts': [],
    'entry_points': {'console_scripts': ['compute_nn_embeddings = locusselect.embeddings:main',
                                         'compute_interpretation_scores = locusselect.interpret:main',
                                         'compute_embedding_distances = locusselect.dist:main',
                                         'visualize_embeddings =locusselect.vis:main',
                                         'compute_kmer_embeddings = locusselect.gapped_kmers:main']},
    'name': 'locusselect'
}

if __name__== '__main__':
    setup(**config)
