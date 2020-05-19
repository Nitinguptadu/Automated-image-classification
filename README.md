# Automated-image-classification
This Repo is for self learning purpose and currently underdevlopment

This Repo is usefull for those who have less data for traning the deep learning model and have to train the model again and again for increment of accuracy of model 

In this project 

1) Tranning _Model.ipynb  
  
  A) Trainning a deep learning model and saving trained deep learning model in Mongodb Local server
    a) Training image dir name ["Train"] 

2) Saving_Result_Mongodb.ipynb

  A)  Importing trained model from mongodb server and predict images  
  
  B)  Using Predict function creating a DataFrame with coloumn name 
      a) filename         --- Image Name
      b) category         --- Image belong to which class either Dog or Cat
      c) Dog              --- Dog class prediction score 
      d) Cat              --- cat class prediction score
      e) Prediction       --- what % of accuacray of actuall class
      f) Time             --- Current Time of prediction
      g) Date             --- Current Date of prediction
      e) Image_string_base_64 Binary --- Converted image into base_64 string
  
  C)  Saving DataFrame to Mongodb  

 3) Retrain_Deep_learning_model.ipynb
  
  A) importing DataFrame from from Mongodb if accuracy is more than 95%
  
  B) Coverting Base_64 string into image and save in download dir
  
  C) For Balancing Data created def save() user define function
     a) if cat image(15) data is More than dog image(10) then randomly delete 5 cat image automatically same for dog class

  D) Retrain model and save model to MongoDb


 4) lastly we run a mailer script so that what % accuracy of model is increased also we use mailer for any type of report 
 
 5) flask Dir consits app_mongdb that create a database in mongodb and  using retrain model.ipynb notebook to retrain the model  


Requiremnet 
Flask
Docker
Python
CNN deep learning with keras
Mongodb
Cronjob
