# Identify Māori text
[![Build Status](https://travis-ci.org/TeHikuMedia/nga-kupu.svg?branch=master)](https://travis-ci.org/TeHikuMedia/nga-kupu)

Identify Māori words in text, and score text by the proportion of words that are in Te Reo.

## Installation
All scripts are run with python3. To install the package, run `python3 setup.py install` from the working directory. To run all scripts you need to first install `yelp_uri` and `beautifulsoup4`.

## Usage
* `kupu_tūtira` takes any textfile and returns a textfile containing a list of the words that it considers to be Māori, as well as hyphenated words. It is passed two filenames in the terminal, the first file containing the corpus, the second being the output file. It also determines how much of the text is Māori, and prints this percentage to the terminal. Use the following format to execute this script.

```
python3 kupu_tūtira.py -i input_file.txt -o output_file.txt
```


* `hihira_raupapa` takes any textfile and returns two textfiles. One contains a list of words that are considered to be Māori, and another contains a list of words that are of Māori form (consonant-vowel format, no doubling of consonants, always ends in a vowel, Māori alphabet), but are not considered to be Māori words. It checks them all against http://maoridictionary.co.nz . Use the following format to execute this script.

```
python3 hihira_raupapa -i input_file.txt -g output_file1.txt -b output_file2.txt
```

* `auaha_tūtira_tū` creates the stoplists used in the `kōmiri_kupu` function (which is called in the `kupu_tūtira` script) from a user-provided English corpus. However I have provided such lists in a subfolder referenced throughout the code called `taumahi_tūtira`, created from Google's provided list of 20,000 most commonly used English words. You may recreate these lists from the same corpus or make your own by executing the script thusly.

```
python3 auaha_tūtira_tū -i input_file
```

## Example usage

The directory `examples/gazette` uses the `kōmiri_kupu` function in the `ngā-kupu` library to identify Māori placenames in the [New Zealand Gazetteer of placenames](https://www.linz.govt.nz/regulatory/place-names/find-place-name/new-zealand-gazetteer-place-names).  In the map below, red and blue markers indicate Māori and non-Māori placenames, respectively.

![Māori placenames in New Zealand](https://github.com/TeHikuMedia/nga-kupu/blob/master/examples/gazette/aotearoa-nz.png)



