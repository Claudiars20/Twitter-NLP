# Find Headlines - Twitter

## Execution order
1. `CORPUS CREATOR.py`
2. `PREPROCESADO.py`
3. `BOW - WORDCLOUD.py`
4. `PONDERADO +.py`
5. `LDA.py`
6. `FIND TITULAR.py`

## File Description .py

- 📎 `CORPUS CREATOR.py`: Creates a Corpus of tweets of a certain day (Peruvian time) from the twitter accounts of Peruvian and world newscasts, it is located in: 📁`CUENTAS DE TWITTER/CUENTAS.csv`. The created Corpus is stored in the folder 📁`CORPUS` in files .json.

- 📎 `PREPROCESADO.py`: Performs the preprocessing of the tweets located in 📁`CORPUS`, cleaning noise and identifying keywords. The result of the keywords is in: 📁`CORPUS-PREPROCESADO`, In these are stored the keywords, number of retweets, number of likes, url of the news of each tweet in files .json.

- 📎 `BOW - WORDCLOUD.py`: Performs the weighted of the keywords located in 📁`CORPUS-PREPROCESADO` using TF-IDF, this result is found in: 📁`MATRICES` in files .csv, and the summary of this is in 📁`PONDERADO/PONDERADO TF-IDF`. With the result of TF-IDF we obtain word clouds, the result is in: 📁`NUBE DE PALABRAS`.

- 📎 `PONDERADO +.py`: This file is an improvement of the weighted obtained in 📁`PONDERADO/PONDERADO TF-IDF` and it is also generalized in topics (GENERAL, POLITICS, SPORTS, FARANDULA, WORLDWIDE). This improvement was made with the Fuzzy-Matching application with a threshold of >= 90% similarity and elimination of stopwords 📎`StopWordsTW.txt`. The result of the improved weighted is in: 📁`PONDERADO/PONDERADO +`.

- 📎 `LDA.py`: Carry out the Topic Modeling of the weighted keywords found in: 📁`PONDERADO/PONDERADO +`. To apply correctly, the context of each keyword is first obtained 📁`PONDERADO/PONDERADO CON CONTEXTO`, then the topics are divided by LDA 📁`PONDERADO/PONDERADO CON LDA`. As a final result you have the keywords with arrangements of the topic to which it belongs, the result is in: 📁`PONDERADO/PONDERADO KEYS + LDA`.

- 📎 `FIND TITULAR.py`: Find headlines from pre-processed tweets located in: 📁`CORPUS-PREPROCESADO`. For optimal obtaining: keywords are restricted with topic modeling in: 📁`PONDERADO/PONDERADO KEYS + LDA` To avoid the repetition of these, wordnet is applied to search with words from the context belonging to the keywords. To find the most relevant tweet, the heuristic is applied: 👍*1 + 🔁*3. Obtaining these headlines is in: `TITULARES_TF-IDF.csv`.
