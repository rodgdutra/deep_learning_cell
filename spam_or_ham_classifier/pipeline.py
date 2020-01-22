import subprocess
import nltk
from nltk.corpus import stopwords
from collections import Counter
from functools import reduce
import string


def get_files_list(dir):
    command = ["ls"]
    process = subprocess.Popen(command, cwd=dir, stdout=subprocess.PIPE)
    final_output = list()
    while True:
        output = process.stdout.readline().decode()
        if output == "" and process.poll() is not None:
            break
        if output:
            final_output.append(output.split("\n")[0])

    rc = process.poll()
    return final_output


def get_email_content(file_name, dir):
    file_path = dir + "/" + file_name
    try:
        with open(file_path, "r") as f:
            file = f.read()
    except UnicodeDecodeError:
        content = ["error",file_name]
        return content
    else:
        content = file
        if "Date:" in file:
            content = file.split("Date:")[-1]
            if "Content-Transfer-Encoding:" in content:
                content = content.split("Content-Transfer-Encoding:")[-1]
        else:
            content = ["None_error"]
        return content


def process_content(content,file_name):
    file_name = file_name
    nopunc = [char for char in content if char not in string.punctuation]
    nopunc = "".join(nopunc)

    clean_words = [
        word.lower()
        for word in nopunc.split()
        #if word.lower() not in stopwords.words("english")
    ]

    return clean_words


def recurrent_words_discovery(file_list, dir):
    recurrent_words = list()
    mini_batch = 10
    n_windows = int(len(file_list) / mini_batch)

    for i in range(1, n_windows):
        i_e = i * mini_batch
        i_s = (i - 1) * mini_batch

        sets_per_file = list()
        for file in file_list[i_s:i_e]:
            content = get_email_content(file, dir)
            words = process_content(content,file)
            sets_per_file.append(Counter(words))

        batch_intersection = reduce(lambda s1, s2: s1 & s2, sets_per_file)
        print(batch_intersection)
        recurrent_words.append(batch_intersection)

    intersection_between_batch = reduce(lambda s1, s2: s1 & s2, recurrent_words)
    return intersection_between_batch
def main():
    diretories = ["easy_ham","hard_ham","easy_ham2","spam"]
    dir = diretories[-1]
    file_list = get_files_list(dir)
    recurrent_words = recurrent_words_discovery(file_list, dir)
    print("Recurrent words")
    print(recurrent_words)

if __name__ == "__main__":
    main()
