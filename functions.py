import numpy as np

def loss_func(y_hat, y):
    ## tensor product and binary cross-entropy loss function
    y_hat_new  = []
    y_new = []
    for i in range(0, len(y_hat), 2):
        tns_pd = np.tensordot(y_hat[i], y_hat[i+1], axes=0)
        y_hat_new.append([tns_pd[0][0] + tns_pd[1][1], tns_pd[0][1] + tns_pd[1][0]])
        y_new.append(y[i])
        #print(np.sum(res_new[i]))
    loss =  -np.sum(np.array(y_new) * np.log(y_hat_new)) / len(y_new) # binary cross-entropy loss
    
    return loss

def loss_func_1(y_hat, y):
    ## cosine similarity and mean squared error
    
    y_hat_new  = []
    y_new = []
    
    
    for i in range(0, len(y_hat), 2):
        cos_sim = np.dot(y_hat[i], y_hat[i+1])/(np.linalg.norm(y_hat[i])*np.linalg.norm(y_hat[i+1]))
        #cos_sim = np.dot(np.sqrt(y_hat[i]), np.sqrt(y_hat[i+1]))
        y_hat_new.append(cos_sim)
        y_new.append(y[i])
    
    loss = np.sum((np.array(y_new) - np.array(y_hat_new))**2)/len(y_new)
            
    return loss

def accuracy_func(y_hat, y):
    y_hat_new  = []
    y_new = []
    for i in range(0, len(y_hat), 2):
        tns_pd = np.tensordot(y_hat[i], y_hat[i+1], axes=0)
        y_hat_new.append([tns_pd[0][0] + tns_pd[1][1], tns_pd[0][1] + tns_pd[1][0]])
        y_new.append(y[i])
    
    acc = np.sum(np.round(y_hat_new) == y_new) / len(y_new) / 2  # half due to double-counting
    
    return acc


def accuracy_func_1(y_hat, y):
    y_hat_new  = []
    y_new = []
    
    for i in range(0, len(y_hat), 2):
        cos_sim = np.dot(y_hat[i], y_hat[i+1])/(np.linalg.norm(y_hat[i])*np.linalg.norm(y_hat[i+1]))
        #cos_sim = np.dot(np.sqrt(y_hat[i]), np.sqrt(y_hat[i+1]))
        theta = np.rad2deg(np.arccos(min(1.0, cos_sim)))
        if theta < 20:
            y_hat_new.append(1) 
        else:
            y_hat_new.append(0) 
        y_new.append(y[i])
    
    acc = 0
    for i,j in zip (y_hat_new, y_new):
        if i==j:
            acc += 1
            
    return acc/len(y_new)