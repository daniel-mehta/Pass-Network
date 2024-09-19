import pandas as pd
from mplsoccer.pitch import Pitch
import matplotlib.pyplot as plt

#read in csv
df = pd.read_csv('valladolidA.csv')

#print(df.to_string()) 

df = df[df['teamId'] == 'Barcelona']

#print(df.to_string()) 

df['passer'] = df['playerId']
df['recipient'] = df['playerId'].shift(-1)

passes = df[df['type'] == 'Pass']
successful = passes[passes['outcome'] == 'Successful']

#print(successful.to_string())

subs = df[df['type'] == 'SubstitutionOff']
subs = subs['minute']

firstSub = subs.min()

#print(firstSub)

successful = successful[successful['minute']<firstSub]

#print(successful.to_string())

pas = pd.to_numeric(successful['passer'], downcast = 'integer')
rec = pd.to_numeric(successful['recipient'], downcast = 'integer')

successful['passer'] = pas
successful['recipient'] = rec

#print(successful.to_string())

averageLocations = successful.groupby('passer').agg({'x':['mean'], 'y':['mean', 'count']})
averageLocations.columns = ['x', 'y', 'count']

#print(averageLocations)

passBetween = successful.groupby(['passer', 'recipient']).id.count().reset_index()
passBetween.rename({'id': 'pass_count'}, axis='columns', inplace=True)

passBetween = passBetween.merge(averageLocations, left_on='passer', right_index = True)
passBetween = passBetween.merge(averageLocations, left_on='recipient', right_index = True, suffixes = ['', '_end'])

#print(passBetween)

passBetween = passBetween[passBetween['pass_count']>3]

#print(passBetween)

pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=False, tight_layout=True)
fig.set_facecolor('#22312b')


arrows = pitch.arrows(1.2*passBetween.x, .8*passBetween.y, 1.2*passBetween.x_end,.8*passBetween.y_end, ax=ax, width = 3, headwidth = 3, color = 'white', zorder = 1, alpha = .5)

#plt.show()

nodes = pitch.scatter(1.2*averageLocations.x, .8*averageLocations.y, s = 300, color = '#d3d3d3', edgecolors = 'black', linewidth = 2.5, alpha = 1, zorder = 1, ax=ax)

plt.show()