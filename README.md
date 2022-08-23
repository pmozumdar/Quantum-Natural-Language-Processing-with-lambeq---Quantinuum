# Quantum-Natural-Language-Processing-with-lambeq---Quantinuum
Womanium Quantum Hackathon 2022

<h2> Intro: </h2>
<h3>Team Name : Ground_State </h3>
<strong>Team members: Pritom Mozumdar </strong>(Discord ID- Pritom; Github ID- pmozumdar (https://github.com/pmozumdar)<br> 
            &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; email ID - mozumdar.pritom@gmail.com)<br>
 Pitch Presenter : Pritom Mozumdar <br>

<h2> Problem Description:</h2> Given pair of sentences either of type 'food' or 'IT' or mixed, the challenge is to write, train and test a simple quantum-natural-language-processing(QNLP) model that can detect whether they belong to the same category or not. In order to solve this problem
one needs to find a suitable quantum representation of each sentence and a way to compare their similarity. <br>

<h2>Solution :</h2>
<h3>Steps:</h3>
&emsp;&emsp;&emsp; 1. Read the data file and extract the sentence pairs and labels. The labels denote whether the corresponding pairs are same type of sentences (either 'food' or 'IT') or mixed type. We are going to use most of the data to train our model and the rest to test the data. <br/><br />  
&emsp;&emsp;&emsp; 2. Divide the data into a train and test set, generally 80% and 20% respectively. It's possible to shuffle the given data and create different train and test datasets. <br><br>

&emsp;&emsp;&emsp; 3. To create a QNLP model one first needs to convert the data into quantum circuits. The first step in that process is to decipher the grammatical structure of the sentences. For this I have used a parser named 'BobcatParser' which comes with the 'lambeq' package. A parser is a statistical tool that converts a sentence into a hierarchical representation depending on the syntactic relationships between the words based on a specific grammar formalism. <br><br>

&emsp;&emsp;&emsp; 3.
