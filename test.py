from path import Path
from training.data_utils import *
import logging
from training import DEFAULT_ALPHABET
from training.utils import *
from training.utils import get_batch_size
from training.utils import get_available_memory

from torch.utils.data import DataLoader


def test(
    audio_directory,
    metadata_path,
    trainlist_path=None,
    vallist_path=None,
    symbols=DEFAULT_ALPHABET,
    train_size=0.8,
    batch_size=None,
    logging=logging,
):
    available_memory_gb = get_available_memory()
    if not batch_size:
        batch_size = get_batch_size(available_memory_gb)
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

    validate_dataset(metadata_path, filepaths_and_text, audio_directory, symbols)
    trainset = TextMelLoader(train_files, audio_directory, symbols)
    valset = TextMelLoader(test_files, audio_directory, symbols)
    collate_fn = TextMelCollate()

    # Data loaders
    train_loader = DataLoader(
        trainset, num_workers=0, sampler=None, batch_size=batch_size, pin_memory=False, collate_fn=collate_fn
    )
    val_loader = DataLoader(
        valset, num_workers=0, sampler=None, batch_size=batch_size, pin_memory=False, collate_fn=collate_fn
    )
    logging.info("Loaded data")


test(audio_directory = 'Clipper Dataset/Cloud Drive/MEGAsync Imports/Master file/Colab Folder/wavs/',metadata_path = 'Clipper Dataset/Cloud Drive/MEGAsync Imports/Master file/Colab Folder/metadata.csv', )