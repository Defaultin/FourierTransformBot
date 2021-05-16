__all__ = ('save_dataset', 'load_dataset', 'drop_dataset')
import pickle


def save_dataset(new_dataset):
    dataset = load_dataset()
    dataset.update(new_dataset)
    in_file = open('dataset.txt', 'wb')
    pickle.dump(dataset, in_file)
    in_file.close()


def load_dataset():
    out_file = open('dataset.txt', 'rb')
    dataset = pickle.load(out_file)
    out_file.close()
    return dataset


def drop_dataset():
    file = open('dataset.txt', 'wb')
    pickle.dump({}, file)
    file.close()