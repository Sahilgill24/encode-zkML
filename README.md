

## Zk-ML


A personalized ad assistant that uses the user's data to train a model for showing personalized adds but we know the data remains private . Also comparing the bench marking results of Risczero and EZKL . (if it makes sense then only which it most probably doesn't )

Running a public model on Private data . 


## Resources 

https://www.geeksforgeeks.org/targeted-advertising-using-machine-learning/

https://github.com/Azure/cortana-intelligence-personalization-data-science-playbook/blob/master/Personalized_Offers_from_Classifiers_Use_Case.md


## Architecture 

data -> sent to the server makes it non sense 
so the model shall be trained locally on the user's machine along with a neutral dataset of ads and their types 
and the data then be encrypted and sent to a server 
which would then send the response containig the Ad id's that should be shown {this would be 
checked from the data set that contains the link's betweeen the ads and their similarity}

otherwise 

sending the data straight to the server , which sends the corresponding ad id's 