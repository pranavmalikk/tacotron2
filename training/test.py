from data_utils import *
import logging
from training import DEFAULT_ALPHABET
from utils import *


def train(
    audio_directory,
    metadata_path=None,
    trainlist_path=None,
    vallist_path=None,
    symbols=DEFAULT_ALPHABET,
    train_size=0.8,
    logging=logging,
):
 # Load data
    logging.info("Loading data...")
    if metadata_path:
        # metadata.csv
        filepaths_and_text = load_labels_file(metadata_path)
        random.shuffle(filepaths_and_text)
        train_files, test_files = train_test_split(filepaths_and_text, train_size)
    else:
         # trainlist.txt & vallist.txt
        train_files = load_labels_file(trainlist_path)
        test_files = load_labels_file(vallist_path)
        filepaths_and_text = train_files + test_files

    validate_dataset(filepaths_and_text, audio_directory, symbols)
    trainset = TextMelLoader(train_files, audio_directory, symbols)
    valset = TextMelLoader(test_files, audio_directory, symbols)
    collate_fn = TextMelCollate()
