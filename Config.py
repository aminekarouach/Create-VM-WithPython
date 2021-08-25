from azure.identity import AzureCliCredential
import os



#credential
credential = AzureCliCredential()

#Récupération de l'ID d'abonnement à partir de la variable.
subscription_id = os.environ["Azure_Sub_Id"] = "729c7ae2-5a3d-4f30-9935-8d87f3158969"