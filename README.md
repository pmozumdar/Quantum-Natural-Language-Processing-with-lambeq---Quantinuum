# Quantum-Natural-Language-Processing-with-lambeq---Quantinuum
Womanium Quantum Hackathon 2022

<h2> Intro: </h2>
<h3>Team Name : Ground_State </h3>
<strong>Team members: Pritom Mozumdar </strong> (Discord ID- Pritom#5410; Github ID - pmozumdar (https://github.com/pmozumdar); 
             email ID - mozumdar.pritom@gmail.com)<br>
 Pitch Presenter : Pritom Mozumdar <br>

<br> <strong>In the following text, I first have introduced the problem and then provided a comprehensive description of our proposed solutions. Next, we have summarized the results and given a brief descrition of the python files. </strong><br>

<h2> Problem Description:</h2> Given pair of sentences either of type 'food' or 'IT' or mixed, the challenge is to write, train and test a simple quantum-natural-language-processing(QNLP) model that can detect whether they belong to the same category or not. In order to solve this problem
one needs to find a suitable quantum representation of each sentence and a way to compare their similarity. <br>

<h2>Solution :</h2>
<h3>Steps:</h3>
&emsp;&emsp;&emsp; 1. <strong> Data processing : </strong>Read the data file and extract the sentence pairs and labels. The labels denote whether the corresponding pairs are same type of sentences (either 'food' or 'IT') or mixed type. We are going to use most of the data to train our model and the rest to test the data. Divide the data into a train and test set, generally 80% and 20% respectively. It's possible to shuffle the given data and create different train and test datasets. <br><br>

&emsp;&emsp;&emsp; 2. <strong> Creating string diagram : </strong>To create a QNLP model one first needs to convert the data into quantum circuits. The first step in that process is to decipher the grammatical structure of the sentences. For this I have used a parser named 'BobcatParser' which comes with the 'lambeq' package. A parser is a statistical tool that converts a sentence into a hierarchical representation depending on the syntactic relationships between the words based on a specific grammar formalism. A parser converts a sentence into a string diagram. For example, using 'BobcatParser' we can convert a sentence -'cook creates complicated dish', into following string diagram ![plot](https://github.com/pmozumdar/Quantum-Natural-Language-Processing-with-lambeq---Quantinuum/blob/main/sentence_diagram.pdf ). By doing so we have formulated the words into pure or entangled quantum states.<br>

&emsp;&emsp;&emsp; 3. <strong> Check and simplify string diagram : </strong>Next, we simply these string diagrams and check whether all of them have been successfully converted to string diagrams. If not we filter them out. <br>

&emsp;&emsp;&emsp; 4. <strong> Creating quantum circuits  : </strong>Using these string diagrams we can create actual quantum circuits using an predfined ansatz. An ansatz maps each wire to a qubit system and each box to a variational quantum circuit. That means an anstaz describes a subroutine consisting of a sequence of gates applied to specific wires. In this problem we have used the 'Instantaneous Quantum Polynomial' ansatz (IQP) anstaz. I have also experimented with other anstaze which are different from the default lambeq provided IQP anstaz circuit in terms of rotation gates or number of layers of circuit. While creating circuits from sentences we have kept track of sentence pairs. <br>

&emsp;&emsp;&emsp; 5. <strong> Defining model : </strong>After creating the sentence circuits we are ready to define a model using the circuit diagrams. In this problem we have used a noise free 'NumpyModel' and a noisy 'TketModel' with Aerbackend.  <br>

&emsp;&emsp;&emsp; 6. <strong> Combining circuit outputs : </strong>One of the major challenge to obtain a model which can clssaify paired sentences is to accommodate such paired sentences with a single label per pair. 'lambeq' model take a list of circuit diagrams as inputs and predict the outcomes of the input circuits as a vector state. However, for a sentence pair we have two different circuits and only one label. Thus, to combine the model predictions for these two circuits and compare with the assigned label for the pair, we need to define some method. To solve this issue I have used two dfferent methods which I am going to describe next. <br> <br>
&emsp;&emsp;&emsp;&emsp;&emsp; <strong> Tensor product </strong> :  The model prediction for a sentence circuit is a vector with two components. We can think this vector as probabilities for the qubit being in state '0' or state '1' where state  '0' or '1' would mean 'food' or 'IT' respectively or vice-versa. Now, the tensor product of the two vectors representing the circuit outcomes of the corresponding paired sentence would give a vector with four states where the elements are '00', '01', '10', and '11'. By design, if the pairs are food, they would belong to 00, and if IT, would belong to 11 and vice-versa. Similarly, '01' and '10' states would represent mixed states. Next, I add the probabilities in states '00' and '11' which is the probability of the pairs belonging to the same category. And adding probabilities for states '01' and '10' would give the probability of the pair being in a mixed pair. Thus, it's possible to reduce the combine the predictions from two different circuits which represnt a sentence pair and create a single label to compare with the given label.<br>

&emsp;&emsp;&emsp;&emsp;&emsp; <strong> Cosine similarity :</strong>  We can consider the output of each circuit as a vector in 2d space (x, y) or (0, 1)  and constrained to be in the region x^2 + y^2 = 1 and x >= 0, y >= 0. Now, we can measure how close this two vectors are by simply measuring the angel between them. If these two vectors are close the angel between them would be smaller which in turn denotes the circuits belongs two same kind of sentences. On the other hand, if the angel between the vectors are big that means the circuits belong two different kind of sentences. Thus, by measuring the angel we can also combine the ouput from two different circits and generate a single label to compare with the given label. <br>

&emsp;&emsp;&emsp; 7. <strong> Measuring loss and accuracy :</strong> Using one of the above methods we can combine the circuit outputs of the paired sentences. Then we will calculate the loss or the combined difference between the base truth and predictions of the model using a loss function. The optimizer aims to reduce the loss and modify the model weights acccordingly, which is basically the training process. In this problem, we have used lambeq provided 'SPSA' optimizer and two different loss functions. During training and testing phase, to evaluate the competency of the model we can check the prediction accuracy of the model using a accuracy function. Next, a short description of those functions. <br>

&emsp;&emsp;&emsp;&emsp;&emsp; <strong> Cross-entropy loss function : </strong> This is logarithmic loss function. Here, each predicted probability is compared to the actual truth value of 0 or 1 and a score/loss is calculated that penalizes the probability based on how far it is from the actual expected value. The penalty is logarithmic in nature yielding a large score for large differences close to 1 and small score for small differences tending to 0. <br>

&emsp;&emsp;&emsp;&emsp;&emsp; <strong> Mean-squared error : </strong> This loss function calculates the mean of the squared differences between the prediction and truth value of each data point. <br>

In our experience, it seems the binary cross-entropy loss function works well with tensor-product method and mean squared error loss function fits well with cosnine similarity method. <br> 

&emsp;&emsp;&emsp;&emsp;&emsp; <strong> Accuracy function : </strong> This function comapres the model's final prediction whether the sentence pairs belong to same category or not with the actual truth. To do this we need to convert the model outcome into '0' or '1' by comparing them against a chosen threshold. For the tensor-product method the chosen threshold was 0.5. That means if any of the state in the  final vector for a paired sentence is greater than 0.5, we have considered the prediction is denoting that state. However, for the cosine similarity method the chosen threshold is an angel. In this problem and for the given dataset our chosen threshold is 20 degree. That means if the angular differene bwteen two vectors which belong to a sentence pair is greater than the threshold, the accuracy function decides that the pair are from different category. And if the angular difference is less than 20 degree then  the sentences belong to the same category (either 'food' or 'IT). <br>

