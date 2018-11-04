import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
data = pd.read_csv('example.csv')

df = pd.DataFrame(data)

# sns.set_style("ticks")
# sns.pairplot(data, hue="Class")
#
#
plt.scatter