# Prediction DDoS
Questo progetto è stato sviluppato per il corso universitario Analisi dei dati per la sicurezza.
Il progetto mira ad estrarre conoscenza dai dati per la classificazione di attacchi DDos seguendo le fasi di sviluppo del processo KDD.

![ProcessoKDD](https://github.com/francescovolpe/Prediction-DDoS/blob/main/Img/KDD-Process.png)

## Dataset
Source: [A subset of data collected by the Canadian Institute for Cybersecurity in 2019](https://www.unb.ca/cic/datasets/ddos-2019.html).
Il dataset contiene attacchi che possono essere eseguiti utilizzando protocolli basati su TCP/UDP.

| # Esempi training | # Esempi testing | # Feature | # Classi |
| :---: | :----: | :----: | :----: |
| 10.000 | 1.000 | 78 | 5 |


## Matrice di confusione sul dataset di test
![ConfusionMatrix](https://github.com/francescovolpe/Prediction-DDoS/blob/main/Img/ConfusionMatrix.png)

## Librerie utilizzate
* Python 3.8.12
* Scikit-learn 1.0
* Pandas 1.3.4
* Matplotlib 3.4.3
* Numpy 1.21.3

#### Problemi visualizzazione notebook
Se riscontri problemi nella visualizzazione dei notebook a causa del rendering, puoi utilizzare [nbviewer](https://nbviewer.jupyter.org/)