&emsp;&emsp;&emsp; 8. <strong> Defining trainer : </strong>Next, we defined a trainer by choosing a particular model (Numpy or Tket), associated backend, a loss function, a optimizer and some other parameters. <br>

&emsp;&emsp;&emsp; 9. <strong> Classify train and test circuits : </strong>We create a train and test dataset from corresponding circuit diagrams while keeping track of sentences belonging to the same pair. We ensure this by not allowing lambeq to shuffle the input list of data. <br>

&emsp;&emsp;&emsp; 10. <strong>  Train the model and test accuracy : </strong>Finally, we train the model using the train dataset and test the accuracy of the model using the test dataset. <br>

<h2> Results: </h2> <br>
&emsp;&emsp;&emsp; 1. By shuffling the provided dataset, we have created different train and test dataset. Then using differet methods (tenosr product or cosine similarity), the default IQPAnsatz  and different loss fand accuracy functions we have trained and tested the models. Using both the tensor product and cosine similarity method we got test accuracy of around 0.9 on average. <br>

&emsp;&emsp;&emsp; 2. We have created another ansatz by chaing the rotation gates of the default IQPAnstaz in labeq. We have replaced the 'Rx' rotation gates with the 'Ry' rotation gates to form this new ansatz. This new anstaz also perform sufficiently well as the default ansatz. <br>

&emsp;&emsp;&emsp; 3. The third ansatz we have tried, has been created by increasing the number of circuit layers than the default circuit layer of 1. We have tested upto five layers. We would have expected the model to train faster and the accuracy to be better with increased layer of gates. However, it doesn't seems to be the case. <br>

<h2>Description of python files: </h2> <br>
&emsp;&emsp;&emsp; <strong> checking_lambeq.ipynb </strong> -- notebook to explore the lambeq package to understand the datset and the given task.<br> <br>

&emsp;&emsp;&emsp; <strong> functions.py </strong> -- python file contains all the loss and accuracy functions. <br>

&emsp;&emsp;&emsp; <strong> tensor_product_solution.ipynb </strong>  -- notebook containing a model to solve the given task using tensor product method.<br>

&emsp;&emsp;&emsp; <strong> cosine_similarity_solution.ipynb </strong>  -- notebook containing a model to solve the given task using cosine similarity method. <br>

&emsp;&emsp;&emsp; <strong> Different_ansatz_solution_1.ipynb </strong> -- notebook showing how to create a different anasatz by changing rotation gates in IQPAnsatz and comparing it with default ansatz by checking their effects on the model using same train and test dataset. <br> 

&emsp;&emsp;&emsp; <strong> Different_ansatz_solution_2.ipynb </strong> -- notebook showing how to implement another ansatzby changing number of circuit layers and their effects on taining the model using same train and test dataset. <br>

<h2> Scalability of the project and viability for a startup: </h2> <br>
Classical natural language processing (CNLP) has numerous applications in the current world. From simple spam detection to building a chat bot, everywhere CNLP has it's footprints. Moreover, it also has its usages in science, finace, politics etc. For example, performing sentiment analysis on the accumulated data from social networks one can predict which direction election results going to tilt. One can also predcit the share market using NLP. As,we continue to work on more and more data, our classical NLP models require to handle vast amount of parameters or features which could be at the point of exhaustion for the classical coumputing resources. Then, the next scope of improvements come along with quantum computing resources. As the quantum circuits would be able accomodate umimaginable number of states, the future of QNLP is promising. This project is a small step towards that path.
