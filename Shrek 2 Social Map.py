#!/usr/bin/env python
# coding: utf-8

# #             Creating A Social Network Graph Based On Movie Scripts

# In[2]:


import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import math
get_ipython().run_line_magic('matplotlib', 'inline')


# ## Part 1: Text Parsing

# ### Load file and convert to raw text:

# In[3]:


file = open("Shrek_2.txt", encoding = "UTF-8")
#file = open("Shrek_2_v2.txt", encoding = "UTF-8")


# In[4]:


raw_text = ""

for x in file:
    raw_text += x
    
raw_text = raw_text.split("\n")

file.close()


# In[87]:


raw_text[1:10]


# ### Extracting list of characters:

# In many scripts, characters are denoted by capital letters

# In[6]:


characters = []

for x in raw_text:
    if x.isupper() and " " not in x:
        if x not in characters:
            characters.append(x)


# In[7]:


characters


# In[8]:


characters.remove("UEEN")
characters.remove("AUDIENCE")
characters.remove("FANFARE")
characters.remove("VOICE")


# In[9]:


characters


# ### Breaking Down Script Into Scenes:

# Similar to how a script denotes characters, scenes are often formatted in capital letters with INT or EXT (interior or exterior) and the setting of the scene.

# In[10]:


scenes = []

scene = []
for x in raw_text:
    if  "EXT." in x or "INT." in x:
        scenes.append(scene)
        scene = []
    else:
        scene.append(x)


# In[88]:


scenes[1]


# ### Extracting Characters In Scenes:

# In[12]:


scenes_characters = []

for scene in scenes:
    scene_characters = []
    
    for line in scene:
        if line in characters and line not in scene_characters:
            scene_characters.append(line)
    scenes_characters.append(scene_characters)


# In[13]:


df = pd.DataFrame(scenes_characters)


# In[14]:


df


# ### Assigning character relationships weights:

# The weight of each character relationship (line weight) is detirmined by how many times they appear in a scene together.

# In[80]:


weights = {}

for x in characters:
    for y in characters:
        weight = 0
        for z in range(df.T.shape[1]):
            if x in df.T[z].values and y in df.T[z].values:
                weight += 1
        weights[(x,y)] = weight / 5


# In[94]:


weights[("WOLF", "CHARMING")]


# ## Part 2: Using NetworkX to create a Social Web:

# ### Adding nodes and edges:

# In[129]:


G = nx.Graph()

G.add_nodes_from(characters, node_size = node_sizes)

for x in range(df.shape[0]):
    for y in range(df.shape[1]):
        for z in range(df.shape[1]):
            if df.iloc[x,y] != None and df.iloc[x,z] != None:
                G.add_edge(df.iloc[x,y], df.iloc[x,z], width = weights[df.iloc[x,y], df.iloc[x,z]])


# ### Setting the positions of nodes and labels:

# In[171]:


pos = {}
r = 3
theta = 2

for x in characters:
    x_coor = r * math.cos(theta)
    y_coor = r * math.sin(theta)
    
    pos[x] = (x_coor, y_coor)
    theta += .5
    
# doing the same thing for the labels separately:
label_pos = {}
r = 3.2
theta = 2

for x in characters:
    x_coor = r * math.cos(theta)
    y_coor = r * math.sin(theta)
    
    label_pos[x] = (x_coor, y_coor)
    theta += .5


# In[172]:


pos


# ### Using our weights to set node size and line weight:

# In[177]:


widths = list(nx.get_edge_attributes(G,'width').values())

node_sizes = []
for x in characters:
    node_size = 0
    for y in characters:
         node_size += weights[(x,y)]
    node_sizes.append(node_size * 125)


# ### Plotting the graph:

# In[181]:


plt.figure(figsize=(18,18))
nx.draw(G, pos, font_size = 32, width = widths, node_color = '#33cc33', edge_color = "#0a290a", node_size = node_sizes)
nx.draw_networkx_labels(G, label_pos, font_weight = "bold")

