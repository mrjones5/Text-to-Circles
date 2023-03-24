#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 21:49:41 2023

@author: mirandajones
"""

#import packages
import matplotlib.pyplot as plt
import math
import pandas as pd
import re
import numpy as np
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)

if 'input' not in st.session_state:
    st.session_state.input = ""
    
if 'encrpyted_message' not in st.session_state:
    st.session_state.encrypted_message = ''

#Make a simple app that takes a few inputs and generates an image

#Create a header
st.write("# Encrypt a Message!")

#Write a description
st.write("Each letter of the alphabet has been mapped to a \
         color. Punctuation, spaces, and special characters are automatically removed.\
         You can enter anything from a letter to a whole block of text.")

#Create a text input box
input = st.text_input("Enter Text", "abcdefghijklmnopqrstuvwxyz")

#Submit buttons
if st.button('Encrypt Message'):
         st.session_state.input = input

         #Generate the charts
         plt.subplots(sharex=True, sharey=True)

         #format the input so that it maps directly to the alphabet
         #Remove spaces
         input = st.session_state.input.replace(' ', '')
         #Remove anything that is not a letter
         input=re.sub("[^A-Za-z]","",input)
         #Make all letters lower case
         lower_input = input.lower()
         #Store in a list
         name = list(lower_input)
         #Store the length of the input
         name_length = len(name)
            
         #generate rgba codes
         #Set minimum
         min = 48
         #Set maximum
         max = 235
         #Create empty numpy arrays
         rgba_r = np.empty(26)
         rgba_g = np.empty(26)
         rgba_b = np.empty(26)
         #Fill this one with ones
         rgba_a = np.ones(26)

         #Now fill the arrays
         #Here I chose to scale the values in equal increments
         for row, element in enumerate(rgba_r):
             if row <= 5:
                 rgba_r[row]=max
             if row > 5 and row <= 9:
                 rgba_r[row] = int(max - (row-5)*(max - min)/5)
             if row > 9 and row <= 17:
                 rgba_r[row]= min
             if row > 17 and row <= 22:
                 rgba_r[row] = int(min + (row-17)*(max - min)/5)
             if row > 22:
                 rgba_r[row]=max

         for row, element in enumerate(rgba_g):
             if row <= 4:
                 rgba_g[row]= int(min + row*(max - min)/5)
             if row > 4 and row <= 13:
                 rgba_g[row] = max
             if row > 13 and row <= 17:
                 rgba_g[row]= int(max - (row-13)*(max - min)/5)
             if row > 17:
                 rgba_g[row] = min

         for row, element in enumerate(rgba_b):
             if row <= 8:
                 rgba_b[row]=min
             if row > 8 and row <= 13:
                 rgba_b[row] = int(min + (row-8)*(max - min)/5)
             if row > 13 and row <= 21:
                 rgba_b[row]= max
             if row > 21:
                 rgba_b[row] = int(max - (row-21)*(max - min)/5)

         #Specify each letter
         letter_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'] 
         #Convert to array
         letter = np.asarray(letter_list)
         #Combine all arrays
         rgba = np.c_[rgba_r,rgba_g,rgba_b,rgba_a,letter]

         #Now make a DataFrame
         rgba_df = pd.DataFrame(rgba)
         #Specify the column names
         rgba_df.columns =['R', 'G', 'B', 'A','letter']

         #Convert values to integers
         rgba_df["R"] =  rgba_df["R"].astype(float)
         rgba_df["R"] = rgba_df["R"].astype(int)

         rgba_df["G"] =  rgba_df["G"].astype(float)
         rgba_df["G"] = rgba_df["G"].astype(int)

         rgba_df["B"] =  rgba_df["B"].astype(float)
         rgba_df["B"] = rgba_df["B"].astype(int)

         rgba_df["A"] =  rgba_df["A"].astype(float)
         rgba_df["A"] = rgba_df["A"].astype(int)

         #Loop through the input and map each letter to a color
         for n, letter in enumerate(name):
             # add a new subplot iteratively

             ax = plt.subplot(int(round(math.sqrt(name_length),0)), int(round(math.sqrt(name_length),0)+1), n + 1)

             # filter df and plot ticker on the new subplot axis
             mapped_value = ord(letter)-96
             rgba_row = rgba_df[rgba_df['letter']==letter]
             rgba_row = rgba_row.reset_index()
             hue = [int(rgba_row['R'][0])/249,int(rgba_row['G'][0])/249,int(rgba_row['B'][0])/249,1]
             #rectangle = plt.Rectangle((0,0), 20, 20, fc=hue) #maybe I'll use this later?
             circle = plt.Circle(( 0.5 , 0.5 ), .5 , fc=hue)
             plt.gca().add_patch(circle)
             plt.gca().set_xticklabels([])
             plt.gca().set_yticklabels([])
             #plt.gca().set_aspect('equal')
             #plt.axis('scaled')
             plt.axis('off')

         #Generate the plot
         fig = plt.subplots_adjust(wspace=0.05, hspace=0.05)

         #Save the plot
         st.session_state.encrypted_message = plt.savefig("encrypted_message.png")
         #Display it in the Streamlit app
         st.pyplot(fig)

         with open("encrypted_message.png", "rb") as file:
            btn = st.download_button(
            label="Download as Image",
            data=file,
            file_name="encrypted_message.png",
            mime="image/png"
         )            

st.markdown("-----")
#Disclaimer
st.write("Special Note: I do not recommend using this for real message encryption.\
It is just meant to be a fun demonstration. If you want the backstory, you can \
read more in my GitHub Wiki. https://github.com/mrjones5/Text-to-Circles")

